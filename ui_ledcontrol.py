# ui_ledcontrol.py
import asyncio
import colorsys
import json
import os
from bleak import BleakClient
import customtkinter as ctk
from tkinter import colorchooser
import tkinter.messagebox as messagebox


BLE_CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
CONFIG_FILE = "led_config.json"

def rgb_to_hsb(r, g, b):
    h, s, _ = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return int(h * 360), int(s * 1000)

def gerar_comando_hsb(h, s):
    return bytes([0xBC, 0x04, 0x06, (h >> 8) & 0xFF, h & 0xFF, (s >> 8) & 0xFF, s & 0xFF, 0x00, 0x00, 0x55])

def comando_on():
    return bytes([0xCC, 0x23, 0x33])

def comando_off():
    return bytes([0xCC, 0x24, 0x33])

class ConfiguracaoDispositivo:
    def __init__(self, path=CONFIG_FILE):
        self.path = path
        self.dados = self._carregar()

    def _carregar(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {}

    def salvar(self):
        with open(self.path, "w") as f:
            json.dump(self.dados, f, indent=4)

    def get_default_color(self, address):
        return self.dados.get(address)

    def set_default_color(self, address, h, s):
        self.dados[address] = {"h": h, "s": s}
        self.salvar()

def open_led_control(parent, device):
    async def verificar_e_abrir():
        try:
            async with BleakClient(device.address) as client:
                services = await client.get_services()
                tem_caracteristica_led = any(
                    BLE_CHARACTERISTIC_UUID.lower() == char.uuid.lower()
                    for service in services
                    for char in service.characteristics
                )

                if not tem_caracteristica_led:
                    messagebox.showwarning(
                        "Atenção",
                        "⚠️ Este dispositivo não possui a característica esperada para controle de LED.\n\nA interface pode não funcionar corretamente."
                    )

                top = ctk.CTkToplevel(parent)
                top.title(f"LED: {device.name or device.address}")
                LEDControlador(top, device.address, ConfiguracaoDispositivo())

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Erro ao conectar ao dispositivo:\n{str(e)}"
            )

        try:
            async with BleakClient(device.address) as client:
                services = await client.get_services()
                tem_caracteristica_led = any(
                    BLE_CHARACTERISTIC_UUID.lower() == char.uuid.lower()
                    for service in services
                    for char in service.characteristics
                )

                if not tem_caracteristica_led:
                    ctk.CTkMessagebox(
                        title="Atenção",
                        message="⚠️ Este dispositivo não possui a característica esperada para controle de LED.\n\nA interface pode não funcionar corretamente.",
                        icon="warning",
                        option_1="OK"
                    )

                top = ctk.CTkToplevel(parent)
                top.title(f"LED: {device.name or device.address}")
                LEDControlador(top, device.address, ConfiguracaoDispositivo())

        except Exception as e:
            ctk.CTkMessagebox(
                title="Erro",
                message=f"Erro ao conectar ao dispositivo:\n{str(e)}",
                icon="cancel",
                option_1="Fechar"
            )

    asyncio.run(verificar_e_abrir())


class LEDControlador:
    def __init__(self, root, address, config):
        self.root = root
        self.address = address
        self.config = config
        self.hue = 180
        self.sat = 800

        ctk.CTkLabel(root, text="Cor (roleta)").pack(pady=5)
        self.cor_btn = ctk.CTkButton(root, text="Escolher cor", command=self.selecionar_cor)
        self.cor_btn.pack()

        self.preview = ctk.CTkLabel(root, text=" ", width=140, height=25, corner_radius=8)
        self.preview.pack(pady=5)

        ctk.CTkLabel(root, text="Intensidade").pack()
        self.slider = ctk.CTkSlider(root, from_=0, to=1000, number_of_steps=1000, command=self.atualizar_intensidade)
        self.slider.set(self.sat)
        self.slider.pack(pady=5)

        ctk.CTkButton(root, text="Enviar", command=self.enviar).pack(pady=2)
        ctk.CTkButton(root, text="Ligar", command=lambda: self.comando_onoff(True)).pack(pady=2)
        ctk.CTkButton(root, text="Desligar", command=lambda: self.comando_onoff(False)).pack(pady=2)

        cor_padrao = self.config.get_default_color(address)
        if cor_padrao:
            self.hue = cor_padrao["h"]
            self.sat = cor_padrao["s"]
            self.slider.set(self.sat)
            asyncio.run(self.enviar())

    def atualizar_intensidade(self, val):
        self.sat = int(float(val))

    def selecionar_cor(self):
        cor_rgb, _ = colorchooser.askcolor()
        if cor_rgb:
            r, g, b = map(int, cor_rgb)
            self.hue, _ = rgb_to_hsb(r, g, b)
            self.preview.configure(bg_color=f"#{r:02x}{g:02x}{b:02x}")

    def comando_onoff(self, ligar):
        cmd = comando_on() if ligar else comando_off()
        asyncio.run(self._enviar_ble(cmd))

    def enviar(self):
        cmd = gerar_comando_hsb(self.hue, self.sat)
        asyncio.run(self._enviar_ble(cmd))

    async def _enviar_ble(self, comando):
        async with BleakClient(self.address) as client:
            await client.write_gatt_char(BLE_CHARACTERISTIC_UUID, comando)

import asyncio
import customtkinter as ctk
from bleak import BleakScanner
from ui_ledcontrol import open_led_control

BLE_CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

class BLEHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluetooth LED")
        self.devices = []
        self.selected_device = None

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.title = ctk.CTkLabel(self.frame, text="Dispositivos Bluetooth encontrados", font=("Arial", 16))
        self.title.pack(pady=(10, 5))

        self.listbox = ctk.CTkTextbox(self.frame, height=200, width=400)
        self.listbox.pack()

        self.scan_button = ctk.CTkButton(self.frame, text="🔍 Escanear", command=self.scan_devices)
        self.scan_button.pack(pady=10)

        self.select_label = ctk.CTkLabel(self.frame, text="Clique duas vezes para conectar e controlar", font=("Arial", 12))
        self.select_label.pack(pady=(5, 0))

        self.listbox.bind("<Double-1>", self.on_device_selected)

    def scan_devices(self):
        self.listbox.delete("0.0", "end")
        self.devices.clear()
        asyncio.run(self._scan_async())

    async def _scan_async(self):
        found = await BleakScanner.discover()
        for dev in found:
            self.devices.append(dev)
            self.listbox.insert("end", f"{dev.name or 'Desconhecido'} - {dev.address}\n")

    def on_device_selected(self, event):
        index = int(self.listbox.index("insert").split('.')[0]) - 1
        if 0 <= index < len(self.devices):
            device = self.devices[index]
            open_led_control(self.root, device)

        

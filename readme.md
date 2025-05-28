# Bluetooth LED Controller

Python application that allows you to control LED lights over Bluetooth Low Energy (BLE) with a modern and customizable GUI. Built with [customtkinter](https://github.com/TomSchimansky/CustomTkinter) and [bleak](https://github.com/hbldh/bleak), it supports features such as color picking, brightness adjustment, and saving a default color per device.

## 🧩 Features

- 🔍 Scans for nearby BLE devices
- ✅ Identifies devices that support LED control (via UUID `0000fff3-0000-1000-8000-00805f9b34fb`)
- 🎨 Color picker with hue + brightness slider
- 💡 On/Off switch for the LED
- 💾 Save a default color to apply on reconnection

## 📦 Requirements

- Python 3.8+
- [customtkinter](https://pypi.org/project/customtkinter/)
- [bleak](https://pypi.org/project/bleak/)

You can install dependencies using:

```bash
pip install -r requirements.txt

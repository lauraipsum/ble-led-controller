Aplicativo desktop simples para escanear dispositivos Bluetooth Low Energy (BLE) e controlar fitas LED compatíveis, incluindo seleção de cor via paleta, controle de intensidade e comandos de ligar/desligar. Também é possível salvar uma cor padrão para cada dispositivo.

## 🖼 Interface
A interface é construída com [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), com uma aparência moderna e escura por padrão.

## 🔧 Funcionalidades

- 🔍 Escanear dispositivos BLE próximos
- ✅ Identificar automaticamente dispositivos compatíveis com LED (característica `0000fff3-0000-1000-8000-00805f9b34fb`)
- 🎨 Selecionar cor via paleta de cores
- 🔆 Ajustar intensidade da luz (saturação)
- 💡 Ligar / Desligar o LED
- 💾 Salvar cor padrão que será aplicada automaticamente na próxima conexão

## 📦 Dependências

- Python 3.10+ recomendado
- `bleak`
- `customtkinter`
- `darkdetect`
- `packaging`

Instale as dependências com:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

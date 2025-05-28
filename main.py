import customtkinter as ctk
from ui_home import BLEHomeApp
import sys
import traceback

def excecao_handler(tipo, valor, tb):
    print("Exceção não tratada capturada:")
    traceback.print_exception(tipo, valor, tb)

sys.excepthook = excecao_handler

def run_app():
    try:
        ctk.set_appearance_mode("dark")  # ou "light"
        ctk.set_default_color_theme("blue")  # ou "green", "dark-blue"

        app = ctk.CTk()
        BLEHomeApp(app)
        app.mainloop()
    except Exception as e:
        print(" Erro fatal na aplicação:")
        traceback.print_exc()

if __name__ == "__main__":
    run_app()

import flet as ft
from login import login_view  # Importa la vista del login desde login.py

def main(page: ft.Page):
    # Llamamos a la función del login
    login_view(page)

# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)

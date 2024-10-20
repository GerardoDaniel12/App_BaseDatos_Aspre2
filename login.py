import flet as ft
import requests

# URL de tu back end Flask
BACKEND_URL = "http://127.0.0.1:5000"

# Variables para los campos de texto
email_field = ft.TextField(
    width=400,
    height=40,
    hint_text="Correo electrónico",
    border="underline",
    color="black",
    prefix_icon=ft.icons.EMAIL
)

password_field = ft.TextField(
    width=400,
    height=40,
    hint_text="Contraseña",
    border="underline",
    color="black",
    prefix_icon=ft.icons.LOCK,
    password=True
)

# Función para manejar el inicio de sesión
def on_login_click(e):
    email = email_field.value
    password = password_field.value
    
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/login", json=payload)
        result = response.json()
        if response.status_code == 200:
            print(f"Inicio de sesión exitoso para {email}")
            # Aquí puedes redirigir al usuario o actualizar la UI
        else:
            print(f"Error: {result.get('error')}")
    except Exception as ex:
        print(f"Error de conexión: {ex}")

# Función para manejar el registro
def on_signup_click(e):
    email = email_field.value
    password = password_field.value
    
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/signup", json=payload)
        result = response.json()
        if response.status_code == 201:
            print(f"Usuario registrado con éxito: {email}")
            # Aquí puedes redirigir al usuario o actualizar la UI
        else:
            print(f"Error: {result.get('error')}")
    except Exception as ex:
        print(f"Error de conexión: {ex}")

conteiner = ft.Container(
    ft.Column([
        ft.Container(
            ft.Text("Iniciar Sesión",
                    width=320,
                    size=30,
                    text_align="center",
                    weight="w900",
                    color=ft.colors.BLACK
                    ),
            padding=ft.padding.only(20, 20)
        ),
        ft.Container(
            email_field,  # Campo de correo electrónico
            padding=ft.padding.only(20, 20)
        ),
                
        ft.Container(
            password_field,  # Campo de contraseña
            padding=ft.padding.only(20, 20),
        ),

        ft.Row([
            ft.ElevatedButton(
                text="Iniciar Sesión",
                width=180,
                bgcolor="black",
                on_click=on_login_click  # Asocia la función al evento on_click
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        ),

    ],
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    horizontal_alignment="Center"
    ),
    border_radius=20,
    width=520,
    height=600,
    bgcolor=ft.colors.WHITE
)

def main(page: ft.Page):
    page.bgcolor = ft.colors.BLACK87
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window_height = 700
    page.window_width = 700
    
    # Centrar la ventana al iniciar
    page.window_center(),
    
    page.add(
        conteiner
    )

ft.app(target=main)


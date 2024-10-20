import flet as ft
from DB.ConexionUsuarios import login as firebase_login
from GuiInicial import main as gui_inicial_main

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
    
    # Usar la función de login de ConexionUsuarios
    success, result = firebase_login(email, password)
    if success:
        print(f"Inicio de sesión exitoso para {email}")
        e.page.clean()  # Limpia la página actual
        gui_inicial_main(e.page)  # Llama a la función main de GuiInicial.py
    else:
        print(f"Error: {result}")  # Imprime el error si el inicio de sesión falla

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
            email_field,
            padding=ft.padding.only(20, 20)
        ),
        ft.Container(
            password_field,
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
    page.window_width = 570
    
    # Centrar la ventana al iniciar
    page.window_center()
    
    # Agregar el contenedor de inicio de sesión
    page.add(conteiner)

# Asegúrate de que este sea el archivo que se ejecuta
ft.app(target=main)



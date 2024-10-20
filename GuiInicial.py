import flet as ft

def main(page: ft.Page):
    page.window_width = 1200
    page.window_height = 720
    page.window_resizable = False
    page.padding = 20
    page.bgcolor = ft.colors.WHITE38

    BotonesNavGui=ft.Container(
       
        width=100,
        border_radius=10,
        bgcolor=ft.colors.BLACK
    )


    OpcionesGui=ft.Container(
        BotonesNavGui,
        width=300,
        bgcolor=ft.colors.LIGHT_BLUE
    )

    InformacionGui=ft.Container(
        content=ft.Text("Informacion"),
        expand=True,
        bgcolor=ft.colors.LIGHT_GREEN,
        padding=10,
    )

    



    container = ft.Container(
        ft.Row([
            ft.Column([
                ft.ElevatedButton(
                    text=("Hola columna 2")
                ), 
                ft.ElevatedButton(
                    text=("Hola Colm")
                )               
            ]),
            ft.Column([
                ft.Text("Informacion")
            ])
        ])




             
    )



    page.add(container)

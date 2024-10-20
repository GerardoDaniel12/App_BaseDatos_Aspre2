import flet as ft

def ButtomExtintoresMostrador(e, page):
    page.navigate("NavIzq/ExtintoresMostrador") 
    
def main(page: ft.Page):
    page.window.width = 1200
    page.window.height = 720
    page.window.resizable = False
    page.padding = 20
    page.bgcolor = ft.colors.WHITE38
    page.window_center


      


    container = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column([
                    ft.ElevatedButton(
                        text="Hola columna 1",
                        on_click=lambda e: ButtomExtintoresMostrador(e, page)  # Pasar `page`
                    ), 
                    ft.ElevatedButton(
                        text=("Hola Colm"),
                    )               
                ]),
                border=ft.border.all(color=ft.colors.BLACK),
                width=250,
                padding=10
                ),
            ft.Container(
                ft.Column([
                    ft.Text("Informacion")
                ]),
                border=ft.border.all(color=ft.colors.BLACK),
                padding=10,
                expand=True,
            )

        ])




             
    )



    page.add(container)
ft.app(target=main)

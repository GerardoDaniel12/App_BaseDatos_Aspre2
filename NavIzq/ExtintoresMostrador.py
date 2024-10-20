import flet as ft
def main(page: ft.Page):
    page.window_width=1200
    page.window_height=720
    page.window_resizable = False
    page.padding = 20
    page.bgcolor = ft.colors.WHITE38
    page.window_center
    
    
    
    page.add()

ft.app(target=main)
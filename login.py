import customtkinter as ctk
from tkinter import messagebox
from DB.ConexionUsuarios import login  # Importa el módulo de autenticación
from GuiInicial import crear_gui_inicial  # Importa la función para crear la GUI principal

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aspre Consultores - Inicio de Sesión")
        self.geometry("400x350")
        self.resizable(False, False)
        
        # Tema de color y apariencia
        ctk.set_appearance_mode("System")  # Cambia entre "System", "Light" y "Dark"
        ctk.set_default_color_theme("blue")

        # Configuración del frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        # Título
        self.title_label = ctk.CTkLabel(self.main_frame, text="Bienvenido", font=("Segoe UI", 20, "bold"))
        self.title_label.pack(pady=(20, 10))

        # Subtítulo
        self.subtitle_label = ctk.CTkLabel(self.main_frame, text="Por favor, inicia sesión", font=("Segoe UI", 14))
        self.subtitle_label.pack(pady=(0, 20))

        # Campo de usuario
        self.user_input = ctk.CTkEntry(self.main_frame, placeholder_text="Usuario", width=260)
        self.user_input.pack(pady=(5, 10))

        # Campo de contraseña
        self.pass_input = ctk.CTkEntry(self.main_frame, placeholder_text="Contraseña", show="*", width=260)
        self.pass_input.pack(pady=(5, 20))

        # Botón de inicio de sesión
        self.login_button = ctk.CTkButton(self.main_frame, text="Iniciar Sesión", command=self.check_login, width=200)
        self.login_button.pack(pady=(10, 20))

        # Opción de alternar tema
        self.switch_theme = ctk.CTkSwitch(self.main_frame, text="Modo oscuro", command=self.toggle_theme)
        self.switch_theme.pack(pady=(10, 10))

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current_mode == "dark" else "dark")

    def check_login(self):
        username = self.user_input.get()
        password = self.pass_input.get()
        success, user_or_error = login(username, password)

        if success:
            self.open_main_window()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def open_main_window(self):
        self.withdraw()  # Oculta la ventana de login
        crear_gui_inicial(self)  # Llama a la función para crear la GUI principal

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()

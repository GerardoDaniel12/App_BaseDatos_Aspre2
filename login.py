import customtkinter as ctk
from tkinter import messagebox
from DB.ConexionUsuarios import login  # Importa el módulo de autenticación
from GuiInicial import crear_gui_inicial  # Importa la función para crear la GUI principal

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aspre Consultores")
        self.geometry("400x300")
        ctk.set_appearance_mode("light")  # Puedes cambiar a "dark" para un tema oscuro
        ctk.set_default_color_theme("blue")

        # Configuración del frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        self.title_label = ctk.CTkLabel(self.main_frame, text="Inicio de Sesión", font=("Segoe UI", 18, "bold"))
        self.title_label.pack(pady=(10, 15))

        # Campo de usuario
        self.user_label = ctk.CTkLabel(self.main_frame, text="Usuario:", font=("Segoe UI", 12))
        self.user_label.pack(anchor="w", padx=10)
        self.user_input = ctk.CTkEntry(self.main_frame, placeholder_text="Ingresa tu usuario", width=300)
        self.user_input.pack(pady=(5, 15))

        # Campo de contraseña
        self.pass_label = ctk.CTkLabel(self.main_frame, text="Contraseña:", font=("Segoe UI", 12))
        self.pass_label.pack(anchor="w", padx=10)
        self.pass_input = ctk.CTkEntry(self.main_frame, placeholder_text="Ingresa tu contraseña", show="*", width=300)
        self.pass_input.pack(pady=(5, 15))

        # Botón de inicio de sesión
        self.login_button = ctk.CTkButton(self.main_frame, text="Iniciar Sesión", command=self.check_login, width=200)
        self.login_button.pack(pady=20)

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

import customtkinter as ctk
from tkinter import messagebox
from DB.ConexionUsuarios import login  # Importa el módulo de autenticación
from GuiInicial import GuiInicial  # Importa la función para crear la GUI principal
from GuiInicialNoAdmin import GuiInicialNoAdmin

# Configuración inicial de tema
ctk.set_appearance_mode("System")  # Alterna entre "System", "Light" y "Dark"
ctk.set_default_color_theme("blue")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aspre Consultores - Inicio de Sesión")
        self.geometry("420x500")
        self.resizable(False, False)

        # Frame principal estilizado
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#34495e")
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        width = 400
        height = 500

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Aplica las dimensiones y la posición calculada
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Título y subtítulo
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Aspre Consultores", 
            font=("Segoe UI", 26, "bold"), 
            text_color="#ecf0f1"
        )
        self.title_label.pack(pady=(20, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame, 
            text="Inicio de Sesión", 
            font=("Segoe UI", 16), 
            text_color="#bdc3c7"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Campo de usuario
        self.user_input = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Usuario", 
            width=300, 
            font=("Segoe UI", 14), 
            corner_radius=10, 
            fg_color="#2c3e50", 
            text_color="#ecf0f1"
        )
        self.user_input.pack(pady=(10, 10))

        # Campo de contraseña
        self.pass_input = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Contraseña", 
            show="*", 
            width=300, 
            font=("Segoe UI", 14), 
            corner_radius=10, 
            fg_color="#2c3e50", 
            text_color="#ecf0f1"
        )
        self.pass_input.pack(pady=(10, 20))

        # Botón de inicio de sesión
        self.login_button = ctk.CTkButton(
            self.main_frame, 
            text="Iniciar Sesión", 
            command=self.check_login, 
            width=250, 
            height=40, 
            font=("Segoe UI", 14, "bold"), 
            fg_color="#2980b9", 
            hover_color="#3498db", 
            corner_radius=15
        )
        self.login_button.pack(pady=(20, 30))

        # Interruptor de tema
        self.switch_theme = ctk.CTkSwitch(
            self.main_frame, 
            text="Modo oscuro", 
            command=self.toggle_theme, 
            font=("Segoe UI", 12), 
            fg_color="#95a5a6"
        )
        self.switch_theme.pack(pady=(10, 10))

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current_mode == "Dark" else "Dark")

    def check_login(self):
        username = self.user_input.get()
        password = self.pass_input.get()
        success, user_or_error = login(username, password)
        print(user_or_error)  # Imprime todo lo que llega desde la función login

        if success:
            user_data = user_or_error['user']  # Accede a la clave 'user'
            print(user_data)  # Imprime los datos del usuario para depuración
            self.open_main_window(user_data)  # Pasa los datos del usuario aquí
        else:
            messagebox.showerror("Error", f"Usuario o contraseña incorrectos: {user_or_error}")

    def open_main_window(self, user_data):
        empresa = user_data.get('empresa', 'Default')  # Usa 'Default' si no se encuentra la empresa
        privilegio = user_data.get('privilegio', 'usuario')  # Usa 'usuario' si no se encuentra privilegio
        self.withdraw()  # Oculta la ventana de login
        if privilegio == "admin":
            GuiInicial(user_data, privilegio, empresa).mainloop()  # Pasa la empresa correctamente
        else:
            GuiInicialNoAdmin(user_data, privilegio, empresa).mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
    app.mainloop()


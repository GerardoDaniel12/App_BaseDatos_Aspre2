import customtkinter as ctk
from tkinter import ttk, messagebox
from DB.ConexionExtintores import crear_conexion, obtener_extintores
import mysql.connector

# Configuración para el tema del sistema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class GuiInicial(ctk.CTk):
    def __init__(self, user_data, privilegio):
        super().__init__()
        self.user_data = user_data  # Aquí almacenas los datos del usuario
        self.privilegio = privilegio
        self.title("Interfaz Principal")
        self.geometry("800x600")
        self.initialize_widgets()

    def initialize_widgets(self):
       

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2B2B2B" if ctk.get_appearance_mode() == "Dark" else "#F0F0F0")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(main_frame, text="Bienvenido a Aspre Consultores", font=("Arial", 26, "bold"), text_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#333333")
        title_label.pack(pady=(10, 20))

        nav_frame = ctk.CTkFrame(main_frame, width=200, corner_radius=15, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9")
        nav_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)

        ctk.CTkLabel(nav_frame, text="Navegación", font=("Arial", 16, "bold"), text_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#333333").pack(pady=(20, 10))

        extintores_button = ctk.CTkButton(nav_frame, text="Extintores Inspeccionados", command=self.mostrar_extintores, width=180, fg_color="#4B8BBE")
        extintores_button.pack(pady=10)

        personal_info_button = ctk.CTkButton(nav_frame, text="Información Personal", command=self.mostrar_info_personal, width=180, fg_color="#5BC0DE")
        personal_info_button.pack(pady=10)

        logout_button = ctk.CTkButton(nav_frame, text="Cerrar Sesión", command=self.cerrar_sesion, fg_color="#d9534f", hover_color="#c9302c", width=180)
        logout_button.pack(pady=20)

        self.extintores_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#4D4D4D" if ctk.get_appearance_mode() == "Dark" else "#FFFFFF")
        self.extintores_frame.pack(fill="both", expand=True, padx=(0, 20), pady=10)
        self.extintores_frame.pack_forget()  # Ocultar inicialmente

        self.tree = None

    def mostrar_extintores(self):
        self.extintores_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4B8BBE", foreground="black")
        style.map("Treeview", background=[("selected", "#4B8BBE")])

        self.tree = ttk.Treeview(self.extintores_frame, columns=("id", "Referencia", "Fecha realizado", "Planta", "Area", "Numero de extintor",
            "Ubicacion de extintor", "Tipo", "Capacidad en kg", "Fecha de fabricacion", "Fecha de recarga", 
            "Fecha de vencimiento", "Fecha ultima de prueba hidrostatica", "Presion", "Manometro", "Seguro", 
            "Etiquetas", "Señalamiento", "Circulo y numero", "Pintura", "Manguera", "Boquilla", 
            "Golpes o daños", "Obstruido","Comentarios"), show='headings', style="Treeview")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        v_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.tree.pack(side="top", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Llenado de datos
        try:
            conn = crear_conexion()
            if conn:
                extintores = obtener_extintores(conn)

                for item in self.tree.get_children():
                    self.tree.delete(item)

                for extintor in extintores:
                    self.tree.insert("", "end", values=extintor)

                conn.close()

        except mysql.connector.Error as db_err:
            messagebox.showerror("Error de base de datos", f"No se pudo obtener la información: {str(db_err)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

        if self.privilegio == "admin":
            editar_button = ctk.CTkButton(self.extintores_frame, text="Editar Extintor", command=self.editar_extintor, width=180, fg_color="#4BBE4B")
            editar_button.pack(pady=10)

    def mostrar_info_personal(self):
        messagebox.showinfo("Información Personal", f"Correo: {self.user_data['correo']}")

    def editar_extintor(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            edit_window = ctk.CTkToplevel(self)
            edit_window.title("Editar Extintor")
            edit_window.geometry("400x300")

            ctk.CTkLabel(edit_window, text="Referencia:").pack(pady=5)
            ref_entry = ctk.CTkEntry(edit_window)
            ref_entry.insert(0, item_values[1])  # Insertar valor actual
            ref_entry.pack(pady=5)

            def guardar_cambios():
                nuevo_valor = ref_entry.get()
                try:
                    conn = crear_conexion()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE extintores SET referencia=%s WHERE id=%s", (nuevo_valor, item_values[0]))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Éxito", "Extintor actualizado correctamente")
                    edit_window.destroy()
                    self.mostrar_extintores()  # Refrescar la tabla
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el extintor: {str(e)}")

            save_button = ctk.CTkButton(edit_window, text="Guardar Cambios", command=guardar_cambios)
            save_button.pack(pady=20)
        else:
            messagebox.showwarning("Seleccionar Extintor", "Por favor, selecciona un extintor para editar.")

    def cerrar_sesion(self):
        self.extintores_frame.pack_forget()
        self.destroy()  # Cierra la ventana actual
        if hasattr(self, 'login_window'):
            self.login_window.deiconify()  # Muestra la ventana de inicio de sesión si existe

    def login(self):
        # Después de que el usuario inicia sesión correctamente
        user_data = {'correo': 'usuario@example.com'}  # Datos de ejemplo
        privilegio = "admin"  # Privilegios de ejemplo
        self.withdraw()  # Oculta la ventana de inicio de sesión
        self.gui_inicial = GuiInicial(user_data, privilegio)  # Pasa datos de usuario
        self.gui_inicial.login_window = self  # Asigna la ventana de inicio de sesión
        self.gui_inicial.mainloop()  # Muestra la ventana principal


if __name__ == "__main__":
    app = GuiInicial({'correo': 'DanielLopez@gmail.com'}, "admin")  # Aquí puedes pasar la ventana de login si corresponde
    app.mainloop()

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
        self.user_data = user_data
        self.privilegio = privilegio
        self.title("Interfaz Principal")
        self.geometry("800x600")
        self.orden_ascendente = True  # Variable para alternar entre ascendente y descendente
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

        asc_button = ctk.CTkButton(self.extintores_frame, text="Orden Ascendente", command=lambda: self.ordenar_referencia(ascendente=True))
        asc_button.pack(side="left", padx=5, pady=10)

        desc_button = ctk.CTkButton(self.extintores_frame, text="Orden Descendente", command=lambda: self.ordenar_referencia(ascendente=False))
        desc_button.pack(side="left", padx=5, pady=10)

        self.cargar_datos_extintores()

        if self.privilegio == "admin":
            editar_button = ctk.CTkButton(self.extintores_frame, text="Editar Extintor", command=self.editar_extintor, width=180, fg_color="#4BBE4B")
            editar_button.pack(pady=10)

    def cargar_datos_extintores(self):
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

    def ordenar_referencia(self, ascendente=True):
        datos = [(self.tree.set(k, "Referencia"), k) for k in self.tree.get_children("")]
        datos.sort(reverse=not ascendente)

        for index, (val, k) in enumerate(datos):
            self.tree.move(k, "", index)

    def mostrar_info_personal(self):
        # Limpiar todos los widgets en extintores_frame antes de mostrar la información personal
        for widget in self.extintores_frame.winfo_children():
            widget.pack_forget()  # Oculta todos los widgets

        # Crear un nuevo frame para mostrar la información personal
        info_frame = ctk.CTkFrame(self.extintores_frame, corner_radius=15, fg_color="#4D4D4D" if ctk.get_appearance_mode() == "Dark" else "#FFFFFF")
        info_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Mostrar el correo
        correo_label = ctk.CTkLabel(info_frame, text=f"Usuario: {self.user_data['correo']}", font=("Arial", 14))
        correo_label.pack(pady=(10, 5))

        # Mostrar el privilegio
        privilegio_label = ctk.CTkLabel(info_frame, text=f"Privilegio: {self.privilegio}", font=("Arial", 14))
        privilegio_label.pack(pady=(0, 10))

        # Aquí puedes agregar código para mostrar una imagen, si la deseas
        # Asegúrate de tener una imagen disponible y la ruta correcta


    def cerrar_sesion(self):
        self.destroy()

    def editar_extintor(self):
        # Obtener el ítem seleccionado en la tabla
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleccionar Extintor", "Por favor, selecciona un extintor para editar.")
            return

        # Obtener los valores del extintor seleccionado
        item_id = selected_item[0]
        extintor_data = self.tree.item(item_id)["values"]

        # Crear una nueva ventana para editar los datos del extintor
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Extintor")
        edit_window.geometry("400x400")

        # Crear un frame desplazable
        scrollable_frame = ctk.CTkScrollableFrame(edit_window)
        scrollable_frame.pack(fill="both", expand=True)

        # Crear campos de entrada para cada dato del extintor
        labels = [
            "Id", "Referencia", "Fecha realizado", "Planta", "Area",
            "Numero de extintor", "Ubicacion de extintor", "Tipo",
            "Capacidad en kg", "Fecha de fabricacion", "Fecha de recarga",
            "Fecha de vencimiento", "Fecha ultima de prueba hidrostatica",
            "Presion", "Manometro", "Seguro", "Etiquetas",
            "Señalamiento", "Circulo y numero", "Pintura",
            "Manguera", "Boquilla", "Golpes o daños", "Obstruido", "Comentarios"
        ]

        entries = []

        for label, value in zip(labels, extintor_data):
            # Crear un campo de entrada
            row_frame = ctk.CTkFrame(scrollable_frame)
            row_frame.pack(pady=5)

            ctk.CTkLabel(row_frame, text=label).pack(side="left", padx=5)
            entry = ctk.CTkEntry(row_frame, width=250)
            entry.insert(0, value)
            entry.pack(side="left", padx=5)
            entries.append(entry)

        # Botón para guardar cambios
        def guardar_cambios():
            # Obtener los nuevos valores
            new_values = [entry.get() for entry in entries]
            # Aquí deberías actualizar el extintor en la base de datos
            # utilizando el item_id y los nuevos valores
            # Por ejemplo, puedes hacer una función de actualización que maneje esto
            # update_extintor(item_id, new_values)

            # Actualizar la tabla
            self.tree.item(item_id, values=new_values)
            edit_window.destroy()

        save_button = ctk.CTkButton(scrollable_frame, text="Guardar Cambios", command=guardar_cambios)
        save_button.pack(pady=10)

        edit_window.transient(self)  # Establece la ventana de edición como modal
        edit_window.grab_set()  # Desactiva la ventana principal mientras está abierta


if __name__ == "__main__":
    app = GuiInicial({'correo': 'DanielLopez@gmail.com'}, "admin")
    app.mainloop()


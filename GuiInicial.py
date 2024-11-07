import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import ttk, messagebox, filedialog  
from DB.ConexionExtintores import crear_conexion, obtener_extintores
from DB.ConexionUsuarios import obtener_imagen, actualizar_usuario
import mysql.connector
from PIL import Image, ImageTk, ImageDraw
import io

# Configuración para el tema del sistema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class GuiInicial(ctk.CTk):
    def __init__(self, user_data, privilegio):
        super().__init__()
        self.user_data = user_data
        self.privilegio = privilegio
        self.title("Interfaz Principal")
        self.after(1, lambda: self.state('zoomed'))

        self.orden_ascendente = True  # Variable para alternar entre ascendente y descendente
        self.initialize_widgets()

    def initialize_widgets(self):
        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="#2B2B2B" if ctk.get_appearance_mode() == "Dark" else "#F0F0F0")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Frame de navegación a la izquierda
        nav_frame = ctk.CTkFrame(main_frame, width=200, corner_radius=15, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9")
        nav_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)


        # Etiqueta de "Navegación" debajo de la imagen
        ctk.CTkLabel(nav_frame, text="Navegación", font=("Arial", 16, "bold"), text_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#333333").pack(pady=(10, 10))

        # Botones de navegación
        extintores_button = ctk.CTkButton(nav_frame, text="Extintores Inspeccionados", command=self.mostrar_extintores, width=180, fg_color="#4B8BBE", height=35)
        extintores_button.pack(pady=10)

        personal_info_button = ctk.CTkButton(nav_frame, text="Información Personal", command=self.mostrar_info_personal, width=180, fg_color="#4B8BBE", height=35)
        personal_info_button.pack(pady=10)

        logout_button = ctk.CTkButton(nav_frame, text="Cerrar Sesión", command=self.cerrar_sesion, fg_color="#d9534f", hover_color="#c9302c", width=180)
        logout_button.pack(pady=20)

        # Frame de contenido principal para la tabla de extintores
        self.extintores_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#4D4D4D" if ctk.get_appearance_mode() == "Dark" else "#FFFFFF")
        self.extintores_frame.pack(fill="both", expand=True, padx=(0, 20), pady=10)

        self.tree = None
        
    def mostrar_extintores(self):
        # Configuración del frame de extintores
        self.extintores_frame.pack(fill="both", expand=True)
        for widget in self.extintores_frame.winfo_children():
            widget.pack_forget()  # Oculta todos los widgets actuales en el frame
        
        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))


        # Estilo para la tabla de extintores
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25, 
                        background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), 
                        background="#4B8BBE", foreground="black")
        style.map("Treeview", background=[("selected", "#4B8BBE")])

        # Frame para botones de orden y edición
        botones_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        botones_frame.pack(fill="x", pady=(5, 10))

        filtro_fecha_label = ctk.CTkLabel(filtros_frame, text="Filtro por Fecha Realizado", font=("Arial", 17, "bold"))
        filtro_fecha_label.pack(side="top", anchor="w", padx=55)

        # Filtro para año
        self.año_filtro = ttk.Combobox(botones_frame, values=[], state="readonly")
        self.año_filtro.bind("<<ComboboxSelected>>", self.filtrar_por_fecha)
        self.año_filtro.pack(side="left", padx=5)

        # Filtro para mes
        self.mes_filtro = ttk.Combobox(botones_frame, values=[], state="readonly")
        self.mes_filtro.bind("<<ComboboxSelected>>", self.filtrar_por_fecha)
        self.mes_filtro.pack(side="left", padx=5)

        # Botón de orden ascendente
        asc_button = ctk.CTkButton(botones_frame, text="Ascendente (Referencia)", 
                                    command=lambda: self.ordenar_referencia(ascendente=True), width=120)
        asc_button.pack(side="left", padx=5)

        # Botón de orden descendente
        desc_button = ctk.CTkButton(botones_frame, text="Descendente (Referencia)", 
                                    command=lambda: self.ordenar_referencia(ascendente=False), width=120)
        desc_button.pack(side="left", padx=5)

        # Botón de edición para administradores
        if self.privilegio == "admin":
            editar_button = ctk.CTkButton(botones_frame, text="Editar Extintor", 
                                        command=self.editar_extintor, fg_color="#4BBE4B", width=120)
            editar_button.pack(side="left", padx=5)

        # Configuración de la tabla de extintores
        columnas = ("id", "Referencia", "Fecha realizado", "Planta", "Area", "Numero de extintor",
                    "Ubicacion de extintor", "Tipo", "Capacidad en kg", "Fecha de fabricacion", 
                    "Fecha de recarga", "Fecha de vencimiento", "Fecha ultima de prueba hidrostatica", 
                    "Presion", "Manometro", "Seguro", "Etiquetas", "Señalamiento", 
                    "Circulo y numero", "Pintura", "Manguera", "Boquilla", 
                    "Golpes o daños", "Obstruido", "Comentarios")

        self.tree = ttk.Treeview(self.extintores_frame, columns=columnas, 
                                show='headings', style="Treeview")

        # Configuración de encabezados y ancho de columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # Añadir barras de desplazamiento
        v_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        # Empaquetado de tabla y scrollbars
        self.tree.pack(side="top", fill="both", expand=True, pady=(5, 5))
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Cargar datos en la tabla
        self.cargar_datos_extintores()

    def cargar_datos_extintores(self):
        try:
            conn = crear_conexion()
            if conn:
                extintores = obtener_extintores(conn)

                # Obtener años y meses únicos
                años = sorted(set(extintor[2].year for extintor in extintores))  # Asumiendo que "fecha_realizado" es el tercer elemento
                meses = sorted(set(extintor[2].month for extintor in extintores))

                años.insert(0, "Todos")
                meses.insert(0, "Todos")

                self.año_filtro['values'] = años
                self.mes_filtro['values'] = meses

                for item in self.tree.get_children():
                    self.tree.delete(item)

                for extintor in extintores:
                    self.tree.insert("", "end", values=extintor)

                conn.close()

        except mysql.connector.Error as db_err:
            messagebox.showerror("Error de base de datos", f"No se pudo obtener la información: {str(db_err)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def filtrar_por_fecha(self, event):
        selected_year = self.año_filtro.get()
        selected_month = self.mes_filtro.get()

        # Filtrar la tabla según el año y mes seleccionados
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = crear_conexion()
        if conn:
            extintores = obtener_extintores(conn)  # Obtén todos los extintores de nuevo
            for extintor in extintores:
                fecha_realizado = extintor[2]  # Asumiendo que "fecha_realizado" es el tercer elemento
                year_match = (selected_year == "Todos" or str(fecha_realizado.year) == selected_year)
                month_match = (selected_month == "Todos" or str(fecha_realizado.month) == selected_month)
                if year_match and month_match:
                    self.tree.insert("", "end", values=extintor)

            conn.close()

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

        # Mostrar empresa
        if 'empresa' in self.user_data:
            empresa_label = ctk.CTkLabel(info_frame, text=f"{self.user_data['empresa']}", font=("ADLaM Display", 60), fg_color="#887CE9", width=1000, height=100, corner_radius=20)
            empresa_label.pack(pady=(0, 10))

        # Mostrar el correo
        correo_label = ctk.CTkLabel(info_frame, text=f"Correo: {self.user_data['correo']}", font=("Arial", 25), width=1000,height=25,anchor="w")
        correo_label.pack(pady=(10, 5))

        # Mostrar el privilegio
        privilegio_label = ctk.CTkLabel(info_frame, text=f"Privilegio: {self.privilegio}", font=("Arial", 25), width=1000,anchor="w")
        privilegio_label.pack(pady=(0, 10))

        # Botón para editar la información personal
        editar_button = ctk.CTkButton(info_frame, text="Editar Información", command=self.editar_info_personal, fg_color="#4BBE4B")
        editar_button.pack(pady=(0, 10))

        # Botón para cerrar la vista de información personal
        cerrar_button = ctk.CTkButton(info_frame, text="Cerrar", command=lambda: self.extintores_frame.pack_forget())
        cerrar_button.pack(pady=(0, 10))

    def editar_info_personal(self):
        # Crear ventana para editar información personal con tamaño y diseño mejorado
        self.editar_ventana = ctk.CTkToplevel(self)
        self.editar_ventana.title("Editar Información")
        self.editar_ventana.geometry("400x400")  # Aumentar tamaño de la ventana
        self.editar_ventana.resizable(False, False)
   
        # Hacer que la ventana sea modal para que quede en primer plano
        self.editar_ventana.grab_set()
        self.editar_ventana.focus_set()

        # Título de la ventana de edición
        titulo_label = ctk.CTkLabel(self.editar_ventana, text="Editar Información Personal", font=("Arial", 16, "bold"))
        titulo_label.pack(pady=(10, 15))

        # Campo de correo
        email_label = ctk.CTkLabel(self.editar_ventana, text="Nuevo correo:")
        email_label.pack(anchor="w", padx=20)
        self.email_entry = ctk.CTkEntry(self.editar_ventana, width=300, placeholder_text="Introduce el nuevo correo")
        self.email_entry.pack(pady=(5, 10))

        # Campo de nueva contraseña
        password_label = ctk.CTkLabel(self.editar_ventana, text="Nueva contraseña:")
        password_label.pack(anchor="w", padx=20)
        self.password_entry = ctk.CTkEntry(self.editar_ventana, width=300, show="*", placeholder_text="Introduce la nueva contraseña")
        self.password_entry.pack(pady=(5, 10))

        # Campo de empresa
        empresa_label = ctk.CTkLabel(self.editar_ventana, text="Empresa:")
        empresa_label.pack(anchor="w", padx=20)
        self.empresa_entry = ctk.CTkEntry(self.editar_ventana, width=300, placeholder_text="Introduce el nombre de la empresa")
        self.empresa_entry.pack(pady=(5, 10))

        # Botón para seleccionar una nueva imagen
        self.btn_imagen = ctk.CTkButton(self.editar_ventana, text="Seleccionar imagen", command=self.seleccionar_imagen)
        self.btn_imagen.pack(pady=(10, 20))

        # Botón para guardar cambios
        self.btn_guardar = ctk.CTkButton(self.editar_ventana, text="Guardar cambios", command=self.guardar_cambios, width=150)
        self.btn_guardar.pack(pady=10)
    
    def seleccionar_imagen(self):
        # Seleccionar imagen desde el sistema de archivos
        self.imagen_path = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    def guardar_cambios(self):
        # Obtener datos del formulario
        nuevo_email = self.email_entry.get() or None
        nueva_password = self.password_entry.get() or None
        nueva_empresa = self.empresa_entry.get() or None
        nueva_imagen = getattr(self, 'imagen_path', None)
        
        # Actualizar datos en la base de datos
        success, mensaje = actualizar_usuario(
            user_id=self.user_data['id'],
            email=nuevo_email,
            password=nueva_password,
            empresa=nueva_empresa,
            imagen_path=nueva_imagen
        )
        
        # Mensaje de confirmación
        if success:
            messagebox.showinfo("Éxito", mensaje)
            self.editar_ventana.destroy()  # Cerrar la ventana de edición
        else:
            messagebox.showerror("Error", mensaje)

    def cerrar_sesion(self):
        self.destroy()
        
# Método para actualizar extintores con la conexión existente
    def update_extintor(self, item_id, new_values):
        try:
            # Crear la conexión a la base de datos desde el módulo existente
            conn = crear_conexion()
            if conn is None:
                raise Exception("No se pudo establecer conexión con la base de datos.")

            cursor = conn.cursor()

            # Definir la consulta de actualización SQL
            update_query = """
                UPDATE formulario_inspeccion SET 
                    id_Extintores = %s, fecha_realizado = %s, planta = %s, area = %s,
                    numero_extintor = %s, ubicacion_extintor = %s, tipo = %s,
                    capacidad_kg = %s, fecha_fabricacion = %s, fecha_recarga = %s,
                    fecha_vencimiento = %s, fecha_ultima_prueba = %s,
                    presion = %s, manometro = %s, seguro = %s, etiquetas = %s,
                    senalamientos = %s, circulo_numero = %s, pintura = %s,
                    manguera = %s, boquilla = %s, golpes_danos = %s,
                    obstruido = %s, comentarios = %s
                WHERE id = %s
            """

            # Ejecutar la consulta con los valores actualizados
            cursor.execute(update_query, new_values[1:] + [new_values[0]])  # Excluye el campo "Id" como en tu tabla

            # Confirmar los cambios
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Extintor actualizado correctamente en la base de datos.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al actualizar en la base de datos: {error}")
        except Exception as e:
            messagebox.showerror("Error", f"{str(e)}")
        
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

            # Actualizar en la base de datos
            self.update_extintor (item_id, new_values)

            # Actualizar la tabla en la interfaz
            self.tree.item(item_id, values=new_values)
            edit_window.destroy()

        save_button = ctk.CTkButton(scrollable_frame, text="Guardar Cambios", command=guardar_cambios)
        save_button.pack(pady=10)

        edit_window.transient(self)
        edit_window.grab_set()


if __name__ == "__main__":
    app = GuiInicial({'correo': 'DanielLopez@gmail.com', "empresa": "Aspre Consultores"}, "admin")
    app.mainloop()


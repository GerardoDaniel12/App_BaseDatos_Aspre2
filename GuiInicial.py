import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import ttk, messagebox, filedialog  
from DB.ConexionExtintores import obtener_extintores_api  # Importa la función para crear la conexión
import mysql.connector
from PIL import Image, ImageTk, ImageDraw
import io
import pymysql.cursors
import pandas as pd
import openpyxl
from tkinter import filedialog


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
        self.año_filtro = None
        self.mes_filtro = None
        self.tree = None
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


        # Filtro para año
        self.año_filtro = ttk.Combobox(botones_frame, values=[], state="readonly")
        self.año_filtro.bind("<<ComboboxSelected>>", self.filtrar_por_fecha)
        self.año_filtro.pack(side="left", padx=5)

        # Filtro para mes
        self.mes_filtro = ttk.Combobox(botones_frame, values=[], state="readonly")
        self.mes_filtro.bind("<<ComboboxSelected>>", self.filtrar_por_fecha)
        self.mes_filtro.pack(side="left", padx=5)

        # Botón para exportar a Excel, añadido en filtros_frame
        export_button = ctk.CTkButton(filtros_frame, text="Exportar a Excel", command=self.exportar_a_excel)
        export_button.pack(side="right", anchor="w", padx=10)

        filtro_fecha_label = ctk.CTkLabel(filtros_frame, text="Filtro por Fecha Realizado", font=("Arial", 17, "bold"))
        filtro_fecha_label.pack(side="top", anchor="w", padx=55)
      
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

# Modificar cargar_datos_extintores para usar obtener_extintores_api
def cargar_datos_extintores(self):
    # Obtiene los datos desde la API
    try:
        datos_extintores = obtener_extintores_api()  # Llama a la función de conexión a la API
        if not datos_extintores:
            messagebox.showwarning("Advertencia", "No se encontraron datos de extintores.")
            return

        # Limpia la tabla antes de cargar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Rellena la tabla con los datos obtenidos de la API
        for extintor in datos_extintores:
            # Asegúrate de que las claves en extintor coincidan con las columnas de tu tabla
            self.tree.insert("", "end", values=(
                extintor.get("id", ""),
                extintor.get("referencia", ""),
                extintor.get("fecha_realizado", ""),
                extintor.get("planta", ""),
                extintor.get("area", ""),
                extintor.get("numero_extintor", ""),
                extintor.get("ubicacion", ""),
                extintor.get("tipo", ""),
                extintor.get("capacidad", ""),
                extintor.get("fecha_fabricacion", ""),
                extintor.get("fecha_recarga", ""),
                extintor.get("fecha_vencimiento", ""),
                extintor.get("fecha_prueba_hidrostatica", ""),
                extintor.get("presion", ""),
                extintor.get("manometro", ""),
                extintor.get("seguro", ""),
                extintor.get("etiquetas", ""),
                extintor.get("senalamiento", ""),
                extintor.get("circulo_numero", ""),
                extintor.get("pintura", ""),
                extintor.get("manguera", ""),
                extintor.get("boquilla", ""),
                extintor.get("golpes_danos", ""),
                extintor.get("obstruido", ""),
                extintor.get("comentarios", "")
            ))
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def filtrar_por_fecha(self, event=None):
        selected_year = self.año_filtro.get()  # Año seleccionado
        selected_month = self.mes_filtro.get()  # Mes seleccionado

        # Limpiar la tabla antes de aplicar los filtros
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Establecer la conexión con la base de datos
        conn = crear_conexion()
        if conn:
            # Consulta base que siempre devuelve todas las filas
            query = "SELECT * FROM formulario_inspeccion WHERE 1=1"
            parametros = []

            # Filtrar por la empresa si no es admin
            if self.privilegio != "admin":
                empresa_filtro = self.user_data['empresa']
                query += " AND empresa = %s"
                parametros.append(empresa_filtro)
                print(f"Filtrando por empresa: {empresa_filtro}")  # Mostrar empresa en la salida

            # Verificar si el año es distinto de "Todos" y agregarlo a la consulta
            if selected_year != "Todos":
                query += " AND YEAR(fecha_realizado) = %s"
                parametros.append(selected_year)
                print(f"Filtrando por año: {selected_year}")  # Mostrar año en la salida

            # Verificar si el mes es distinto de "Todos" y agregarlo a la consulta
            if selected_month != "Todos":
                query += " AND MONTH(fecha_realizado) = %s"
                parametros.append(selected_month)
                print(f"Filtrando por mes: {selected_month}")  # Mostrar mes en la salida

            # Imprimir la consulta generada para depuración
            print(f"Consulta SQL generada: {query}")
            print(f"Parámetros para la consulta: {parametros}")

            # Ejecutar la consulta con los parámetros
            cursor = conn.cursor(pymysql.cursors.DictCursor)  # Utilizar DictCursor para obtener los resultados en forma de diccionario

            try:
                cursor.execute(query, tuple(parametros))
                result = cursor.fetchall()
                
                # Verifica si se obtuvieron registros
                if not result:
                    print("No se encontraron registros con los filtros aplicados.")
                else:
                    print(f"Registros encontrados: {len(result)}")
                    
                # Convertir las filas a diccionarios si el cursor no los devuelve así
                if isinstance(result, list):
                    for row in result:
                        # Si result no es un diccionario, lo convertimos manualmente
                        if not isinstance(row, dict):
                            columns = [desc[0] for desc in cursor.description]
                            row = dict(zip(columns, row))
                            
                        if self.privilegio == "admin" or row['empresa'] == empresa_filtro:
                            # Extraer valores en orden para que coincidan con las columnas de tu tabla
                            valores = (row['id'],row['id_Extintores'], row['fecha_realizado'], row['empresa'], row['area'], row['numero_extintor'], row['ubicacion_extintor'], row['tipo'], row['capacidad_kg'], row['fecha_fabricacion'], row['fecha_recarga'], row['fecha_vencimiento'], row['fecha_ultima_prueba'], row['presion'], row['manometro'], row['seguro'], row['etiquetas'], row['senalamientos'], row['circulo_numero'], row['pintura'], row['manguera'], row['boquilla'], row['golpes_danos'], row['obstruido'], row['comentarios'])
                            self.tree.insert("", "end", values=valores)

            except Exception as e:
                print(f"Error al ejecutar la consulta: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            print("No se pudo conectar a la base de datos.")

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
    
    def exportar_a_excel(self):
        # Abre una ventana para que el usuario elija dónde guardar el archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
            title="Guardar archivo de Excel"
        )
        
        # Verifica si se seleccionó una ubicación
        if not file_path:
            return  # Si el usuario cancela, no hace nada

        try:
            # Crear un nuevo libro de trabajo
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Extintores"

            # Encabezados
            headers = [
                "Id", "Referencia", "Fecha realizado", "Empresa", "Área",
                "Número de extintor", "Ubicación de extintor", "Tipo",
                "Capacidad en kg", "Fecha de fabricación", "Fecha de recarga",
                "Fecha de vencimiento", "Fecha última de prueba hidrostatica",
                "Presión", "Manómetro", "Seguro", "Etiquetas",
                "Señalamiento", "Círculo y número", "Pintura",
                "Manguera", "Boquilla", "Golpes o daños", "Obstruido", "Comentarios"
            ]
            sheet.append(headers)

            # Filas de datos desde el Treeview
            for row_id in self.tree.get_children():
                row = self.tree.item(row_id)["values"]
                sheet.append(row)

            # Guarda el archivo en la ubicación seleccionada
            workbook.save(file_path)
            messagebox.showinfo("Éxito", f"Datos exportados exitosamente a {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {e}")

    
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
                    id_Extintores = %s, fecha_realizado = %s, empresa = %s, area = %s,
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
        edit_window.geometry("450x500")
        edit_window.resizable(False, False)  # Evitar que se redimensione

        # Crear un frame desplazable
        scrollable_frame = ctk.CTkScrollableFrame(edit_window, corner_radius=10)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Crear campos de entrada para cada dato del extintor
        labels = [
            "Id", "Referencia", "Fecha realizado", "Empresa", "Área",
            "Número de extintor", "Ubicación de extintor", "Tipo",
            "Capacidad en kg", "Fecha de fabricación", "Fecha de recarga",
            "Fecha de vencimiento", "Fecha última de prueba hidrostatica",
            "Presión", "Manómetro", "Seguro", "Etiquetas",
            "Señalamiento", "Círculo y número", "Pintura",
            "Manguera", "Boquilla", "Golpes o daños", "Obstruido", "Comentarios"
        ]

        entries = []

        for label, value in zip(labels, extintor_data):
            row_frame = ctk.CTkFrame(scrollable_frame, corner_radius=8)
            row_frame.pack(pady=5, fill="x")

            label_widget = ctk.CTkLabel(row_frame, text=label, width=150, anchor="w", font=("Arial", 10, "bold"))
            label_widget.pack(side="left", padx=10)

            entry = ctk.CTkEntry(row_frame, width=250, placeholder_text="Introduce valor...")
            entry.insert(0, value)
            entry.pack(side="left", padx=10)
            entries.append(entry)

        # Botón para guardar cambios
        def guardar_cambios():
            # Obtener los nuevos valores
            new_values = [entry.get() for entry in entries]

            # Validar que no haya campos vacíos
            if any(not value for value in new_values):
                messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
                return

            # Actualizar en la base de datos
            self.update_extintor(item_id, new_values)

            # Actualizar la tabla en la interfaz
            self.tree.item(item_id, values=new_values)
            edit_window.destroy()

        save_button = ctk.CTkButton(scrollable_frame, text="Guardar Cambios", command=guardar_cambios, width=200, corner_radius=8)
        save_button.pack(pady=20)

        # Agregar botones de acción con más estilo
        cancel_button = ctk.CTkButton(scrollable_frame, text="Cancelar", command=edit_window.destroy, width=200, corner_radius=8, fg_color="red")
        cancel_button.pack(pady=5)

        # Establecer la ventana como modal (solo interactuar con esta ventana)
        edit_window.transient(self)
        edit_window.grab_set()


if __name__ == "__main__":
    app.mainloop()


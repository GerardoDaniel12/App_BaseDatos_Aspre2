import customtkinter as ctk
from tkinter import ttk, messagebox, Toplevel
import tkinter.messagebox as messagebox
from DB.ConexionExtintores import *
from datetime import datetime
from io import BytesIO


# Configuración para el tema del sistema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class GuiInicial(ctk.CTk):
    def __init__(self, user_data, privilegio, empresa):
        super().__init__()
        self.user_data = user_data
        self.privilegio = privilegio
        self.empresa = empresa  # Almacena el nombre de la empresa
        self.title("Extintores Generales")  # Título principal
        self.after(1, lambda: self.state('zoomed'))

        self.tree = None
        self.planta_filtro = None  # Variable para el filtro de planta
        self.planta_dropdown_resp = None
        self.planta_dropdown_bomberos = None
        self.planta_dropdown_hidrantes = None
        self.search_input = None  # Campo de búsqueda
        self.search_input_resp = None
        self.search_input_bomberos = None
        self.search_input_hidrantes = None
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

        ctk.CTkLabel(nav_frame, text=self.user_data.get("NombreUsuario", "Usuario"), font=("Arial", 14, "bold"), text_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#333333").pack(pady=(10, 5))
        ctk.CTkLabel(nav_frame, text=self.empresa, font=("Arial", 12), text_color="#BDC3C7" if ctk.get_appearance_mode() == "Dark" else "#666666").pack(pady=(0, 20))

        ctk.CTkLabel(nav_frame, text="Navegación", font=("Arial", 16, "bold"), text_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#333333").pack(pady=(10, 10))

        extintores_button = ctk.CTkButton(nav_frame, text="Extintores Generales", command=lambda: self.mostrar_seccion("Extintores Generales"), width=180, fg_color="#4B8BBE", height=35)
        extintores_button.pack(pady=10)

        respiracion_button = ctk.CTkButton(nav_frame, text="Gabinete de Equipo de Respiración", command=lambda: self.mostrar_seccion_Gabinete_Equipo_Respiración("Gabinete de Equipo de Respiración"), width=180, fg_color="#4B8BBE", height=35)
        respiracion_button.pack(pady=10)

        bomberos_button = ctk.CTkButton(nav_frame, text="Gabinete de Equipo de Bomberos", command=lambda: self.mostrar_seccion_Gabinete_Equipo_Bomberos_PSC("Gabinete de Equipo de Bomberos"), width=180, fg_color="#4B8BBE", height=35)
        bomberos_button.pack(pady=10)

        mangueras_button = ctk.CTkButton(nav_frame, text="Gabinete de Mangueras e Hidrantes", command=lambda: self.mostrar_seccion_Gabinete_hidrantes_mangueras("Gabinete de Mangueras e Hidrantes"), width=180, fg_color="#4B8BBE", height=35)
        mangueras_button.pack(pady=10)

        logout_button = ctk.CTkButton(nav_frame, text="Cerrar Sesión", command=self.cerrar_sesion, fg_color="#d9534f", hover_color="#c9302c", width=180)
        logout_button.pack(pady=20)

        # Frame de contenido principal para la tabla de extintores
        self.extintores_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#4D4D4D" if ctk.get_appearance_mode() == "Dark" else "#FFFFFF")
        self.extintores_frame.pack(fill="both", expand=True, padx=(0, 20), pady=10)

    def mostrar_seccion(self, titulo):
        self.title(titulo)  # Cambia el título dinámicamente
        self.extintores_frame.pack(fill="both", expand=True)
        for widget in self.extintores_frame.winfo_children():
            widget.destroy()  # Limpia el contenido actual del frame

        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        # Campo de búsqueda
        search_label = ctk.CTkLabel(filtros_frame, text="Buscar:", font=("Arial", 12))
        search_label.pack(side="left", padx=5)

        self.search_input = ctk.CTkEntry(filtros_frame, placeholder_text="Número de extintor, referencia, fecha, ubicación", width=180)
        self.search_input.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_extintor, width=40)
        search_button.pack(side="left", padx=5)

        # Botón de refrescar tabla
        refresh_button = ctk.CTkButton(filtros_frame, text="Refrescar", command=self.cargar_datos_extintores, width=80)
        refresh_button.pack(side="left", padx=5)

        # Botón para agregar extintor
        agregar_button = ctk.CTkButton(filtros_frame, text="Agregar", command=self.agregar_extintor, width=80, fg_color="#4CAF50")
        agregar_button.pack(side="left", padx=5)

        # Botón para modificar extintor
        modificar_button = ctk.CTkButton(filtros_frame, text="Modificar", command=self.modificar_extintor, width=80, fg_color="#FFA500")
        modificar_button.pack(side="left", padx=5)

        # Botón para eliminar extintor
        eliminar_button = ctk.CTkButton(filtros_frame, text="Eliminar", command=self.eliminar_extintor, width=80, fg_color="#FF6347")
        eliminar_button.pack(side="left", padx=5)

        # Dropdown para filtro por planta si es admin
        planta_label = ctk.CTkLabel(filtros_frame, text="Filtrar por Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_filtro = ttk.Combobox(filtros_frame, values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
        self.planta_filtro.bind("<<ComboboxSelected>>", self.filtrar_por_planta)
        self.planta_filtro.pack(side="left", padx=5)

        # Botón para exportar tabla completa
        exportar_button = ctk.CTkButton(filtros_frame, text="Exportar", command=self.exportar_reporte_extintores, width=80, fg_color="#4CAF50")
        exportar_button.pack(side="left", padx=5)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30, background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E", borderwidth=1)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4B8BBE", foreground="white")
        style.map("Treeview", background=[("selected", "#4B8BBE")])

        columnas = (
            "Referencia", "Fecha de Fabricación", "Planta", "Área", "Número de Extintor",
            "Ubicación del Extintor", "Tipo", "Capacidad en kg", "Fecha de Recarga", 
            "Fecha de Vencimiento", "Fecha Última Prueba", "Última Actualización"
        )

        self.tree = ttk.Treeview(self.extintores_frame, columns=columnas, show='headings', style="Treeview")

        # Configuración de encabezados y ancho de columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.tree.pack(side="top", fill="both", expand=True, pady=(5, 5))
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Agregar los botones de paginación
        paginacion_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        paginacion_frame.pack(side="bottom", fill="x", pady=(10, 5))  # Asegúrate de que esté al final

        # Botón para retroceder de página
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Retroceder", command=self.pagina_anterior, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Siguiente >>", command=self.pagina_siguiente, width=100)
        siguiente_button.pack(side="left", padx=5)

        # Cargar datos en la tabla
        self.cargar_datos_extintores()

    def filtrar_por_planta(self, event=None):
        # Obtener la planta seleccionada del dropdown
        planta_seleccionada = self.planta_filtro.get()

        # Si la planta seleccionada es "Todos", no se filtra por planta
        if planta_seleccionada == "Todos":
            self.cargar_datos_extintores(planta=None)  # No filtrar por planta
        else:
            self.cargar_datos_extintores(planta=planta_seleccionada)  # Filtrar por la planta seleccionada

    def buscar_extintor(self):
        # Obtener el valor del campo de búsqueda
        search_term = self.search_input.get()

        # Si el campo de búsqueda está vacío, mostrar un mensaje
        if not search_term.strip():
            messagebox.showwarning("Advertencia", "Por favor, ingresa un término de búsqueda.")
            return

        # Llamar a la función cargar_datos_extintores con el término de búsqueda y la página 1
        self.cargar_datos_extintores(search=search_term, page=1)
        
        # Opcional: Limpiar la selección del dropdown después de la búsqueda
        self.planta_filtro.set(self.planta_seleccionada)  # O cualquier valor predeterminado que quieras

    def cargar_datos_extintores(self, planta=None, search=None, page=1):
        try:
            # Si no se pasó la planta como parámetro, usar la planta seleccionada en el dropdown
            planta_filtrada = self.planta_filtro.get() if self.planta_filtro.get() else self.empresa

            # Llamar a la API para obtener los datos (incluyendo búsqueda y paginación)
            datos_extintores = obtener_extintores_api(planta_filtrada, search=search, page=page)

            if not datos_extintores:
                messagebox.showwarning("Advertencia", "No se encontraron datos de extintores.")
                return

            # Limpiar la tabla antes de cargar nuevos datos
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Agregar los datos obtenidos a la tabla
            for extintor in datos_extintores:
                self.tree.insert("", "end", values=(
                    extintor.get("referencia", ""),
                    extintor.get("fecha_fabricacion", ""),
                    extintor.get("planta", ""),
                    extintor.get("area", ""),
                    extintor.get("numerodeextintor", ""),
                    extintor.get("ubicacion_extintor", ""),
                    extintor.get("tipo", ""),
                    extintor.get("capacidad_kg", ""),
                    extintor.get("fecha_recarga", ""),
                    extintor.get("fecha_vencimiento", ""),
                    extintor.get("fecha_ultima_prueba", ""),
                    extintor.get("ultima_actualizacion", "")
                ))

            # Actualizar página actual
            self.current_page = page
            print(f"Datos cargados: Planta={planta_filtrada}, Búsqueda={search}, Página={page}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def exportar_tabla_completa(self):
        """
        Exporta la tabla completa o filtrada según la planta seleccionada o el privilegio del usuario.
        """
        try:
            # Si el usuario es admin, usa el valor del dropdown; si no, usa la empresa predeterminada
            planta_seleccionada = self.planta_filtro.get() if self.planta_filtro else self.empresa

            # Llama a la función de exportación, pasando el filtro de planta
            resultado = exportar_extintores_api(self.empresa, self.privilegio, planta_seleccionada)

            # Mostrar mensajes según el resultado
            if "Archivo Excel guardado exitosamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado durante la exportación: {e}")

    def modificar_extintor(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un extintor para modificar.")
            return

        extintor_data = self.tree.item(selected_item, "values")
        top = ctk.CTkToplevel(self)
        top.title("Modificar Extintor")
        top.geometry("400x570")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        scrollable_frame = ctk.CTkScrollableFrame(top, width=380, height=400)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Opciones para los dropdowns
        opciones_planta = ["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"]
        opciones_tipo = ["CO2", "PQS", "H2O", "Halotron", "ClaseK", "ClaseD", "AP", "AFFF"]

        # Tabla de capacidades por tipo
        capacidades_por_tipo = {
            "CO2": [2.2, 4.5, 6.8, 9.0, 12.0, 25.0, 50.0],
            "PQS": [1.0, 2.0, 4.5, 6.0, 9.0, 12.0, 34.0, 50.0, 68.0],
            "H2O": [10.0],
            "Halotron": [2.2],
            "ClaseK": [6.0],
            "ClaseD": [13.0],
            "AFFF": [6.0, 9.0, 50.0, 68.0],
            "AP": [6.0, 9.0]
        }

        opciones_capacidad = []

        # Campos y widgets
        fields = {
            "referencia": {"widget": "entry"},
            "fecha_fabricacion": {"widget": "entry", "hint": "MM AAAA"},
            "planta": {"widget": "dropdown", "options": opciones_planta},
            "area": {"widget": "entry"},
            "numerodeextintor": {"widget": "entry"},
            "ubicacion_extintor": {"widget": "entry"},
            "tipo": {"widget": "dropdown", "options": opciones_tipo},
            "capacidad_kg": {"widget": "dropdown", "options": opciones_capacidad},
            "fecha_recarga": {"widget": "entry", "hint": "MM AAAA"},
            "fecha_vencimiento": {"widget": "entry", "hint": "MM AAAA"},
            "fecha_ultima_prueba": {"widget": "entry", "hint": "MM AAAA"},
        }

        entries = {}

        def actualizar_capacidades(event):
            tipo_seleccionado = tipo_combobox.get()
            capacidades = capacidades_por_tipo.get(tipo_seleccionado, [])
            capacidad_combobox['values'] = capacidades
            if capacidades:
                capacidad_combobox.set(capacidades[0])

        for i, (field, config) in enumerate(fields.items()):
            label = ctk.CTkLabel(scrollable_frame, text=field.capitalize(), font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            # Determinar si el campo será editable o no
            editable = self.privilegio == "admin" or field in ["area", "numerodeextintor", "ubicacion_extintor"]

            if config["widget"] == "entry":
                entry = ctk.CTkEntry(scrollable_frame, state="normal" if editable else "disabled")
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                entry.insert(0, extintor_data[i])
                entries[field] = entry

                if "hint" in config:
                    hint_label = ctk.CTkLabel(scrollable_frame, text=config["hint"], font=("Arial", 10), text_color="gray")
                    hint_label.grid(row=i, column=2, padx=5, pady=5, sticky="w")

            elif config["widget"] == "dropdown":
                if field == "tipo":
                    tipo_combobox = ttk.Combobox(
                        scrollable_frame,
                        values=config["options"],
                        state="readonly" if editable else "disabled",
                    )
                    tipo_combobox.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                    tipo_combobox.set(extintor_data[i])
                    tipo_combobox.bind("<<ComboboxSelected>>", actualizar_capacidades)
                    entries[field] = tipo_combobox
                elif field == "capacidad_kg":
                    capacidad_combobox = ttk.Combobox(
                        scrollable_frame,
                        values=config["options"],
                        state="readonly" if editable else "disabled",
                    )
                    capacidad_combobox.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                    capacidad_combobox.set(extintor_data[i])
                    entries[field] = capacidad_combobox
                else:
                    combobox = ttk.Combobox(
                        scrollable_frame,
                        values=config["options"],
                        state="readonly" if editable else "disabled",
                    )
                    combobox.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                    combobox.set(extintor_data[i])
                    entries[field] = combobox

        def guardar_cambios():
            nuevos_datos = {}
            for field, widget in entries.items():
                if widget.cget("state") != "disabled":  # Solo guardar campos editables
                    nuevos_datos[field] = widget.get()

            # Enviar los datos a la API para guardarlos
            respuesta = editar_extintores_api(extintor_data[0], nuevos_datos)
            if "error" in respuesta:
                messagebox.showerror("Error", "No se pudo actualizar el extintor.")
            else:
                messagebox.showinfo("Éxito", "Extintor actualizado correctamente.")
                top.destroy()
                self.cargar_datos_extintores()

        guardar_button = ctk.CTkButton(top, text="Guardar Cambios", command=guardar_cambios)
        guardar_button.pack(pady=10)

    def eliminar_extintor(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un extintor para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar el extintor seleccionado?")
        if confirm:
            extintor_data = self.tree.item(selected_item, "values")
            referencia = extintor_data[0]  # La referencia está en la primera columna de la tabla

            # Llamar a la función de conexión para eliminar
            respuesta = eliminar_extintor_api(referencia)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", f"El extintor con referencia '{referencia}' fue eliminado exitosamente.")
                self.cargar_datos_extintores()  # Refrescar la tabla

    def agregar_extintor(self):
        # Crear ventana emergente
        top = ctk.CTkToplevel(self)
        top.title("Agregar Nuevo Extintor")
        top.geometry("450x640")

        # Opciones para dropdowns
        opciones_planta = ["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"]
        opciones_tipo = ["CO2", "PQS", "H2O", "Halotron", "ClaseK", "ClaseD", "AFFF", "AP"]
        capacidades = ["1.0", "2.0", "2.2", "4.5", "6.0", "6.8", "9.0", "10.0", "12.0", "13.0", "25.0", "34.0", "50.0", "68.0"]  # Lista de capacidades estáticas

        # Campos de entrada
        campos = [
            "numero_referencia", "area", "numerodeextintor", "ubicacion_extintor",
            "tipo", "capacidad_kg", "fecha_recarga", "fecha_vencimiento",
            "fecha_ultima_prueba", "fecha_fabricacion"
        ]
        entradas = {}

        # Crear formulario dinámico
        for idx, campo in enumerate(campos):
            label = ctk.CTkLabel(top, text=campo.replace("_", " ").capitalize(), font=("Arial", 12))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            if campo == "tipo":
                tipo_combobox = ctk.CTkComboBox(top, values=opciones_tipo, width=250)
                tipo_combobox.grid(row=idx, column=1, padx=10, pady=5)
                entradas[campo] = tipo_combobox
            elif campo == "capacidad_kg":
                capacidad_combobox = ctk.CTkComboBox(top, values=capacidades, width=250)
                capacidad_combobox.grid(row=idx, column=1, padx=10, pady=5)
                entradas[campo] = capacidad_combobox
            elif "fecha" in campo:
                entry = ctk.CTkEntry(top, width=250, placeholder_text="AAAA-MM-DD")
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entradas[campo] = entry
            else:
                entry = ctk.CTkEntry(top, width=250)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entradas[campo] = entry

        # Campo de planta (sin restricción)
        label_planta = ctk.CTkLabel(top, text="Planta", font=("Arial", 12))
        label_planta.grid(row=len(campos), column=0, padx=10, pady=5, sticky="w")

        planta_combobox = ctk.CTkComboBox(top, values=opciones_planta, width=250)
        planta_combobox.grid(row=len(campos), column=1, padx=10, pady=5)
        entradas["planta"] = planta_combobox

        def guardar_datos():
            # Obtener los valores ingresados
            datos = {campo: entrada.get() for campo, entrada in entradas.items()}

            # Validar campos obligatorios
            for campo, valor in datos.items():
                if not valor:
                    messagebox.showerror("Error", f"El campo '{campo}' es obligatorio.")
                    return

            # Validar formato de fechas
            for campo in ["fecha_recarga", "fecha_vencimiento", "fecha_ultima_prueba", "fecha_fabricacion"]:
                if not validar_fecha(datos[campo]):
                    messagebox.showerror("Error", f"El campo '{campo}' debe tener el formato AAAA-MM-DD.")
                    return

            # Llamar a la función de conexión para agregar
            respuesta = agregar_extintor_api(datos)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", respuesta.get("message", "El extintor fue agregado exitosamente."))
                top.destroy()  # Cerrar ventana emergente
                self.cargar_datos_extintores()  # Refrescar la tabla


        def validar_fecha(fecha):
            import re
            patron = r"^\d{4}-\d{2}-\d{2}$"
            return re.match(patron, fecha) is not None

        # Botón para guardar los datos
        guardar_button = ctk.CTkButton(top, text="Guardar", command=guardar_datos)
        guardar_button.grid(row=len(campos) + 1, column=0, columnspan=2, pady=20)

    def pagina_anterior(self):
        # Decrementar la página actual, asegurándose de no ir más allá de la página 1
        if self.current_page > 1:
            self.current_page -= 1

            # Llamar a la función cargar_datos_extintores con la nueva página
            self.cargar_datos_extintores(page=self.current_page)

            # Opcional: Deshabilitar el botón si ya estamos en la primera página
            # if self.current_page == 1:
            #     self.retroceder_button.config(state="disabled")

    def pagina_siguiente(self):
        # Incrementar la página actual
        self.current_page += 1

        # Llamar a la función cargar_datos_extintores con la nueva página
        self.cargar_datos_extintores(page=self.current_page)

        # Opcional: Deshabilitar el botón si se alcanzó la última página (según los datos de tu API)
        # if self.current_page == self.total_pages:
        #     self.siguiente_button.config(state="disabled")

    def exportar_reporte_extintores(self):
        """
        Abre una ventana emergente con opciones para exportar la tabla de datos o un reporte completo de extintores inspeccionados.
        """
        top = ctk.CTkToplevel(self)
        top.title("Exportar Reporte de Extintores")
        top.geometry("400x200")

        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        # Etiqueta de descripción
        label = ctk.CTkLabel(
            top,
            text="Seleccione una opción para exportar:",
            font=("Arial", 14)
        )
        label.pack(pady=10)

        # Botón para exportar la tabla de datos
        def exportar_tabla():
            """
            Exporta la tabla actual mostrada en el sistema.
            """
            planta_seleccionada = self.planta_filtro.get() if self.planta_filtro else self.empresa
            resultado = exportar_extintores_api(planta_seleccionada)

            if isinstance(resultado, BytesIO):
                # Guardar el archivo con un diálogo
                ruta_archivo = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Archivos de Excel", "*.xlsx")],
                    title="Guardar archivo como",
                    initialfile=f"tabla_extintores_{planta_seleccionada}.xlsx"
                )
                if ruta_archivo:
                    with open(ruta_archivo, "wb") as archivo:
                        archivo.write(resultado.getvalue())
                    messagebox.showinfo("Éxito", f"Tabla exportada exitosamente a {ruta_archivo}")
            else:
                messagebox.showerror("Error", f"Error al exportar la tabla: {resultado}")

        exportar_tabla_button = ctk.CTkButton(
            top,
            text="Exportar Tabla de Datos",
            command=self.exportar_tabla_completa
        )
        exportar_tabla_button.pack(pady=10)

        # Botón para exportar el reporte completo
        def exportar_reporte():
            """
            Exporta el reporte completo de extintores inspeccionados y no inspeccionados.
            """
            planta_seleccionada = self.planta_filtro.get() if self.planta_filtro else self.empresa

            # Mostrar ventana emergente para elegir mes y año
            def seleccionar_filtros():
                """
                Permite al usuario seleccionar el mes y el año para filtrar el reporte.
                """
                filtro_top = ctk.CTkToplevel(top)
                filtro_top.title("Seleccionar Filtros")
                filtro_top.geometry("300x200")

                filtro_top.lift()
                filtro_top.attributes('-topmost', True)
                filtro_top.after(10, lambda: top.attributes('-topmost', False))

                # Campo para el mes
                mes_label = ctk.CTkLabel(filtro_top, text="Mes (Opcional):", font=("Arial", 12))
                mes_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                mes_entry = ctk.CTkEntry(filtro_top, width=150)
                mes_entry.grid(row=0, column=1, padx=10, pady=5)

                # Campo para el año
                ano_label = ctk.CTkLabel(filtro_top, text="Año (Opcional):", font=("Arial", 12))
                ano_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
                ano_entry = ctk.CTkEntry(filtro_top, width=150)
                ano_entry.grid(row=1, column=1, padx=10, pady=5)

                # Botón para confirmar los filtros
                def confirmar_filtros():
                    mes = mes_entry.get()
                    ano = ano_entry.get()

                    # Validar que mes y año sean números si no están vacíos
                    if mes and not mes.isdigit():
                        messagebox.showerror("Error", "El mes debe ser un número.")
                        return
                    if ano and not ano.isdigit():
                        messagebox.showerror("Error", "El año debe ser un número.")
                        return

                    resultado = exportar_reporte_extintores_api(
                        planta_seleccionada,
                        mes=int(mes) if mes else None,
                        ano=int(ano) if ano else None
                    )

                    if isinstance(resultado, BytesIO):
                        ruta_archivo = filedialog.asksaveasfilename(
                            defaultextension=".xlsx",
                            filetypes=[("Archivos de Excel", "*.xlsx")],
                            title="Guardar archivo como",
                            initialfile=f"Reporte_Extintores_{planta_seleccionada}.xlsx"
                        )
                        if ruta_archivo:
                            with open(ruta_archivo, "wb") as archivo:
                                archivo.write(resultado.getvalue())
                            messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a {ruta_archivo}")
                    else:
                        messagebox.showerror("Error", f"Error al exportar el reporte: {resultado}")

                    filtro_top.destroy()

                confirmar_button = ctk.CTkButton(filtro_top, text="Confirmar", command=confirmar_filtros)
                confirmar_button.grid(row=2, column=0, columnspan=2, pady=10)

            seleccionar_filtros()

        exportar_reporte_button = ctk.CTkButton(
            top,
            text="Exportar Reporte Completo",
            command=exportar_reporte
        )
        exportar_reporte_button.pack(pady=10)


#############################################################################################################
                            #Seccion para Gabientes de equipo de respiracion:
#############################################################################################################
    
    def configurar_filtros_resp(self):
        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        planta_label = ctk.CTkLabel(filtros_frame, text="Seleccionar Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_dropdown_resp = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],
            width=200
        )
        self.planta_dropdown_resp.set("Todos")  # Valor inicial predeterminado
        self.planta_dropdown_resp.pack(side="left", padx=5)
        self.planta_dropdown_resp.bind("<<ComboboxSelected>>", self.filtrar_por_planta_resp)

        # Campo de búsqueda
        self.search_input_resp = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar equipos de respiración...", width=200)
        self.search_input_resp.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_respiracion)
        search_button.pack(side="left", padx=5)

    def filtrar_por_planta_resp(self, event=None):
        """
        Maneja el evento de selección de planta en el dropdown para equipos de respiración.
        """
        if self.planta_dropdown_resp:
            planta_seleccionada = self.planta_dropdown_resp.get()
            if planta_seleccionada:
                print(f"[DEBUG] Planta seleccionada: {planta_seleccionada}")
                self.cargar_datos_resp(planta=planta_seleccionada)
            else:
                print("[DEBUG] No se seleccionó una planta válida. Usando 'Todos'.")
                self.cargar_datos_resp(planta="Todos")
        else:
            print("[DEBUG] El dropdown no está definido.")
            self.cargar_datos_resp(planta="Todos")
      
    def cargar_datos_resp(self, planta=None, search=None, page=1):
        """
        Carga los datos de equipos de respiración en la tabla.
        """
        try:
            # Determinar la planta a usar
            planta_filtrada = self.planta_dropdown_resp.get() if self.planta_dropdown_resp.get() else self.empresa

            print(f"[DEBUG] Cargando datos para planta: {planta_filtrada}, búsqueda: {search}, página: {page}")

            # Llamar a la API
            datos_resp = obtener_gabinetes_api(planta_filtrada, search=search, page=page)

            if not datos_resp:
                messagebox.showwarning("Advertencia", "No se encontraron datos de equipos de respiración.")
                return

            # Limpiar la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Agregar los datos a la tabla
            for equipo in datos_resp:
                self.tree.insert("", "end", values=(
                    equipo.get("referencia", ""),
                    equipo.get("numero", ""),
                    equipo.get("area", ""),
                    equipo.get("ubicacion", ""),
                    equipo.get("planta", ""),
                    equipo.get("fecha_ph", ""),
                    equipo.get("ultima_actualizacion", "")
                ))

            # Actualizar página actual
            self.current_page = page
            print(f"[DEBUG] Datos cargados para planta: {planta_filtrada}, página: {page}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def mostrar_seccion_Gabinete_Equipo_Respiración(self, titulo):
        self.title(titulo)  # Cambia el título dinámicamente
        self.extintores_frame.pack(fill="both", expand=True)
        for widget in self.extintores_frame.winfo_children():
            widget.destroy()  # Limpia el contenido actual del frame

        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        # Campo de búsqueda
        search_label = ctk.CTkLabel(filtros_frame, text="Buscar:", font=("Arial", 12))
        search_label.pack(side="left", padx=5)

        self.search_input_resp = ctk.CTkEntry(filtros_frame, placeholder_text="Número, referencia, ubicación", width=180)
        self.search_input_resp.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_respiracion, width=40)
        search_button.pack(side="left", padx=5)

        # Botón de refrescar tabla
        refresh_button = ctk.CTkButton(filtros_frame, text="Refrescar", command=self.cargar_datos_resp, width=80)
        refresh_button.pack(side="left", padx=5)

        # Botón para agregar extintor
        agregar_button = ctk.CTkButton(filtros_frame, text="Agregar", command=self.agregar_equipo_respiracion, width=80, fg_color="#4CAF50")
        agregar_button.pack(side="left", padx=5)

        # Botón para modificar extintor
        modificar_button = ctk.CTkButton(filtros_frame, text="Modificar", command=self.modificar_equipo_respiracion, width=80, fg_color="#FFA500")
        modificar_button.pack(side="left", padx=5)

        # Botón para eliminar extintor
        eliminar_button = ctk.CTkButton(filtros_frame, text="Eliminar", command=self.eliminar_equipo_respiracion, width=80, fg_color="#FF6347")
        eliminar_button.pack(side="left", padx=5)

        # Dropdown para filtro por planta si es admin
        planta_label = ctk.CTkLabel(filtros_frame, text="Filtrar por Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_dropdown_resp = ttk.Combobox(filtros_frame, values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
        self.planta_dropdown_resp.bind("<<ComboboxSelected>>", self.filtrar_por_planta_resp)
        self.planta_dropdown_resp.pack(side="left", padx=5)

        # Botón para exportar tabla completa
        exportar_button = ctk.CTkButton(filtros_frame, text="Exportar", command=self.exportar_reporte_gabinete_equipo_respiracion, width=80, fg_color="#4CAF50")
        exportar_button.pack(side="left", padx=5)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30, background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E", borderwidth=1)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4B8BBE", foreground="white")
        style.map("Treeview", background=[("selected", "#4B8BBE")])

        columnas = (
            "Referencia", "Numero", "Area", "Ubicacion", "Planta",
            "Fecha_ph", "Ultima Actualizacion"
        )

        self.tree = ttk.Treeview(self.extintores_frame, columns=columnas, show='headings', style="Treeview")

        # Configuración de encabezados y ancho de columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.tree.pack(side="top", fill="both", expand=True, pady=(5, 5))
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Agregar los botones de paginación
        paginacion_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        paginacion_frame.pack(side="bottom", fill="x", pady=(10, 5))  # Asegúrate de que esté al final

        # Botón para retroceder de página
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Retroceder", command=self.pagina_anterior, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Siguiente >>", command=self.pagina_siguiente, width=100)
        siguiente_button.pack(side="left", padx=5)

        # Cargar datos en la tabla
        self.cargar_datos_resp()

    def buscar_equipo_respiracion(self):
        """
        Función para buscar equipos de respiración según un término de búsqueda.
        """
        search_term = self.search_input_resp.get()  # Obtener el término de búsqueda desde la entrada
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda.")
            return

        print(f"Término de búsqueda: {search_term}")

        # Determinar la planta
        planta_filtrada = self.planta_dropdown_resp.get() if hasattr(self, "planta_dropdown_resp") else "Todos"

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_resp(planta=planta_filtrada, search=search_term, page=self.current_page)

    def exportar_tabla_completa_resp(self):
        """
        Exporta la tabla completa o filtrada según la planta seleccionada o el privilegio del usuario.
        """
        try:
            # Si el usuario es admin, usa el valor del dropdown; si no, usa la empresa predeterminada
            planta_seleccionada = self.planta_dropdown_resp.get() if self.planta_dropdown_resp else self.empresa

            # Llama a la función de exportación, pasando el filtro de planta
            resultado = exportar_gabinetes_api(self.empresa, planta_seleccionada)

            # Mostrar mensajes según el resultado
            if "Archivo Excel guardado exitosamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado durante la exportación: {e}")

    def agregar_equipo_respiracion(self):
        # Crear ventana emergente
        top = ctk.CTkToplevel(self)
        top.title("Agregar Nuevo Gabinete")
        top.geometry("450x500")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        # Campos de entrada
        campos = ["referencia", "numero", "area", "ubicacion", "fecha_ph"]
        entradas = {}

        # Crear formulario dinámico
        for idx, campo in enumerate(campos):
            label = ctk.CTkLabel(top, text=campo.replace("_", " ").capitalize(), font=("Arial", 12))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            
            # Verificar si el campo es fecha
            if "fecha" in campo:
                entry = ctk.CTkEntry(top, width=250, placeholder_text="AAAA-MM-DD")
            else:
                entry = ctk.CTkEntry(top, width=250)
            
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entradas[campo] = entry

        # Campo de planta como dropdown
        label_planta = ctk.CTkLabel(top, text="Planta", font=("Arial", 12))
        label_planta.grid(row=len(campos), column=0, padx=10, pady=5, sticky="w")

        # Crear ComboBox para el campo "planta"
        planta_options = ["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"]  # Opciones disponibles
        planta_entry = ctk.CTkComboBox(top, values=planta_options, width=250)
        planta_entry.grid(row=len(campos), column=1, padx=10, pady=5)
        planta_entry.set(self.empresa)  # Prellenar con la empresa del usuario (si se desea)

        entradas["planta"] = planta_entry

        def guardar_datos():
            # Obtener los valores ingresados
            datos = {campo: entrada.get() for campo, entrada in entradas.items()}
            datos["planta"] = planta_entry.get()  # Planta seleccionada

            # Validar que todos los campos están llenos
            for campo, valor in datos.items():
                if not valor:
                    messagebox.showerror("Error", f"El campo '{campo}' es obligatorio.")
                    return

            # Llamar a la función de conexión para agregar
            respuesta = agregar_gabinete_api(datos)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", respuesta.get("message", "El gabinete fue agregado exitosamente."))
                top.destroy()  # Cerrar ventana emergente
                self.cargar_datos_gabinetes()  # Refrescar la tabla

        # Botón para guardar los datos
        guardar_button = ctk.CTkButton(top, text="Guardar", command=guardar_datos)
        guardar_button.grid(row=len(campos) + 1, column=0, columnspan=2, pady=20)

    def eliminar_equipo_respiracion(self):
        """
        Elimina un equipo de respiración seleccionado en la tabla.
        """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un equipo de respiración para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar el equipo seleccionado?")
        if confirm:
            equipo_data = self.tree.item(selected_item, "values")
            referencia = equipo_data[0]  # La referencia está en la primera columna de la tabla

            # Llamar a la función de conexión para eliminar
            respuesta = eliminar_gabinete_api(referencia)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", f"El equipo de respiración con referencia '{referencia}' fue eliminado exitosamente.")
                self.cargar_datos_resp()  # Refrescar la tabla

    def modificar_equipo_respiracion(self):
        """
        Abre una ventana emergente para modificar los datos de un equipo de respiración seleccionado en la tabla.
        """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un equipo de respiración para modificar.")
            return

        # Obtener los datos del equipo seleccionado
        equipo_data = self.tree.item(selected_item, "values")
        
        try:
            referencia = equipo_data[0]
            numero = equipo_data[1]
            area = equipo_data[2]
            ubicacion = equipo_data[3]
            fecha_ph = equipo_data[5]  # Índice correcto para fecha_ph
            planta = equipo_data[4]
        except IndexError as e:
            messagebox.showerror("Error", f"Error al obtener datos del equipo: {e}")
            return

        # Crear ventana para modificar los datos
        top = ctk.CTkToplevel(self)
        top.title("Modificar Equipo de Respiración")
        top.geometry("450x500")

        scrollable_frame = ctk.CTkScrollableFrame(top, width=400, height=350)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Campos a editar
        fields = ["referencia", "numero", "area", "ubicacion", "fecha_ph"]
        values = [referencia, numero, area, ubicacion, fecha_ph]
        entries = {}

        for i, (field, value) in enumerate(zip(fields, values)):
            label = ctk.CTkLabel(scrollable_frame, text=field.capitalize(), font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(scrollable_frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            
            if field == "fecha_ph":
                try:
                    # Cambiar formato de '10-2022' a '10 2022'
                    formatted_date = value.replace("-", " ")
                    entry.insert(0, formatted_date)
                except AttributeError:
                    entry.insert(0, value)  # Si el valor no es válido, usar el original
            else:
                entry.insert(0, value)

            entries[field] = entry


        # Campo de planta como dropdown
        planta_label = ctk.CTkLabel(scrollable_frame, text="Planta", font=("Arial", 12))
        planta_label.grid(row=len(fields), column=0, padx=10, pady=5, sticky="w")

        planta_dropdown = ctk.CTkComboBox(
            scrollable_frame, 
            values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],  # Opciones reales
            width=250
        )
        planta_dropdown.set(planta)
        planta_dropdown.grid(row=len(fields), column=1, padx=10, pady=5)
        entries["planta"] = planta_dropdown

        def guardar_cambios():
            nuevos_datos = {field: (entry.get() if field != "planta" else planta_dropdown.get()) for field, entry in entries.items()}

            fecha_ph = nuevos_datos.get("fecha_ph", "")
            try:
                # Validar que la fecha tenga el formato 'MM AAAA'
                datetime.strptime(fecha_ph, "%m %Y")
            except ValueError:
                messagebox.showerror("Error", "El campo 'Fecha PH' debe tener el formato 'MM AAAA'.")
                return

            # Llamar a la API para actualizar los datos
            respuesta = editar_gabinetes_api(referencia, nuevos_datos)
            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", "Equipo de respiración actualizado correctamente.")
                top.destroy()
                self.cargar_datos_resp()


        guardar_button = ctk.CTkButton(top, text="Guardar Cambios", command=guardar_cambios)
        guardar_button.pack(pady=10)

    def exportar_reporte_gabinete_equipo_respiracion(self):
        """
        Abre una ventana emergente con opciones para exportar la tabla de datos o un reporte completo de extintores inspeccionados.
        """
        top = ctk.CTkToplevel(self)
        top.title("Exportar Reporte de Equipo de Respiracion")
        top.geometry("400x200")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        # Etiqueta de descripción
        label = ctk.CTkLabel(
            top,
            text="Seleccione una opción para exportar:",
            font=("Arial", 14)
        )
        label.pack(pady=10)

        # Botón para exportar la tabla de datos
        exportar_tabla_button = ctk.CTkButton(
            top,
            text="Exportar Tabla de Datos",
            command=self.exportar_tabla_completa_resp
        )
        exportar_tabla_button.pack(pady=10)

        # Botón para exportar el reporte completo
        def exportar_reporte():
            """
            Exporta el reporte completo de extintores inspeccionados y no inspeccionados.
            """
            planta_seleccionada = self.planta_dropdown_resp.get() if self.planta_dropdown_resp else self.empresa

            # Mostrar ventana emergente para elegir mes y año
            def seleccionar_filtros():
                """
                Permite al usuario seleccionar el mes y el año para filtrar el reporte.
                """
                filtro_top = ctk.CTkToplevel(top)
                filtro_top.title("Seleccionar Filtros")
                filtro_top.geometry("300x200")
                filtro_top.lift()
                filtro_top.attributes('-topmost', True)
                filtro_top.after(10, lambda: top.attributes('-topmost', False))

                # Campo para el mes
                mes_label = ctk.CTkLabel(filtro_top, text="Mes (Opcional):", font=("Arial", 12))
                mes_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                mes_entry = ctk.CTkEntry(filtro_top, width=150)
                mes_entry.grid(row=0, column=1, padx=10, pady=5)

                # Campo para el año
                ano_label = ctk.CTkLabel(filtro_top, text="Año (Opcional):", font=("Arial", 12))
                ano_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
                ano_entry = ctk.CTkEntry(filtro_top, width=150)
                ano_entry.grid(row=1, column=1, padx=10, pady=5)

                # Botón para confirmar los filtros
                def confirmar_filtros():
                    mes = mes_entry.get()
                    ano = ano_entry.get()

                    # Validar que mes y año sean números si no están vacíos
                    if mes and not mes.isdigit():
                        messagebox.showerror("Error", "El mes debe ser un número.")
                        return
                    if ano and not ano.isdigit():
                        messagebox.showerror("Error", "El año debe ser un número.")
                        return

                    resultado = exportar_reporte_gabinetes_equipo_respiracion_api(
                        planta_seleccionada,
                        mes=int(mes) if mes else None,
                        ano=int(ano) if ano else None
                    )

                    if isinstance(resultado, BytesIO):
                        ruta_archivo = filedialog.asksaveasfilename(
                            defaultextension=".xlsx",
                            filetypes=[("Archivos de Excel", "*.xlsx")],
                            title="Guardar archivo como",
                            initialfile=f"Reporte_Gabinetes_Equipo_Respiracion{planta_seleccionada}.xlsx"
                        )
                        if ruta_archivo:
                            with open(ruta_archivo, "wb") as archivo:
                                archivo.write(resultado.getvalue())
                            messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a {ruta_archivo}")
                    else:
                        messagebox.showerror("Error", f"Error al exportar el reporte: {resultado}")

                    filtro_top.destroy()

                confirmar_button = ctk.CTkButton(filtro_top, text="Confirmar", command=confirmar_filtros)
                confirmar_button.grid(row=2, column=0, columnspan=2, pady=10)

            seleccionar_filtros()

        exportar_reporte_button = ctk.CTkButton(
            top,
            text="Exportar Reporte Completo",
            command=exportar_reporte
        )
        exportar_reporte_button.pack(pady=10)


#############################################################################################################
                            #Seccion para Gabientes de equipo de bomberos:
#############################################################################################################

    def configurar_filtros_bomberos(self):
        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        planta_label = ctk.CTkLabel(filtros_frame, text="Seleccionar Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_dropdown_bomberos = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],
            width=200
        )
        self.planta_dropdown_bomberos.set("Todos")  # Valor inicial predeterminado
        self.planta_dropdown_bomberos.pack(side="left", padx=5)
        self.planta_dropdown_bomberos.bind("<<ComboboxSelected>>", self.filtrar_por_planta_bomberos)

        # Campo de búsqueda
        self.search_input_bomberos = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar equipos de respiración...", width=200)
        self.search_input_bomberos.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_bomberos)
        search_button.pack(side="left", padx=5)

    def filtrar_por_planta_bomberos(self, event=None):
        """
        Maneja el evento de selección de planta en el dropdown para equipos de respiración.
        """
        if self.planta_dropdown_bomberos:
            planta_seleccionada = self.planta_dropdown_bomberos.get()
            if planta_seleccionada:
                print(f"[DEBUG] Planta seleccionada: {planta_seleccionada}")
                self.cargar_datos_bomberos(planta=planta_seleccionada)
            else:
                print("[DEBUG] No se seleccionó una planta válida. Usando 'Todos'.")
                self.cargar_datos_bomberos(planta="Todos")
        else:
            print("[DEBUG] El dropdown no está definido.")
            self.cargar_datos_bomberos(planta="Todos")
      
    def cargar_datos_bomberos(self, planta=None, search=None, page=1):
        """
        Carga los datos de equipos de respiración en la tabla.
        """
        try:
            # Determinar la planta a usar
            planta_filtrada = self.planta_dropdown_bomberos.get() if self.planta_dropdown_bomberos.get() else self.empresa

            print(f"[DEBUG] Cargando datos para planta: {planta_filtrada}, búsqueda: {search}, página: {page}")

            # Llamar a la API
            datos_bomb = obtener_gabinetes_equipo_bomberos_psc_api(planta_filtrada, search=search, page=page)

            if not datos_bomb:
                messagebox.showwarning("Advertencia", "No se encontraron datos de equipos de respiración.")
                return

            # Limpiar la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Agregar los datos a la tabla
            for equipo in datos_bomb:
                self.tree.insert("", "end", values=(
                    equipo.get("referencia", ""),
                    equipo.get("numero", ""),
                    equipo.get("area", ""),
                    equipo.get("ubicacion", ""),
                    equipo.get("planta", ""),
                    equipo.get("ultima_actualizacion", "")
                ))

            # Actualizar página actual
            self.current_page = page
            print(f"[DEBUG] Datos cargados para planta: {planta_filtrada}, página: {page}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def mostrar_seccion_Gabinete_Equipo_Bomberos_PSC(self, titulo):
        self.title(titulo)  # Cambia el título dinámicamente
        self.extintores_frame.pack(fill="both", expand=True)
        for widget in self.extintores_frame.winfo_children():
            widget.destroy()  # Limpia el contenido actual del frame

        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        # Campo de búsqueda
        search_label = ctk.CTkLabel(filtros_frame, text="Buscar:", font=("Arial", 12))
        search_label.pack(side="left", padx=5)

        self.search_input_bomberos = ctk.CTkEntry(filtros_frame, placeholder_text="Número, referencia, ubicación", width=180)
        self.search_input_bomberos.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_bomberos, width=40)
        search_button.pack(side="left", padx=5)

        # Botón de refrescar tabla
        refresh_button = ctk.CTkButton(filtros_frame, text="Refrescar", command=self.cargar_datos_bomberos, width=80)
        refresh_button.pack(side="left", padx=5)

        # Botón para agregar extintor
        agregar_button = ctk.CTkButton(filtros_frame, text="Agregar", command=self.agregar_equipo_bomberos, width=80, fg_color="#4CAF50")
        agregar_button.pack(side="left", padx=5)

        # Botón para modificar extintor
        modificar_button = ctk.CTkButton(filtros_frame, text="Modificar", command=self.modificar_equipo_bomberos, width=80, fg_color="#FFA500")
        modificar_button.pack(side="left", padx=5)

        # Botón para eliminar extintor
        eliminar_button = ctk.CTkButton(filtros_frame, text="Eliminar", command=self.eliminar_equipo_bomberos, width=80, fg_color="#FF6347")
        eliminar_button.pack(side="left", padx=5)

        # Dropdown para filtro por planta si es admin
        planta_label = ctk.CTkLabel(filtros_frame, text="Filtrar por Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_dropdown_bomberos = ttk.Combobox(filtros_frame, values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
        self.planta_dropdown_bomberos.bind("<<ComboboxSelected>>", self.filtrar_por_planta_bomberos)
        self.planta_dropdown_bomberos.pack(side="left", padx=5)

        # Botón para exportar tabla completa
        exportar_button = ctk.CTkButton(filtros_frame, text="Exportar", command=self.exportar_reporte_gabinete_equipo_bomberos, width=80, fg_color="#4CAF50")
        exportar_button.pack(side="left", padx=5)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30, background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E", borderwidth=1)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4B8BBE", foreground="white")
        style.map("Treeview", background=[("selected", "#4B8BBE")])

        columnas = (
            "Referencia", "Numero", "Area", "Ubicacion", "Planta",
            "Ultima Actualizacion"
        )

        self.tree = ttk.Treeview(self.extintores_frame, columns=columnas, show='headings', style="Treeview")

        # Configuración de encabezados y ancho de columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.tree.pack(side="top", fill="both", expand=True, pady=(5, 5))
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Agregar los botones de paginación
        paginacion_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        paginacion_frame.pack(side="bottom", fill="x", pady=(10, 5))  # Asegúrate de que esté al final

        # Botón para retroceder de página
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Retroceder", command=self.pagina_anterior, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Siguiente >>", command=self.pagina_siguiente, width=100)
        siguiente_button.pack(side="left", padx=5)

        # Cargar datos en la tabla
        self.cargar_datos_bomberos()

    def buscar_equipo_bomberos(self):
        """
        Función para buscar equipos de respiración según un término de búsqueda.
        """
        search_term = self.search_input_bomberos.get()  # Obtener el término de búsqueda desde la entrada
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda.")
            return

        print(f"Término de búsqueda: {search_term}")

        # Determinar la planta
        planta_filtrada = self.planta_dropdown_bomberos.get() if hasattr(self, "planta_dropdown_bomberos") else "Todos"

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_bomberos(planta=planta_filtrada, search=search_term, page=self.current_page)

    def exportar_tabla_completa_bomberos(self):
        """
        Exporta la tabla completa o filtrada según la planta seleccionada o el privilegio del usuario.
        """
        try:
            # Si el usuario es admin, usa el valor del dropdown; si no, usa la empresa predeterminada
            planta_seleccionada = self.planta_dropdown_bomberos.get() if self.planta_dropdown_bomberos else self.empresa

            # Llama a la función de exportación, pasando el filtro de planta
            resultado = exportar_gabinetes_bomberos_api(self.empresa, planta_seleccionada)

            # Mostrar mensajes según el resultado
            if "Archivo Excel guardado exitosamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado durante la exportación: {e}")

    def agregar_equipo_bomberos(self):
        """
        Abre una ventana emergente para agregar un nuevo gabinete de bomberos.
        """
        # Crear ventana emergente
        top = ctk.CTkToplevel(self)
        top.title("Agregar Nuevo Gabinete de Bomberos")
        top.geometry("450x500")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        # Campos de entrada
        campos = ["referencia", "numero", "area", "ubicacion"]
        entradas = {}

        # Crear formulario dinámico
        for idx, campo in enumerate(campos):
            label = ctk.CTkLabel(top, text=campo.replace("_", " ").capitalize(), font=("Arial", 12))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            entry = ctk.CTkEntry(top, width=250)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entradas[campo] = entry

        # Campo de planta como dropdown
        label_planta = ctk.CTkLabel(top, text="Planta", font=("Arial", 12))
        label_planta.grid(row=len(campos), column=0, padx=10, pady=5, sticky="w")

        planta_options = ["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"]
        planta_entry = ctk.CTkComboBox(top, values=planta_options, width=250)
        planta_entry.grid(row=len(campos), column=1, padx=10, pady=5)
        planta_entry.set(self.empresa)  # Prellenar con la empresa del usuario (si aplica)

        entradas["planta"] = planta_entry

        def guardar_datos():
            """
            Guarda los datos del nuevo gabinete y llama a la API para agregarlo.
            """
            # Obtener los valores ingresados
            datos = {campo: entrada.get() for campo, entrada in entradas.items()}
            datos["planta"] = planta_entry.get()  # Planta seleccionada

            # Validar que todos los campos están llenos
            for campo, valor in datos.items():
                if not valor:
                    messagebox.showerror("Error", f"El campo '{campo}' es obligatorio.")
                    return

            # Llamar a la API para agregar el gabinete
            respuesta = agregar_gabinete_bomberos_api(datos)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", respuesta.get("message", "El gabinete fue agregado exitosamente."))
                top.destroy()  # Cerrar ventana emergente
                self.cargar_datos_bomberos()  # Refrescar la tabla

        # Botón para guardar los datos
        guardar_button = ctk.CTkButton(top, text="Guardar", command=guardar_datos)
        guardar_button.grid(row=len(campos) + 1, column=0, columnspan=2, pady=20)

    def eliminar_equipo_bomberos(self):
        """
        Elimina un gabinete de bomberos seleccionado en la tabla.
        """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un gabinete para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar el gabinete seleccionado?")
        if confirm:
            # Obtener la referencia del equipo seleccionado
            equipo_data = self.tree.item(selected_item, "values")
            try:
                referencia = equipo_data[0]  # Se asume que la referencia está en la primera columna
            except IndexError:
                messagebox.showerror("Error", "No se pudo obtener la referencia del gabinete.")
                return

            # Llamar a la API para eliminar el gabinete
            respuesta = eliminar_gabinete_bomberos_api(referencia)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", f"El gabinete con referencia '{referencia}' fue eliminado exitosamente.")
                self.cargar_datos_bomberos()  # Refrescar la tabla

    def modificar_equipo_bomberos(self):
        """
        Abre una ventana emergente para modificar los datos de un equipo de bomberos seleccionado en la tabla.
        """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un equipo de bomberos para modificar.")
            return

        # Obtener los datos del equipo seleccionado
        equipo_data = self.tree.item(selected_item, "values")
        
        try:
            referencia = equipo_data[0]
            numero = equipo_data[1]
            area = equipo_data[2]
            ubicacion = equipo_data[3]
            planta = equipo_data[4]
        except IndexError as e:
            messagebox.showerror("Error", f"Error al obtener datos del equipo: {e}")
            return

        # Crear ventana para modificar los datos
        top = ctk.CTkToplevel(self)
        top.title("Modificar Equipo de Bomberos")
        top.geometry("450x500")

        scrollable_frame = ctk.CTkScrollableFrame(top, width=400, height=350)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Campos a editar
        fields = ["referencia", "numero", "area", "ubicacion"]
        values = [referencia, numero, area, ubicacion]
        entries = {}

        for i, (field, value) in enumerate(zip(fields, values)):
            label = ctk.CTkLabel(scrollable_frame, text=field.capitalize(), font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(scrollable_frame)
            entry.insert(0, value)  # Prellenar el campo con el valor actual
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries[field] = entry

        # Campo de planta como dropdown
        planta_label = ctk.CTkLabel(scrollable_frame, text="Planta", font=("Arial", 12))
        planta_label.grid(row=len(fields), column=0, padx=10, pady=5, sticky="w")

        planta_dropdown = ctk.CTkComboBox(
            scrollable_frame, 
            values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],  # Opciones reales
            width=250
        )
        planta_dropdown.set(planta)  # Seleccionar la planta actual
        planta_dropdown.grid(row=len(fields), column=1, padx=10, pady=5)
        entries["planta"] = planta_dropdown

        def guardar_cambios():
            """
            Envía los nuevos datos del equipo a la API para actualizar.
            """
            nuevos_datos = {field: (entry.get() if field != "planta" else planta_dropdown.get()) for field, entry in entries.items()}

            # Validación de datos antes de enviar
            for field, valor in nuevos_datos.items():
                if not valor.strip():
                    messagebox.showerror("Error", f"El campo '{field}' no puede estar vacío.")
                    return

            # Llamar a la API para actualizar los datos
            respuesta = editar_gabinetes_equipo_bomberos_psc_api(referencia, nuevos_datos)
            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", "Equipo de bomberos actualizado correctamente.")
                top.destroy()
                self.cargar_datos_bomberos()  # Refrescar la tabla con los datos actualizados

        guardar_button = ctk.CTkButton(top, text="Guardar Cambios", command=guardar_cambios)
        guardar_button.pack(pady=10)

    def exportar_reporte_gabinete_equipo_bomberos(self):
        """
        Abre una ventana emergente con opciones para exportar la tabla de datos o un reporte completo de extintores inspeccionados.
        """
        top = ctk.CTkToplevel(self)
        top.title("Exportar Reporte de Equipo de Bomberos")
        top.geometry("400x200")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False)) 

        # Etiqueta de descripción
        label = ctk.CTkLabel(
            top,
            text="Seleccione una opción para exportar:",
            font=("Arial", 14)
        )
        label.pack(pady=10)

        # Botón para exportar la tabla de datos
        exportar_tabla_button = ctk.CTkButton(
            top,
            text="Exportar Tabla de Datos",
            command=self.exportar_tabla_completa_bomberos
        )
        exportar_tabla_button.pack(pady=10)

        # Botón para exportar el reporte completo
        def exportar_reporte():
            """
            Exporta el reporte completo de extintores inspeccionados y no inspeccionados.
            """
            planta_seleccionada = self.planta_dropdown_bomberos.get() if self.planta_dropdown_bomberos else self.empresa

            # Mostrar ventana emergente para elegir mes y año
            def seleccionar_filtros():
                """
                Permite al usuario seleccionar el mes y el año para filtrar el reporte.
                """
                filtro_top = ctk.CTkToplevel(top)
                filtro_top.title("Seleccionar Filtros")
                filtro_top.geometry("300x200")
                filtro_top.lift()
                filtro_top.attributes('-topmost', True)
                filtro_top.after(10, lambda: top.attributes('-topmost', False))
                # Campo para el mes
                mes_label = ctk.CTkLabel(filtro_top, text="Mes (Opcional):", font=("Arial", 12))
                mes_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                mes_entry = ctk.CTkEntry(filtro_top, width=150)
                mes_entry.grid(row=0, column=1, padx=10, pady=5)

                # Campo para el año
                ano_label = ctk.CTkLabel(filtro_top, text="Año (Opcional):", font=("Arial", 12))
                ano_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
                ano_entry = ctk.CTkEntry(filtro_top, width=150)
                ano_entry.grid(row=1, column=1, padx=10, pady=5)

                # Botón para confirmar los filtros
                def confirmar_filtros():
                    mes = mes_entry.get()
                    ano = ano_entry.get()

                    # Validar que mes y año sean números si no están vacíos
                    if mes and not mes.isdigit():
                        messagebox.showerror("Error", "El mes debe ser un número.")
                        return
                    if ano and not ano.isdigit():
                        messagebox.showerror("Error", "El año debe ser un número.")
                        return

                    resultado = exportar_reporte_gabinetes_bomberos_psc_api(
                        planta_seleccionada,
                        mes=int(mes) if mes else None,
                        ano=int(ano) if ano else None
                    )

                    if isinstance(resultado, BytesIO):
                        ruta_archivo = filedialog.asksaveasfilename(
                            defaultextension=".xlsx",
                            filetypes=[("Archivos de Excel", "*.xlsx")],
                            title="Guardar archivo como",
                            initialfile=f"Reporte_Gabinetes_Bomberos_PSC_{planta_seleccionada}.xlsx"
                        )
                        if ruta_archivo:
                            with open(ruta_archivo, "wb") as archivo:
                                archivo.write(resultado.getvalue())
                            messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a {ruta_archivo}")
                    else:
                        messagebox.showerror("Error", f"Error al exportar el reporte: {resultado}")

                    filtro_top.destroy()

                confirmar_button = ctk.CTkButton(filtro_top, text="Confirmar", command=confirmar_filtros)
                confirmar_button.grid(row=2, column=0, columnspan=2, pady=10)

            seleccionar_filtros()

        exportar_reporte_button = ctk.CTkButton(
            top,
            text="Exportar Reporte Completo",
            command=exportar_reporte
        )
        exportar_reporte_button.pack(pady=10)


#############################################################################################################
                            #Seccion para Gabientes de mangueras e hidrantes:
#############################################################################################################


    def configurar_filtros_hidrantes(self):
        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        planta_label = ctk.CTkLabel(filtros_frame, text="Seleccionar Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_dropdown_hidrantes = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],
            width=200
        )
        self.planta_dropdown_hidrantes.set("Todos")  # Valor inicial predeterminado
        self.planta_dropdown_hidrantes.pack(side="left", padx=5)
        self.planta_dropdown_hidrantes.bind("<<ComboboxSelected>>", self.filtrar_por_planta_hidrantes)

        # Campo de búsqueda
        self.search_input_hidrantes = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar equipos hidrantes...", width=200)
        self.search_input_hidrantes.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_hidrantes)
        search_button.pack(side="left", padx=5)

    def filtrar_por_planta_hidrantes(self, event=None):
        """
        Maneja el evento de selección de planta en el dropdown para equipos de respiración.
        """
        if self.planta_dropdown_hidrantes:
            planta_seleccionada = self.planta_dropdown_hidrantes.get()
            if planta_seleccionada:
                print(f"[DEBUG] Planta seleccionada: {planta_seleccionada}")
                self.cargar_datos_hidrantes(planta=planta_seleccionada)
            else:
                print("[DEBUG] No se seleccionó una planta válida. Usando 'Todos'.")
                self.cargar_datos_hidrantes(planta="Todos")
        else:
            print("[DEBUG] El dropdown no está definido.")
            self.cargar_datos_hidrantes(planta="Todos")
      
    def cargar_datos_hidrantes(self, planta=None, search=None, page=1):
        """
        Carga los datos de equipos de respiración en la tabla.
        """
        try:
            # Determinar la planta a usar
            planta_filtrada = self.planta_dropdown_hidrantes.get() if self.planta_dropdown_hidrantes.get() else self.empresa

            print(f"[DEBUG] Cargando datos para planta: {planta_filtrada}, búsqueda: {search}, página: {page}")

            # Llamar a la API
            datos_hidrantes = obtener_gabinetes_hidrantes_mangueras_api(planta_filtrada, search=search, page=page)

            if not datos_hidrantes:
                messagebox.showwarning("Advertencia", "No se encontraron datos.")
                return

            # Limpiar la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Agregar los datos a la tabla
            for equipo in datos_hidrantes:
                self.tree.insert("", "end", values=(
                    equipo.get("referencia", ""),
                    equipo.get("numero", ""),
                    equipo.get("area", ""),
                    equipo.get("ubicacion", ""),
                    equipo.get("planta", ""),
                    equipo.get("fecha_ph_manguera"),
                    equipo.get("ultima_actualizacion", "")
                ))

            # Actualizar página actual
            self.current_page = page
            print(f"[DEBUG] Datos cargados para planta: {planta_filtrada}, página: {page}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def mostrar_seccion_Gabinete_hidrantes_mangueras(self, titulo):
        self.title(titulo)  # Cambia el título dinámicamente
        self.extintores_frame.pack(fill="both", expand=True)
        for widget in self.extintores_frame.winfo_children():
            widget.destroy()  # Limpia el contenido actual del frame

        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        # Campo de búsqueda
        search_label = ctk.CTkLabel(filtros_frame, text="Buscar:", font=("Arial", 12))
        search_label.pack(side="left", padx=5)

        self.search_input_hidrantes = ctk.CTkEntry(filtros_frame, placeholder_text="Número, referencia, ubicación", width=180)
        self.search_input_hidrantes.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_hidrantes, width=40)
        search_button.pack(side="left", padx=5)

        # Botón de refrescar tabla
        refresh_button = ctk.CTkButton(filtros_frame, text="Refrescar", command=self.cargar_datos_hidrantes, width=80)
        refresh_button.pack(side="left", padx=5)

        # Botón para agregar extintor
        agregar_button = ctk.CTkButton(filtros_frame, text="Agregar", command=self.agregar_equipo_hidrantes, width=80, fg_color="#4CAF50")
        agregar_button.pack(side="left", padx=5)

        # Botón para modificar extintor
        modificar_button = ctk.CTkButton(filtros_frame, text="Modificar", command=self.modificar_equipo_hidrantes, width=80, fg_color="#FFA500")
        modificar_button.pack(side="left", padx=5)

        # Botón para eliminar extintor
        eliminar_button = ctk.CTkButton(filtros_frame, text="Eliminar", command=self.eliminar_equipo_hidrantes, width=80, fg_color="#FF6347")
        eliminar_button.pack(side="left", padx=5)

        # Dropdown para filtro por planta si es admin
        planta_label = ctk.CTkLabel(filtros_frame, text="Filtrar por Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_dropdown_hidrantes = ttk.Combobox(filtros_frame, values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
        self.planta_dropdown_hidrantes.bind("<<ComboboxSelected>>", self.filtrar_por_planta_hidrantes)
        self.planta_dropdown_hidrantes.pack(side="left", padx=5)

        # Botón para exportar tabla completa
        exportar_button = ctk.CTkButton(filtros_frame, text="Exportar", command=self.exportar_reporte_gabinete_hidrantes, width=80, fg_color="#4CAF50")
        exportar_button.pack(side="left", padx=5)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30, background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E", borderwidth=1)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4B8BBE", foreground="white")
        style.map("Treeview", background=[("selected", "#4B8BBE")])

        columnas = (
            "Referencia", "Numero", "Area", "Ubicacion", "Planta", "Fecha PH",
            "Ultima Actualizacion"
        )

        self.tree = ttk.Treeview(self.extintores_frame, columns=columnas, show='headings', style="Treeview")

        # Configuración de encabezados y ancho de columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.extintores_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        self.tree.pack(side="top", fill="both", expand=True, pady=(5, 5))
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Agregar los botones de paginación
        paginacion_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        paginacion_frame.pack(side="bottom", fill="x", pady=(10, 5))  # Asegúrate de que esté al final

        # Botón para retroceder de página
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Retroceder", command=self.pagina_anterior, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Siguiente >>", command=self.pagina_siguiente, width=100)
        siguiente_button.pack(side="left", padx=5)

        # Cargar datos en la tabla
        self.cargar_datos_hidrantes()

    def buscar_equipo_hidrantes(self):
        """
        Función para buscar equipos de respiración según un término de búsqueda.
        """
        search_term = self.search_input_hidrantes.get()  # Obtener el término de búsqueda desde la entrada
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda.")
            return

        print(f"Término de búsqueda: {search_term}")

        # Determinar la planta
        planta_filtrada = self.planta_dropdown_hidrantes.get() if hasattr(self, "planta_dropdown_hidrantes") else "Todos"

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_hidrantes(planta=planta_filtrada, search=search_term, page=self.current_page)

    def exportar_tabla_completa_hidrantes(self):
        """
        Exporta la tabla completa o filtrada según la planta seleccionada o el privilegio del usuario.
        """
        try:
            # Si el usuario es admin, usa el valor del dropdown; si no, usa la empresa predeterminada
            planta_seleccionada = self.planta_dropdown_hidrantes.get() if self.planta_dropdown_hidrantes else self.empresa

            # Llama a la función de exportación, pasando el filtro de planta
            resultado = exportar_gabinetes_hidrantes_mangueras_api(self.empresa, planta_seleccionada)

            # Mostrar mensajes según el resultado
            if "Archivo Excel guardado exitosamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado durante la exportación: {e}")

    def agregar_equipo_hidrantes(self):
        """
        Abre una ventana emergente para agregar un nuevo gabinete de hidrantes.
        """
        # Crear ventana emergente
        top = ctk.CTkToplevel(self)
        top.title("Agregar Nuevo Gabinete de Hidrantes")
        top.geometry("450x500")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        # Campos de entrada
        campos = ["referencia", "numero", "area", "ubicacion"]
        entradas = {}

        # Crear formulario dinámico
        for idx, campo in enumerate(campos):
            label = ctk.CTkLabel(top, text=campo.replace("_", " ").capitalize(), font=("Arial", 12))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            entry = ctk.CTkEntry(top, width=250)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entradas[campo] = entry

        # Campo de fecha_ph_manguera
        label_fecha_ph = ctk.CTkLabel(top, text="Fecha PH Manguera", font=("Arial", 12))
        label_fecha_ph.grid(row=len(campos), column=0, padx=10, pady=5, sticky="w")

        fecha_entry = ctk.CTkEntry(top, width=250, placeholder_text="YYYY-MM-DD")
        fecha_entry.grid(row=len(campos), column=1, padx=10, pady=5)
        entradas["fecha_ph_manguera"] = fecha_entry

        # Campo de planta como dropdown
        label_planta = ctk.CTkLabel(top, text="Planta", font=("Arial", 12))
        label_planta.grid(row=len(campos) + 1, column=0, padx=10, pady=5, sticky="w")

        planta_options = ["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"]
        planta_entry = ctk.CTkComboBox(top, values=planta_options, width=250)
        planta_entry.grid(row=len(campos) + 1, column=1, padx=10, pady=5)
        planta_entry.set(self.empresa)  # Prellenar con la empresa del usuario (si aplica)

        entradas["planta"] = planta_entry

        def validar_fecha(fecha_texto):
            """
            Valida si una fecha está en formato AAAA-MM-DD.
            """
            try:
                datetime.strptime(fecha_texto, "%Y-%m-%d")
                return True
            except ValueError:
                return False

        def guardar_datos():
            """
            Guarda los datos del nuevo gabinete y llama a la API para agregarlo.
            """
            # Obtener los valores ingresados
            datos = {campo: entrada.get() for campo, entrada in entradas.items()}
            datos["planta"] = planta_entry.get()  # Planta seleccionada

            # Validar que todos los campos están llenos
            for campo, valor in datos.items():
                if not valor:
                    messagebox.showerror("Error", f"El campo '{campo}' es obligatorio.")
                    return

            # Validar formato de fecha para fecha_ph_manguera
            if not validar_fecha(datos["fecha_ph_manguera"]):
                messagebox.showerror("Error", "La fecha PH Manguera debe estar en el formato AAAA-MM-DD.")
                return

            # Llamar a la API para agregar el gabinete
            respuesta = agregar_gabinete_hidrantes_mangueras(datos)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", respuesta.get("message", "El gabinete fue agregado exitosamente."))
                top.destroy()  # Cerrar ventana emergente
                self.cargar_datos_hidrantes()  # Refrescar la tabla

        # Botón para guardar los datos
        guardar_button = ctk.CTkButton(top, text="Guardar", command=guardar_datos)
        guardar_button.grid(row=len(campos) + 2, column=0, columnspan=2, pady=20)

    def eliminar_equipo_hidrantes(self):
        """
        Elimina un gabinete de bomberos seleccionado en la tabla.
        """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un gabinete para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar el gabinete seleccionado?")
        if confirm:
            # Obtener la referencia del equipo seleccionado
            equipo_data = self.tree.item(selected_item, "values")
            try:
                referencia = equipo_data[0]  # Se asume que la referencia está en la primera columna
            except IndexError:
                messagebox.showerror("Error", "No se pudo obtener la referencia del gabinete.")
                return

            # Llamar a la API para eliminar el gabinete
            respuesta = eliminar_gabinete_hidrantes_mangueras_api(referencia)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", f"El gabinete con referencia '{referencia}' fue eliminado exitosamente.")
                self.cargar_datos_hidrantes()  # Refrescar la tabla

    def modificar_equipo_hidrantes(self):
        """
        Abre una ventana emergente para modificar los datos de un equipo de bomberos seleccionado en la tabla.
        """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un equipo de bomberos para modificar.")
            return

        # Obtener los datos del equipo seleccionado
        equipo_data = self.tree.item(selected_item, "values")
        
        try:
            referencia = equipo_data[0]
            numero = equipo_data[1]
            area = equipo_data[2]
            ubicacion = equipo_data[3]
            planta = equipo_data[4]
            fecha_ph_manguera = equipo_data[5]
        except IndexError as e:
            messagebox.showerror("Error", f"Error al obtener datos del equipo: {e}")
            return

        # Crear ventana para modificar los datos
        top = ctk.CTkToplevel(self)
        top.title("Modificar Equipo de Bomberos")
        top.geometry("450x500")

        scrollable_frame = ctk.CTkScrollableFrame(top, width=400, height=350)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Campos a editar
        fields = ["referencia", "numero", "area", "ubicacion", "fecha_ph_manguera"]
        values = [referencia, numero, area, ubicacion, fecha_ph_manguera]
        entries = {}

        for i, (field, value) in enumerate(zip(fields, values)):
            label = ctk.CTkLabel(scrollable_frame, text=field.capitalize(), font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(scrollable_frame)
            entry.insert(0, value)  # Prellenar el campo con el valor actual
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries[field] = entry

        # Campo de planta como dropdown
        planta_label = ctk.CTkLabel(scrollable_frame, text="Planta", font=("Arial", 12))
        planta_label.grid(row=len(fields), column=0, padx=10, pady=5, sticky="w")

        planta_dropdown = ctk.CTkComboBox(
            scrollable_frame, 
            values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],  # Opciones reales
            width=250
        )
        planta_dropdown.set(planta)  # Seleccionar la planta actual
        planta_dropdown.grid(row=len(fields), column=1, padx=10, pady=5)
        entries["planta"] = planta_dropdown

        def guardar_cambios():
            """
            Envía los nuevos datos del equipo a la API para actualizar.
            """
            nuevos_datos = {field: (entry.get() if field != "planta" else planta_dropdown.get()) for field, entry in entries.items()}

            # Validación de datos antes de enviar
            for field, valor in nuevos_datos.items():
                if not valor.strip():
                    messagebox.showerror("Error", f"El campo '{field}' no puede estar vacío.")
                    return

            # Llamar a la API para actualizar los datos
            respuesta = editar_gabinetes_hidrantes_mangueras_api(referencia, nuevos_datos)
            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", "Equipo de bomberos actualizado correctamente.")
                top.destroy()
                self.cargar_datos_hidrantes()  # Refrescar la tabla con los datos actualizados

        guardar_button = ctk.CTkButton(top, text="Guardar Cambios", command=guardar_cambios)
        guardar_button.pack(pady=10)

    def exportar_reporte_gabinete_hidrantes(self):
        """
        Abre una ventana emergente con opciones para exportar la tabla de datos o un reporte completo de extintores inspeccionados.
        """
        top = ctk.CTkToplevel(self)
        top.title("Exportar Reporte de Mangueras")
        top.geometry("400x200")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        # Etiqueta de descripción
        label = ctk.CTkLabel(
            top,
            text="Seleccione una opción para exportar:",
            font=("Arial", 14)
        )
        label.pack(pady=10)

        # Botón para exportar la tabla de datos
        exportar_tabla_button = ctk.CTkButton(
            top,
            text="Exportar Tabla de Datos",
            command=self.exportar_tabla_completa_hidrantes
        )
        exportar_tabla_button.pack(pady=10)

        # Botón para exportar el reporte completo
        def exportar_reporte():
            """
            Exporta el reporte completo de extintores inspeccionados y no inspeccionados.
            """
            planta_seleccionada = self.planta_dropdown_hidrantes.get() if self.planta_dropdown_hidrantes else self.empresa

            # Mostrar ventana emergente para elegir mes y año
            def seleccionar_filtros():
                """
                Permite al usuario seleccionar el mes y el año para filtrar el reporte.
                """
                filtro_top = ctk.CTkToplevel(top)
                filtro_top.title("Seleccionar Filtros")
                filtro_top.geometry("300x200")
                filtro_top.lift()
                filtro_top.attributes('-topmost', True)
                filtro_top.after(10, lambda: top.attributes('-topmost', False))
                # Campo para el mes
                mes_label = ctk.CTkLabel(filtro_top, text="Mes (Opcional):", font=("Arial", 12))
                mes_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                mes_entry = ctk.CTkEntry(filtro_top, width=150)
                mes_entry.grid(row=0, column=1, padx=10, pady=5)

                # Campo para el año
                ano_label = ctk.CTkLabel(filtro_top, text="Año (Opcional):", font=("Arial", 12))
                ano_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
                ano_entry = ctk.CTkEntry(filtro_top, width=150)
                ano_entry.grid(row=1, column=1, padx=10, pady=5)

                # Botón para confirmar los filtros
                def confirmar_filtros():
                    mes = mes_entry.get()
                    ano = ano_entry.get()

                    # Validar que mes y año sean números si no están vacíos
                    if mes and not mes.isdigit():
                        messagebox.showerror("Error", "El mes debe ser un número.")
                        return
                    if ano and not ano.isdigit():
                        messagebox.showerror("Error", "El año debe ser un número.")
                        return

                    resultado = exportar_reporte_hidrantes_mangueras_psc_api(
                        planta_seleccionada,
                        mes=int(mes) if mes else None,
                        ano=int(ano) if ano else None
                    )

                    if isinstance(resultado, BytesIO):
                        ruta_archivo = filedialog.asksaveasfilename(
                            defaultextension=".xlsx",
                            filetypes=[("Archivos de Excel", "*.xlsx")],
                            title="Guardar archivo como",
                            initialfile=f"Reporte_Gabinetes_Mangueras_Hidrantes_{planta_seleccionada}.xlsx"
                        )
                        if ruta_archivo:
                            with open(ruta_archivo, "wb") as archivo:
                                archivo.write(resultado.getvalue())
                            messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a {ruta_archivo}")
                    else:
                        messagebox.showerror("Error", f"Error al exportar el reporte: {resultado}")

                    filtro_top.destroy()

                confirmar_button = ctk.CTkButton(filtro_top, text="Confirmar", command=confirmar_filtros)
                confirmar_button.grid(row=2, column=0, columnspan=2, pady=10)

            seleccionar_filtros()

        exportar_reporte_button = ctk.CTkButton(
            top,
            text="Exportar Reporte Completo",
            command=exportar_reporte
        )
        exportar_reporte_button.pack(pady=10)




    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar sesión?")
        if respuesta:
            self.destroy()

if __name__ == "__main__":
    user_data = {"NombreUsuario": "Gerardo Daniel Lopez Lara"}  # Sustituir por datos reales del usuario
    privilegio = "admin"  # Cambiar según el privilegio del usuario
    app = GuiInicial(user_data, privilegio, "Time or Time")
    app.mainloop()

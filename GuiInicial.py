import customtkinter as ctk
from tkinter import ttk, messagebox, Toplevel
import tkinter.messagebox as messagebox
from DB.ConexionExtintores import *
from datetime import datetime
from io import BytesIO
import datetime

# Configuración para el tema del sistema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
x = datetime.datetime.now()

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
        self.planta_dropdown_ordenes_serivcio = None
        self.tiempo_real_dropdown = None
        self.search_input = None  # Campo de búsqueda
        self.search_input_resp = None
        self.search_input_bomberos = None
        self.search_input_hidrantes = None
        self.search_tiempo_real_dropdown = None
        self.search_ordenes_servicio = None
        self.dia_dropdown_inspeccionados = x.day
        self.mes_dropdown_inspeccionados = x.month
        self.ano_dropdown_inspeccionados = x.year
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

        ctk.CTkLabel(nav_frame, text="Extintores", font=("Arial", 16, "bold"), text_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#333333").pack(pady=(10, 10))
    
        linea_superior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_superior.pack(pady=(0, 0))
        extintores_button = ctk.CTkButton(nav_frame, text="Extintores Generales", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=lambda: self.mostrar_seccion("Extintores Generales"),
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=40, hover_color="#1e1d1d" if ctk.get_appearance_mode() == "Dark" else "#f4f4f4", 
        corner_radius=0)
        extintores_button.pack(pady=(0,0))
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 0))


        inspecciones_tiempo_button = ctk.CTkButton(nav_frame, text="Inspecciones", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=lambda: self.mostrar_seccion_inspecciones_hechas("Extintores Inspeccionados"),
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=40, hover_color="#1e1d1d" if ctk.get_appearance_mode() == "Dark" else "#f4f4f4", 
        corner_radius=0)
        inspecciones_tiempo_button.pack(pady=0)
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 30))
        
        ctk.CTkLabel(nav_frame, text="Gabinetes", font=("Arial", 16, "bold"), text_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#333333").pack(pady=(10, 10))

        linea_superior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_superior.pack(pady=(0, 0))
        respiracion_button = ctk.CTkButton(nav_frame, text="Equipos de Respiracion", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=lambda: self.mostrar_seccion_Gabinete_Equipo_Respiración("Equipo de respiracion"),
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=40, hover_color="#1e1d1d" if ctk.get_appearance_mode() == "Dark" else "#f4f4f4", 
        corner_radius=0)
        respiracion_button.pack(pady=0)
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 0))

        bomberos_button = ctk.CTkButton(nav_frame, text="Equipo de Bomberos", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=lambda: self.mostrar_seccion_Gabinete_Equipo_Bomberos_PSC("Equipos de bomberos"),
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=40, hover_color="#1e1d1d" if ctk.get_appearance_mode() == "Dark" else "#f4f4f4", 
        corner_radius=0)
        bomberos_button.pack(pady=0)
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 0))
        
        mangueras_button = ctk.CTkButton(nav_frame, text="Mangueras e Hidrantes", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=lambda: self.mostrar_seccion_Gabinete_hidrantes_mangueras("Mangueras e hidrantes"),
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=40, hover_color="#1e1d1d" if ctk.get_appearance_mode() == "Dark" else "#f4f4f4", 
        corner_radius=0)
        mangueras_button.pack(pady=0)
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 0))
                
        inspecciones_tiempo_button = ctk.CTkButton(nav_frame, text="Inspecciones", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=lambda: self.mostrar_seccion_inspecciones_hechas("Inspecciones"),
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=40, hover_color="#1e1d1d" if ctk.get_appearance_mode() == "Dark" else "#f4f4f4", 
        corner_radius=0)
        inspecciones_tiempo_button.pack(pady=0)
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 20))

        ctk.CTkLabel(nav_frame, text="Extras", font=("Arial", 16, "bold"), text_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#333333").pack(pady=(10, 10))
        linea_superior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_superior.pack(pady=(0, 0))
        
        reporte_mensual_completo = ctk.CTkButton(nav_frame, text="Reporte Completo Mensual", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=self.reporte_completo_mensual_planta,
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=25, hover_color="#1e1d1d" if ctk.get_appearance_mode() == "Dark" else "#f4f4f4", 
        corner_radius=0)
        reporte_mensual_completo.pack(pady=0)
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 0))
        
        ordenes_servicio = ctk.CTkButton(nav_frame, text="Ordenes de servicio", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=lambda: self.mostrar_seccion_ordenes_servicio("Ordenes de servicio"),
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=25, hover_color="#1e1d1d" if ctk.get_appearance_mode() == "Dark" else "#f4f4f4", 
        corner_radius=0)
        ordenes_servicio.pack(pady=0)
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 0))
                
        
        logout_button = ctk.CTkButton(nav_frame, text="Cerrar Sesion", 
        text_color="#D9D9D9" if ctk.get_appearance_mode() == "Dark" else "#3C3C3C",  
        command=lambda: self.cerrar_sesion(),
        width=220, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9", 
        height=25, hover_color="#e73636", 
        corner_radius=0)
        logout_button.pack(pady=0)
        linea_inferior = ctk.CTkFrame(nav_frame, height=2, width=220, fg_color="#666666")
        linea_inferior.pack(pady=(0, 0))
        
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
        siguiente_button.pack(side="right", padx=5)

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
        top.lift()
        top.attributes('-topmost', True)  # Mantiene la ventana al frente
        top.after(100, lambda: top.attributes('-topmost', False))  # Permite interacción con otras ventanas después de 100ms

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
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Retroceder", command=self.pagina_anterior_resp, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Siguiente >>", command=self.pagina_siguiente_resp, width=100)
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

    def pagina_anterior_resp(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.cargar_datos_resp(page=self.current_page)

    def pagina_siguiente_resp(self):
        # Incrementar la página actual
        self.current_page += 1

        # Llamar a la función cargar_datos_extintores con la nueva página
        self.cargar_datos_resp(page=self.current_page)

        # Opcional: Deshabilitar el botón si se alcanzó la última página (según los datos de tu API)
        # if self.current_page == self.total_pages:
        #     self.siguiente_button.config(state="disabled")

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
        self.search_input_bomberos = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar equipos de bomberos...", width=200)
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
                messagebox.showwarning("Advertencia", "No se encontraron datos de equipos de bomberos.")
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
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Retroceder", command=self.pagina_anterior_bomb, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Siguiente >>", command=self.pagina_siguiente_bomb, width=100)
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

    def pagina_anterior_bomb(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.cargar_datos_bomberos(page=self.current_page)

    def pagina_siguiente_bomb(self):
        self.current_page += 1
        self.cargar_datos_bomberos(page=self.current_page)

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
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Retroceder", command=self.pagina_anterior_hidrantes, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Siguiente >>", command=self.pagina_siguiente_hidrantes, width=100)
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
                datetime.datetime.strptime(fecha_texto, "%Y-%m-%d")
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
   
    def pagina_anterior_hidrantes(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.cargar_datos_hidrantes(page=self.current_page)

    def pagina_siguiente_hidrantes(self):
        self.current_page += 1
        self.cargar_datos_hidrantes(page=self.current_page)


#############################################################################################################
            #Seccion para mostrar en tiempo real los extintores que se inspeccionan:
#############################################################################################################


    def configurar_filtros_inspeccionados(self):
        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        planta_label = ctk.CTkLabel(filtros_frame, text="Seleccionar Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.tiempo_real_dropdown = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],
            width=200
        )
        self.tiempo_real_dropdown.set("Todos")  # Valor inicial predeterminado
        self.tiempo_real_dropdown.pack(side="left", padx=5)
        self.tiempo_real_dropdown.bind("<<ComboboxSelected>>", self.filtrar_por_planta_inspeccionados)

        # Campo de búsqueda
        self.search_tiempo_real_dropdown = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar equipos hidrantes...", width=200)
        self.search_tiempo_real_dropdown.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_inspeccionados)
        search_button.pack(side="left", padx=5)

    def filtrar_por_planta_inspeccionados(self, event=None):
        """
        Maneja el evento de selección de planta en el dropdown.
        """
        planta_seleccionada = self.tiempo_real_dropdown.get() if self.tiempo_real_dropdown else "Todos"
        mes = self.mes_dropdown_inspeccionados.get() if self.mes_dropdown_inspeccionados else datetime.datetime.now().year
        ano = self.ano_dropdown_inspeccionados.get() if self.ano_dropdown_inspeccionados else datetime.datetime.now().month
        search = self.search_input.get() if self.search_input else None

        print(f"[DEBUG] Filtrando: Planta={planta_seleccionada}, Mes={mes}, Año={ano}, Search={search}")
        self.cargar_datos_extintores_visualizador(planta=planta_seleccionada, mes=mes, ano=ano, search=search)

    def filtrar_por_dia_inspeccionados(self, event=None):
        """
        Maneja el evento de selección del mes en el dropdown.
        """
        dia_seleccionado = self.dia_dropdown_inspeccionados.get() if self.dia_dropdown_inspeccionados else datetime.datetime.now().day
        planta = self.tiempo_real_dropdown.get() if self.tiempo_real_dropdown else "Todos"
        mes = self.mes_dropdown_inspeccionados.get() if self.mes_dropdown_inspeccionados else datetime.datetime.now().month
        ano = self.ano_dropdown_inspeccionados.get() if self.ano_dropdown_inspeccionados else datetime.datetime.now().year
        search = self.search_input.get() if self.search_input else None

        print(f"[DEBUG] Filtrando: Planta={planta}, Dia={dia_seleccionado}, Mes={mes}, Año={ano}, Search={search}")
        self.cargar_datos_extintores_visualizador(planta=planta, dia=dia_seleccionado, mes=mes, ano=ano, search=search)

    def filtrar_por_mes_inspeccionados(self, event=None):
        """
        Maneja el evento de selección del mes en el dropdown.
        """
        mes_seleccionado = self.mes_dropdown_inspeccionados.get() if self.mes_dropdown_inspeccionados else datetime.datetime.now().month
        planta = self.tiempo_real_dropdown.get() if self.tiempo_real_dropdown else "Todos"
        dia = self.dia_dropdown_inspeccionados.get() if self.dia_dropdown_inspeccionados else datetime.datetime.now().year
        ano = self.ano_dropdown_inspeccionados.get() if self.ano_dropdown_inspeccionados else datetime.datetime.now().year
        search = self.search_input.get() if self.search_input else None

        print(f"[DEBUG] Filtrando: Planta={planta}, Dia={dia}, Mes={mes_seleccionado}, Año={ano}, Search={search}")
        self.cargar_datos_extintores_visualizador(planta=planta, dia=dia, mes=mes_seleccionado, ano=ano, search=search)

    def filtrar_por_ano_inspeccionados(self, event=None):
        """
        Maneja el evento de selección del año en el dropdown.
        """
        ano_seleccionado = self.ano_dropdown_inspeccionados.get() if self.ano_dropdown_inspeccionados else datetime.datetime.now().year
        planta = self.tiempo_real_dropdown.get() if self.tiempo_real_dropdown else "Todos"
        mes = self.mes_dropdown_inspeccionados.get() if self.mes_dropdown_inspeccionados else datetime.datetime.now().month
        dia = self.dia_dropdown_inspeccionados.get() if self.dia_dropdown_inspeccionados else datetime.datetime.now().month
        search = self.search_input.get() if self.search_input else None

        print(f"[DEBUG] Filtrando: Planta={planta}, Dia={dia}, Mes={mes}, Año={ano_seleccionado}, Search={search}")
        self.cargar_datos_extintores_visualizador(planta=planta, dia=dia, mes=mes, ano=ano_seleccionado, search=search)

    def cargar_datos_extintores_visualizador(self, planta=None, dia=None, mes=None, ano=None, page=1, search=None):
        """Carga los datos de inspecciones en la tabla desde la API de manera eficiente."""
        try:
            # Obtener valores actuales de los filtros si no se pasaron como parámetros
            planta_filtrada = planta or (self.tiempo_real_dropdown.get() if self.tiempo_real_dropdown else "Todos")
            dia_filtrado = dia or (self.dia_dropdown_inspeccionados.get() if self.dia_dropdown_inspeccionados else datetime.datetime.now().day)
            mes_filtrado = mes or (self.mes_dropdown_inspeccionados.get() if self.mes_dropdown_inspeccionados else datetime.datetime.now().month)
            ano_filtrado = ano or (self.ano_dropdown_inspeccionados.get() if self.ano_dropdown_inspeccionados else datetime.datetime.now().year)

            print(f"[DEBUG] Cargando datos: Planta={planta_filtrada}, Dia={dia_filtrado}, Mes={mes_filtrado}, Año={ano_filtrado}, Página={page}")

            # Obtener los datos con filtros y paginación
            datos_extintores = obtener_extintores_gabinetes_inspeccionados_en_linea_api(
                planta_filtrada, dia=dia_filtrado, mes=mes_filtrado, ano=ano_filtrado, page=page, search=search
            )

            if not datos_extintores or not isinstance(datos_extintores, list):
                print("[DEBUG] No se encontraron datos de extintores.")
                return  # Evita el uso de messagebox para no bloquear la UI

            # Limpiar solo si hay nuevos datos
            if len(self.tree.get_children()) > 0:
                self.tree.delete(*self.tree.get_children())

            # Insertar datos en la tabla en un solo ciclo
            for extintor in datos_extintores:
                self.tree.insert("", "end", values=(
                    extintor.get("referencia", ""),
                    extintor.get("fecha_inspeccionado", ""),
                    extintor.get("inspeccionista", ""),
                    extintor.get("planta", ""),
                    extintor.get("area", ""),
                    extintor.get("numerodeextintor", ""),
                    extintor.get("ubicacion_extintor", ""),
                    extintor.get("tipo", ""),
                    extintor.get("capacidad_kg", ""),
                    extintor.get("fecha_recarga", ""),
                    extintor.get("fecha_vencimiento", ""),
                    extintor.get("fecha_ultima_prueba", ""),
                    extintor.get("fecha_fabricacion", ""),
                    extintor.get("presion", ""),
                    extintor.get("manometro", ""),
                    extintor.get("seguro", ""),
                    extintor.get("etiquetas_datos", ""),
                    extintor.get("senalamientos", ""),
                    extintor.get("circulo_numero", ""),
                    extintor.get("pintura", ""),
                    extintor.get("manguera", ""),
                    extintor.get("boquilla", ""),
                    extintor.get("golpes_danos", ""),
                    extintor.get("obstruido", ""),
                    extintor.get("funda", ""),
                    extintor.get("condicionllanta", ""),
                    extintor.get("comentarios", ""),
                ))

            # Actualizar página actual
            self.current_page = page
            print(f"[DEBUG] Datos cargados para planta: {planta_filtrada}, página: {page}, dia: {dia_filtrado}, mes: {mes_filtrado}, año: {ano_filtrado}, SEARCH: {search}")

        except Exception as e:
            print(f"[ERROR] {e}")  # Evitar messagebox para no bloquear la UI

    def pagina_siguiente_extintores_inspeccionados(self):
        """Avanza a la siguiente página y recarga los datos."""
        self.current_page += 1  # Aumenta el número de página
        print(f"[DEBUG] Página siguiente: {self.current_page}")  # Depuración
        self.cargar_datos_extintores_visualizador(page=self.current_page)

    def pagina_anterior_extintores_inspeccionados(self):
        """Retrocede una página (si no es la primera) y recarga los datos."""
        if self.current_page > 1:
            self.current_page -= 1  # Reduce el número de página
            print(f"[DEBUG] Página anterior: {self.current_page}")  # Depuración
            self.cargar_datos_extintores_visualizador(page=self.current_page)
        else:
            print("[DEBUG] Ya estás en la primera página.")
        
    def mostrar_seccion_inspecciones_hechas(self, titulo):
        self.title(titulo)  # Cambia el título dinámicamente
        self.extintores_frame.pack(fill="both", expand=True)
        for widget in self.extintores_frame.winfo_children():
            widget.destroy()  # Limpia el contenido actual del frame

        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        # Campo de búsqueda
        search_label = ctk.CTkLabel(filtros_frame, text="Buscar:", font=("Arial", 12))
        search_label.pack(side="left", padx=5)

        self.search_tiempo_real_dropdown = ctk.CTkEntry(filtros_frame, placeholder_text="Número, referencia, ubicación", width=180)
        self.search_tiempo_real_dropdown.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_inspeccionados, width=40)
        search_button.pack(side="left", padx=5)

        # Botón de refrescar tabla
        refresh_button = ctk.CTkButton(filtros_frame, text="Refrescar", command=self.cargar_datos_extintores_visualizador, width=80)
        refresh_button.pack(side="left", padx=5)

        # Botón para eliminar extintor
        eliminar_button = ctk.CTkButton(filtros_frame, text="Eliminar", command=self.eliminar_equipo_inspeccionados, width=80, fg_color="#FF6347")
        eliminar_button.pack(side="left", padx=5)

        # Dropdown para filtro por planta si es admin
        planta_label = ctk.CTkLabel(filtros_frame, text="Filtrar por Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.tiempo_real_dropdown = ttk.Combobox(filtros_frame, values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
        self.tiempo_real_dropdown.bind("<<ComboboxSelected>>", self.filtrar_por_planta_inspeccionados)
        self.tiempo_real_dropdown.pack(side="left", padx=5)
        
        # Botón para exportar tabla completa
        exportar_button = ctk.CTkButton(filtros_frame, text="Exportar", command=self.exportar_reporte_inspeccionados, width=80, fg_color="#4CAF50")
        exportar_button.pack(side="right", padx=5)
        
        filtros_frame_abajo = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame_abajo.pack(fill="x", pady=(5, 10))
        
        # Dropdown para filtro por mes 
        dia_dropdown_inspeccionados = ctk.CTkLabel(filtros_frame_abajo, text="Dia:", font=("Arial", 12))
        dia_dropdown_inspeccionados.pack(side="left", padx=5)
        
        self.dia_dropdown_inspeccionados = ttk.Combobox(filtros_frame_abajo, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
                                                                                     "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26",
                                                                                     "27", "28", "29", "30", "31"], state="readonly", width=6)
        self.dia_dropdown_inspeccionados.bind("<<ComboboxSelected>>", self.filtrar_por_mes_inspeccionados)
        self.dia_dropdown_inspeccionados.pack(side="left", padx=5)
        
        
        # Dropdown para filtro por mes 
        mes_dropdown_inspeccionados = ctk.CTkLabel(filtros_frame_abajo, text="Mes:", font=("Arial", 12))
        mes_dropdown_inspeccionados.pack(side="left", padx=5)
        
        self.mes_dropdown_inspeccionados = ttk.Combobox(filtros_frame_abajo, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], state="readonly", width=6)
        self.mes_dropdown_inspeccionados.bind("<<ComboboxSelected>>", self.filtrar_por_mes_inspeccionados)
        self.mes_dropdown_inspeccionados.pack(side="left", padx=5)
        
        # Dropdown para filtro por año
        ano_dropdown_inspeccionados = ctk.CTkLabel(filtros_frame_abajo, text="Año:", font=("Arial", 12))
        ano_dropdown_inspeccionados.pack(side="left", padx=5)
        
        self.ano_dropdown_inspeccionados = ttk.Combobox(filtros_frame_abajo, values=["2025", "2026", "2027"], state="readonly", width=6)
        self.ano_dropdown_inspeccionados.bind("<<ComboboxSelected>>", self.filtrar_por_ano_inspeccionados)
        self.ano_dropdown_inspeccionados.pack(side="left", padx=5)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30, background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E", borderwidth=1)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4B8BBE", foreground="white")
        style.map("Treeview", background=[("selected", "#4B8BBE")])

        boton_izquierda = ctk.CTkButton(self.extintores_frame, text="<",text_color="white" if ctk.get_appearance_mode() == "Dark" else "black",  command=lambda: self.mover_tabla_horizontalmente(-150), width=20, height=550, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9")
        boton_izquierda.pack(side="left", padx=5, pady=5)
        
        columnas = (
            "Referencia", "Fecha inspeccionado", "Inspeccionista", "Planta", "Area", "Numero de extintor", "Ubicacion de extintor",
            "Tipo", "Capacidad en kg", "Fecha de recarga", "Fecha de vencimiento", "Fecha ph", "Fecha fabricacion",
            "Presion", "Manometro", "Seguro", "Etiquetas de datos", "Señalamientos",
            "Circulo y numero", "Pintura", "Manguera", "Boquilla", "Golpes o daños", "Obstruido", 
            "Funda", "Condicion de llanta", "Comentarios"
        )

        self.tree = ttk.Treeview(self.extintores_frame, columns=columnas, show='headings', style="Treeview")

        # Configuración de encabezados y ancho de columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        boton_derecha = ctk.CTkButton(self.extintores_frame, text=">",text_color="white" if ctk.get_appearance_mode() == "Dark" else "black",  command=lambda: self.mover_tabla_horizontalmente(150), width=20, height=550, fg_color="#3C3C3C" if ctk.get_appearance_mode() == "Dark" else "#D9D9D9")
        boton_derecha.pack(side="right", padx=5, pady=5)


        self.tree.pack(side="top", fill="both", expand=True, pady=(5, 5))


        # Agregar los botones de paginación
        paginacion_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        paginacion_frame.pack(side="bottom", fill="x", pady=(10, 5))  # Asegúrate de que esté al final

        # Botón para retroceder de página
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Pagina", command=self.pagina_anterior_extintores_inspeccionados, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Pagina >>", command=self.pagina_siguiente_extintores_inspeccionados, width=100)
        siguiente_button.pack(side="right", padx=5)
        
        # Cargar datos en la tabla
        self.cargar_datos_extintores_visualizador()
        
    def mover_tabla_horizontalmente(self, direction):
        """ Mueve la tabla horizontalmente al hacer clic en los botones. """
        self.tree.xview_scroll(direction, "units")  # Mueve la vista de la tabla por unidades

    def buscar_equipo_inspeccionados(self):
        """
        Función para buscar equipos de respiración según un término de búsqueda.
        """
        search_term = self.search_tiempo_real_dropdown.get()  # Obtener el término de búsqueda desde la entrada
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda.")
            return

        print(f"Término de búsqueda: {search_term}")

        # Determinar la planta
        planta_filtrada = self.tiempo_real_dropdown.get() if hasattr(self, "tiempo_real_dropdown") else "Todos"

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_extintores_visualizador(planta=planta_filtrada, search=search_term, page=self.current_page)

    def agregar_equipo_inspeccionados(self):
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
                datetime.datetime.strptime(fecha_texto, "%Y-%m-%d")
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

    def eliminar_equipo_inspeccionados(self):
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

    def modificar_equipo_inspeccionados(self):
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

    def exportar_reporte_inspeccionados(self):
        """Abre una ventana emergente con opciones para exportar los reportes de inspecciones."""
        top = ctk.CTkToplevel(self)
        top.title("Exportar Inspecciones de Extintores")
        top.geometry("400x200")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        label = ctk.CTkLabel(top, text="Seleccione una opción para exportar:", font=("Arial", 14))
        label.pack(pady=10)

        def seleccionar_filtros(callback):
            """Ventana emergente para seleccionar filtros (mes, año y planta)."""
            filtro_top = ctk.CTkToplevel(top)
            filtro_top.title("Seleccionar Filtros")
            filtro_top.geometry("300x200")
            filtro_top.lift()
            filtro_top.attributes('-topmost', True)
            filtro_top.after(10, lambda: filtro_top.attributes('-topmost', False))

            ctk.CTkLabel(filtro_top, text="Mes (Opcional):", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
            mes_entry = ctk.CTkEntry(filtro_top, width=150)
            mes_entry.grid(row=0, column=1, padx=10, pady=5)

            ctk.CTkLabel(filtro_top, text="Año (Opcional):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
            ano_entry = ctk.CTkEntry(filtro_top, width=150)
            ano_entry.grid(row=1, column=1, padx=10, pady=5)

            ctk.CTkLabel(filtro_top, text="Planta (Obligatorio):", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
            planta_drop = ttk.Combobox(filtro_top, values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
            planta_drop.grid(row=2, column=1, padx=10, pady=5, sticky="w")

            def confirmar_filtros():
                mes = mes_entry.get()
                ano = ano_entry.get()
                planta = planta_drop.get()

                if not planta:
                    messagebox.showerror("Error", "Debe seleccionar una planta.")
                    return
                if mes and not mes.isdigit():
                    messagebox.showerror("Error", "El mes debe ser un número.")
                    return
                if ano and not ano.isdigit():
                    messagebox.showerror("Error", "El año debe ser un número.")
                    return

                callback(planta, int(mes) if mes else None, int(ano) if ano else None)
                filtro_top.destroy()

            ctk.CTkButton(filtro_top, text="Confirmar", command=confirmar_filtros).grid(row=3, column=0, columnspan=2, pady=10)

        def exportar_reporte(tipo):
            """Exporta el reporte según el tipo de inspección."""
            def generar_reporte(planta, mes, ano):
                if tipo == "inspeccionados":
                    resultado = obtener_extintores_inspeccionados_excel(planta, mes, ano)
                else:  # Aquí aseguramos que realmente se llame la función correcta
                    resultado = obtener_extintores_no_inspeccionados_excel(planta, mes, ano)

                fecha = datetime.datetime.now().strftime("%Y-%m-%d")
                nombre_archivo = f"Extintores_{tipo.capitalize()}_{planta}_{fecha}.xlsx"

                if isinstance(resultado, BytesIO):
                    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")], title="Guardar archivo como", initialfile=nombre_archivo)
                    if ruta_archivo:
                        with open(ruta_archivo, "wb") as archivo:
                            archivo.write(resultado.getvalue())
                        messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a {ruta_archivo}")
                else:
                    messagebox.showerror("Error", f"No hay extintores pendientes de este mes y año")

            seleccionar_filtros(generar_reporte)

        ctk.CTkButton(top, text="Exportar Extintores No Inspeccionados", command=lambda: exportar_reporte("no_inspeccionados")).pack(pady=10)
        ctk.CTkButton(top, text="Exportar Extintores Inspeccionados", command=lambda: exportar_reporte("inspeccionados")).pack(pady=10)


#############################################################################################################
                                    #Descarga de reporte completo mensual
#############################################################################################################
    def reporte_completo_mensual_planta(self):
        """Abre una ventana emergente con opciones para exportar los reportes de inspecciones."""
        top = ctk.CTkToplevel(self)
        top.title("Exportar Reporte Mensual")
        top.geometry("400x200")
        top.lift()
        top.attributes('-topmost', True)
        top.after(10, lambda: top.attributes('-topmost', False))

        label = ctk.CTkLabel(top, text="Seleccione una opción para exportar:", font=("Arial", 14))
        label.pack(pady=10)

        def seleccionar_filtros(callback):
            """Ventana emergente para seleccionar filtros (mes, año y planta)."""
            filtro_top = ctk.CTkToplevel(top)
            filtro_top.title("Seleccionar Filtros")
            filtro_top.geometry("300x200")
            filtro_top.lift()
            filtro_top.attributes('-topmost', True)
            filtro_top.after(10, lambda: filtro_top.attributes('-topmost', False))

            ctk.CTkLabel(filtro_top, text="Mes (Opcional):", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
            mes_entry = ctk.CTkEntry(filtro_top, width=150)
            mes_entry.grid(row=0, column=1, padx=10, pady=5)

            ctk.CTkLabel(filtro_top, text="Año (Opcional):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
            ano_entry = ctk.CTkEntry(filtro_top, width=150)
            ano_entry.grid(row=1, column=1, padx=10, pady=5)

            ctk.CTkLabel(filtro_top, text="Planta (Obligatorio):", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
            planta_drop = ttk.Combobox(filtro_top, values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
            planta_drop.grid(row=2, column=1, padx=10, pady=5, sticky="w")

            def confirmar_filtros():
                mes = mes_entry.get()
                ano = ano_entry.get()
                planta = planta_drop.get()

                if not planta:
                    messagebox.showerror("Error", "Debe seleccionar una planta.")
                    return
                if mes and not mes.isdigit():
                    messagebox.showerror("Error", "El mes debe ser un número.")
                    return
                if ano and not ano.isdigit():
                    messagebox.showerror("Error", "El año debe ser un número.")
                    return

                callback(planta, int(mes) if mes else None, int(ano) if ano else None)
                filtro_top.destroy()

            ctk.CTkButton(filtro_top, text="Confirmar", command=confirmar_filtros).grid(row=3, column=0, columnspan=2, pady=10)

        def exportar_reporte(tipo):
            """Exporta el reporte según el tipo de inspección."""
            def generar_reporte(planta, mes, ano):
                if tipo == "Reporte Completo":
                    # Llamar a la función correcta para obtener el reporte
                    resultado = exportar_reporte_mensual_extintores_gabinetes_api(planta, mes, ano)
                else:  # Aquí aseguramos que realmente se llame la función correcta
                    print("Error al exportar el reporte.")

                fecha = datetime.datetime.now().strftime("%Y-%m-%d")
                nombre_archivo = f"Reporte_Completo_{planta}_{fecha}.xlsx"

                if isinstance(resultado, BytesIO):
                    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")], title="Guardar archivo como", initialfile=nombre_archivo)
                    if ruta_archivo:
                        with open(ruta_archivo, "wb") as archivo:
                            archivo.write(resultado.getvalue())
                        messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a {ruta_archivo}")
                else:
                    messagebox.showerror("Error", f"No se pudo generar el reporte para {planta} en {mes}/{ano}")

            seleccionar_filtros(generar_reporte)

        ctk.CTkButton(top, text="Exportar Reporte Completo Mensual", command=lambda: exportar_reporte("Reporte Completo")).pack(pady=10)




#############################################################################################################
                                    #Vizualizar y descargar ordenes de servicio
#############################################################################################################

    def configurar_ordenes_servicio(self):
        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        planta_label = ctk.CTkLabel(filtros_frame, text="Seleccionar Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_dropdown_ordenes_serivcio = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],
            width=200
        )
        self.planta_dropdown_ordenes_serivcio.set("Todos")  # Valor inicial predeterminado
        self.planta_dropdown_ordenes_serivcio.pack(side="left", padx=5)
        self.planta_dropdown_ordenes_serivcio.bind("<<ComboboxSelected>>", self.filtrar_por_planta_hidrantes)

        # Campo de búsqueda
        self.search_ordenes_servicio = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar ordenes de servicio...", width=200)
        self.search_ordenes_servicio.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_ordenes_servicio)
        search_button.pack(side="left", padx=5)

    def filtrar_ordenes_servicio(self, event=None):
        """
        Maneja el evento de selección de planta en el dropdown para equipos de respiración.
        """
        if self.planta_dropdown_ordenes_serivcio:
            planta_seleccionada = self.planta_dropdown_ordenes_serivcio.get()
            if planta_seleccionada:
                print(f"[DEBUG] Planta seleccionada: {planta_seleccionada}")
                self.cargar_ordenes_servicio(planta=planta_seleccionada)
            else:
                print("[DEBUG] No se seleccionó una planta válida. Usando 'Todos'.")
                self.cargar_ordenes_servicio(planta="Todos")
        else:
            print("[DEBUG] El dropdown no está definido.")
            self.cargar_ordenes_servicio(planta="Todos")
      
    def cargar_ordenes_servicio(self, planta=None, search=None, page=1):
        """
        Carga los datos de equipos de respiración en la tabla.
        """
        try:
            # Determinar la planta a usar
            planta_filtrada = self.planta_dropdown_ordenes_serivcio.get() if self.planta_dropdown_ordenes_serivcio.get() else self.empresa

            # Llamar a la API
            ordenes_servicio = obtener_listado_ordenes_servicio(planta_filtrada, search=search, page=page)

            if not ordenes_servicio:
                messagebox.showwarning("Advertencia", "No se encontraron datos.")
                return

            # Limpiar la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Agregar los datos a la tabla
            for equipo in ordenes_servicio:
                self.tree.insert("", "end", values=(
                    equipo.get("id", ""),
                    equipo.get("cliente", ""),
                    equipo.get("fecha_envio", ""),
                    equipo.get("firma_confirmacion", "")
                ))
            # Actualizar página actual
            self.current_page = page
            print(f"[DEBUG] Datos cargados para planta: {planta_filtrada}, página: {page}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def mostrar_seccion_ordenes_servicio(self, titulo):
        self.title(titulo)  # Cambia el título dinámicamente
        self.extintores_frame.pack(fill="both", expand=True)
        for widget in self.extintores_frame.winfo_children():
            widget.destroy()  # Limpia el contenido actual del frame

        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        # Campo de búsqueda
        search_label = ctk.CTkLabel(filtros_frame, text="Buscar:", font=("Arial", 12))
        search_label.pack(side="left", padx=5)

        self.search_ordenes_servicio = ctk.CTkEntry(filtros_frame, placeholder_text="Número", width=180)
        self.search_ordenes_servicio.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_ordenes_servicio, width=40)
        search_button.pack(side="left", padx=5)

        # Botón de refrescar tabla
        refresh_button = ctk.CTkButton(filtros_frame, text="Refrescar", command=self.cargar_ordenes_servicio, width=80)
        refresh_button.pack(side="left", padx=5)

        # Dropdown para filtro por planta si es admin
        planta_label = ctk.CTkLabel(filtros_frame, text="Filtrar por Planta:", font=("Arial", 12))
        planta_label.pack(side="left", padx=5)

        self.planta_dropdown_ordenes_serivcio = ttk.Combobox(filtros_frame, values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
        self.planta_dropdown_ordenes_serivcio.bind("<<ComboboxSelected>>", self.filtrar_ordenes_servicio)
        self.planta_dropdown_ordenes_serivcio.pack(side="left", padx=5)

        # Botón para exportar tabla completa
        aprobar_orden_servicio = ctk.CTkButton(filtros_frame, text="Aprobar", command=self.aprobar_orden, width=80, fg_color="#4CAF50")
        aprobar_orden_servicio.pack(side="left", padx=5)
        
        # Botón para exportar tabla completa
        exportar_button = ctk.CTkButton(filtros_frame, text="Exportar", command=self.descargar_orden_servicio, width=80, fg_color="#4CAF50")
        exportar_button.pack(side="left", padx=5)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30, background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E", borderwidth=1)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4B8BBE", foreground="white")
        style.map("Treeview", background=[("selected", "#4B8BBE")])

        columnas = (
            "Orden servicio", "Planta", "Fecha de envio", "Recibí equipo"
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
        retroceder_button = ctk.CTkButton(paginacion_frame, text="<< Retroceder", command=self.pagina_anterior_ordenes_servicio, width=100)
        retroceder_button.pack(side="left", padx=5)

        # Botón para siguiente página
        siguiente_button = ctk.CTkButton(paginacion_frame, text="Siguiente >>", command=self.pagina_siguiente_ordenes_servicio, width=100)
        siguiente_button.pack(side="left", padx=5)

        # Cargar datos en la tabla
        self.cargar_ordenes_servicio()

    def buscar_ordenes_servicio(self):
        """
        Función para buscar equipos de respiración según un término de búsqueda.
        """
        search_term = self.search_ordenes_servicio.get()  # Obtener el término de búsqueda desde la entrada
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda.")
            return

        print(f"Término de búsqueda: {search_term}")

        # Determinar la planta
        planta_filtrada = self.planta_dropdown_ordenes_serivcio.get() if hasattr(self, "planta_dropdown_ordenes_serivcio") else "Todos"

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_ordenes_servicio(planta=planta_filtrada, search=search_term, page=self.current_page)

    def descargar_orden_servicio(self):
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
                datetime.datetime.strptime(fecha_texto, "%Y-%m-%d")
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

    def pagina_anterior_ordenes_servicio(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.cargar_ordenes_servicio(page=self.current_page)

    def pagina_siguiente_ordenes_servicio(self):
        self.current_page += 1
        self.cargar_ordenes_servicio(page=self.current_page)

    def aprobar_orden(id_orden):
        selected_item = id_orden.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una orden de servicio.")
            return

        dato = id_orden.tree.item(selected_item, "values")

        try:
            id_seleccionado = dato[0]
        except IndexError as e:
            messagebox.showerror("Error", f"Error al obtener id de la orden de servicio: {e}")
            return

        confirmacion = messagebox.askyesno("Confirmar Aprobación", f"¿Estás seguro de aprobar la orden ID {id_seleccionado}?")

        if not confirmacion:
            messagebox.showinfo("Cancelado", "Aprobación cancelada.")
            return

        payload = {
            "id": id_seleccionado,
            "firma_confirmacion": "Aprobado"
        }

        resultado = aprobar_orden_servicio(payload)

        if resultado.get("success"):
            messagebox.showinfo("Éxito", f"Orden ID {id_seleccionado} aprobada exitosamente.")
            if hasattr(id_orden, 'cargar_ordenes_servicio') and callable(getattr(id_orden, 'cargar_ordenes_servicio')):
                id_orden.cargar_ordenes_servicio()
        else:
            messagebox.showerror("Error", f"Error al aprobar: {resultado.get('error', 'Error desconocido')}")




    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar sesión?")
        if respuesta:
            self.destroy()

if __name__ == "__main__":
    user_data = {"NombreUsuario": "Gerardo Daniel Lopez Lara"}  # Sustituir por datos reales del usuario
    privilegio = "admin"  # Cambiar según el privilegio del usuario
    app = GuiInicial(user_data, privilegio, "Time or Time")
    app.mainloop()

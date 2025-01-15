import customtkinter as ctk
from tkinter import ttk, messagebox, Toplevel
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
        self.search_input_resp = None
        self.search_input = None  # Campo de búsqueda
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

        bomberos_button = ctk.CTkButton(nav_frame, text="Gabinete de Equipo de Bomberos", command=lambda: self.mostrar_seccion("Gabinete de Equipo de Bomberos"), width=180, fg_color="#4B8BBE", height=35)
        bomberos_button.pack(pady=10)

        mangueras_button = ctk.CTkButton(nav_frame, text="Gabinete de Mangueras e Hidrantes", command=lambda: self.mostrar_seccion("Gabinete de Mangueras e Hidrantes"), width=180, fg_color="#4B8BBE", height=35)
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
        if self.privilegio == "admin":
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

    def configurar_filtros(self):
        """
        Configura los filtros para la tabla, incluyendo el dropdown de planta si el usuario es admin.
        """
        filtros_frame = ctk.CTkFrame(self.extintores_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(5, 10))

        if self.privilegio == "admin":
            planta_label = ctk.CTkLabel(filtros_frame, text="Seleccionar Planta:", font=("Arial", 12))
            planta_label.pack(side="left", padx=5)

            # Dropdown con opciones de plantas
            self.planta_dropdown = ctk.CTkComboBox(
                filtros_frame,
                values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"],
                width=200
            )
            self.planta_dropdown.pack(side="left", padx=5)

            # Vincular el evento de selección al método filtrar_por_planta
            self.planta_dropdown.bind("<<ComboboxSelected>>", self.filtrar_por_planta)

        # Campo de búsqueda y botón de buscar
        self.search_input = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar extintores...", width=200)
        self.search_input.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_extintor)
        search_button.pack(side="left", padx=5)

    def filtrar_por_planta(self, event=None):
        planta_seleccionada = self.planta_filtro.get()
        
        # Verificación de que el valor no sea vacío
        if planta_seleccionada:
            print(f"Filtrando por planta: {planta_seleccionada}")
            self.cargar_datos_extintores(planta=planta_seleccionada)
        else:
            print("No se seleccionó una planta válida.")
            # Opcional: puedes cargar todos los datos si no se selecciona una planta válida.
            self.cargar_datos_extintores()

    def cargar_datos_extintores(self, planta=None, search=None, page=1):
        """
        Carga los datos de extintores en la tabla, considerando privilegios, búsqueda y filtros.

        Args:
            planta (str): La planta seleccionada (solo para admin).
            search (str): El término de búsqueda.
            page (int): Número de página para la API.
        """
        try:
            # Determinar la planta a usar según el privilegio
            if self.privilegio == "admin":
                if search:  # Si hay búsqueda, no cambiar la planta del dropdown
                    planta_filtrada = self.planta_dropdown.get() if not search else self.planta_filtrada_anterior
                    print(f"Planta seleccionada por el admin (búsqueda activa): {planta_filtrada}")  # Depuración
                else:
                    planta_filtrada = planta if planta else self.planta_dropdown.get()
                    print(f"Planta seleccionada por el admin (sin búsqueda): {planta_filtrada}")  # Depuración
            else:
                # Usuarios no admin siempre usan su planta
                planta_filtrada = self.empresa

            # Llamar a la API para obtener los datos
            datos_extintores = obtener_extintores_api(planta_filtrada, search=search, page=page)

            if not datos_extintores:
                messagebox.showwarning("Advertencia", "No se encontraron datos de extintores.")
                return

            # Limpia la tabla antes de cargar nuevos datos
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Agrega los datos a la tabla
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
            print(f"Datos cargados para la planta: {planta_filtrada}, Búsqueda: {search}, Página: {page}")
            
            # Guardar la planta actual para futuras búsquedas
            self.planta_filtrada_anterior = planta_filtrada

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
        top = Toplevel(self)
        top.title("Modificar Extintor")
        top.geometry("400x500")

        scrollable_frame = ctk.CTkScrollableFrame(top, width=380, height=350)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        fields = ["referencia", "fecha_fabricacion", "planta", "area", "numerodeextintor", "ubicacion_extintor", "tipo", "capacidad_kg", "fecha_recarga", "fecha_vencimiento", "fecha_ultima_prueba"]
        entries = {}

        for i, field in enumerate(fields):
            label = ctk.CTkLabel(scrollable_frame, text=field.capitalize(), font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(scrollable_frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entry.insert(0, extintor_data[i])
            entries[field] = entry

        def guardar_cambios():
            nuevos_datos = {field: entry.get() for field, entry in entries.items()}
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
        top.geometry("450x540")

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
            entry = ctk.CTkEntry(top, width=250)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entradas[campo] = entry

        # Campo de planta
        label_planta = ctk.CTkLabel(top, text="Planta", font=("Arial", 12))
        label_planta.grid(row=len(campos), column=0, padx=10, pady=5, sticky="w")

        if self.privilegio == "admin":  # Si es administrador, permitir seleccionar la planta
            planta_entry = ctk.CTkComboBox(top, values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], width=250)
            planta_entry.grid(row=len(campos), column=1, padx=10, pady=5)
        else:  # Si no es administrador, prellenar la planta con la empresa
            planta_entry = ctk.CTkEntry(top, width=250)
            planta_entry.grid(row=len(campos), column=1, padx=10, pady=5)
            planta_entry.insert(0, self.empresa)
            planta_entry.configure(state="disabled")  # No editable

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
            respuesta = agregar_extintor_api(datos)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", respuesta.get("message", "El extintor fue agregado exitosamente."))
                top.destroy()  # Cerrar ventana emergente
                self.cargar_datos_extintores()  # Refrescar la tabla

        # Botón para guardar los datos
        guardar_button = ctk.CTkButton(top, text="Guardar", command=guardar_datos)
        guardar_button.grid(row=len(campos) + 1, column=0, columnspan=2, pady=20)

    def buscar_extintor(self):
        """
        Función para buscar extintores según un término de búsqueda.
        """
        search_term = self.search_input.get()  # Obtener el término de búsqueda desde la entrada
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda.")
            return

        print(f"Término de búsqueda: {search_term}")  # Depuración

        # Determinar la planta según el privilegio
        if self.privilegio == "admin" and hasattr(self, "planta_dropdown"):
            planta_filtrada = self.planta_dropdown.get()
        else:
            planta_filtrada = self.empresa

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_extintores(planta=planta_filtrada, search=search_term, page=self.current_page)

    # Lógica para paginación (siguiente y retroceder)
    def pagina_anterior(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.cargar_datos_extintores(page=self.current_page)

    def pagina_siguiente(self):
        self.current_page += 1
        self.cargar_datos_extintores(page=self.current_page)

    def exportar_reporte_extintores(self):
        """
        Abre una ventana emergente con opciones para exportar la tabla de datos o un reporte completo de extintores inspeccionados.
        """
        top = ctk.CTkToplevel(self)
        top.title("Exportar Reporte de Extintores")
        top.geometry("400x200")

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
                            initialfile=f"reporte_extintores_{planta_seleccionada}.xlsx"
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

        if self.privilegio == "admin":
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
        if self.privilegio == "admin" and self.planta_dropdown_resp:
            planta_seleccionada = self.planta_dropdown_resp.get()
            if planta_seleccionada:
                print(f"[DEBUG] Planta seleccionada: {planta_seleccionada}")
                self.cargar_datos_resp(planta=planta_seleccionada)
            else:
                print("[DEBUG] No se seleccionó una planta válida. Usando 'Todos'.")
                self.cargar_datos_resp(planta="Todos")
        else:
            print("[DEBUG] El dropdown no está definido o el usuario no es admin.")
            self.cargar_datos_resp(planta="Todos")
            
    def cargar_datos_resp(self, planta=None, search=None, page=1):
        """
        Carga los datos de equipos de respiración en la tabla.
        """
        try:
            # Determinar la planta a usar
            if self.privilegio == "admin":
                planta_filtrada = planta or (self.planta_dropdown_resp.get() if self.planta_dropdown_resp else "Todos")
            else:
                planta_filtrada = self.empresa

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

        self.search_input = ctk.CTkEntry(filtros_frame, placeholder_text="Número de extintor, referencia, ubicación", width=180)
        self.search_input.pack(side="left", padx=5)

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
        if self.privilegio == "admin":
            planta_label = ctk.CTkLabel(filtros_frame, text="Filtrar por Planta:", font=("Arial", 12))
            planta_label.pack(side="left", padx=5)

            self.planta_dropdown_resp = ttk.Combobox(filtros_frame, values=["Todos", "Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], state="readonly")
            self.planta_dropdown_resp.bind("<<ComboboxSelected>>", self.filtrar_por_planta_resp)
            self.planta_dropdown_resp.pack(side="left", padx=5)

        # Botón para exportar tabla completa
        exportar_button = ctk.CTkButton(filtros_frame, text="Exportar", command=self.exportar_tabla_completa_resp, width=80, fg_color="#4CAF50")
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

        # Determinar la planta según el privilegio
        if self.privilegio == "admin" and hasattr(self, "planta_dropdown_resp"):
            planta_filtrada = self.planta_dropdown_resp.get()
        else:
            planta_filtrada = self.empresa

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

        # Campos de entrada
        campos = ["referencia", "numero", "area", "ubicacion", "fecha_ph"]
        entradas = {}

        # Crear formulario dinámico
        for idx, campo in enumerate(campos):
            label = ctk.CTkLabel(top, text=campo.replace("_", " ").capitalize(), font=("Arial", 12))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(top, width=250)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entradas[campo] = entry

        # Campo de planta
        label_planta = ctk.CTkLabel(top, text="Planta", font=("Arial", 12))
        label_planta.grid(row=len(campos), column=0, padx=10, pady=5, sticky="w")

        if self.privilegio == "admin":  # Si es administrador, permitir seleccionar la planta
            planta_entry = ctk.CTkComboBox(top, values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], width=250)
            planta_entry.grid(row=len(campos), column=1, padx=10, pady=5)
        else:  # Si no es administrador, prellenar la planta con la empresa
            planta_entry = ctk.CTkEntry(top, width=250)
            planta_entry.grid(row=len(campos), column=1, padx=10, pady=5)
            planta_entry.insert(0, self.empresa)
            planta_entry.configure(state="disabled")  # No editable

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
        
        # Verificar el índice correcto de las columnas
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
            
            # Rellenar el formulario con los valores actuales
            if field == "fecha_ph" and value:
                try:
                    # Convertir el valor de fecha_ph al formato adecuado (si es necesario)
                    parsed_date = datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z").strftime("%m %Y")
                    entry.insert(0, parsed_date)
                except ValueError:
                    entry.insert(0, value)  # Si no es una fecha válida, usar el valor original
            else:
                entry.insert(0, value)

            entries[field] = entry

        # Campo de planta (solo editable si el usuario es admin)
        if self.privilegio == "admin":
            planta_entry = ctk.CTkComboBox(scrollable_frame, values=["Aspre Consultores", "Frisa Santa Catarina", "Frisa Aerospace"], width=250)
            planta_entry.grid(row=len(fields), column=1, padx=10, pady=5)
            planta_entry.set(planta)  # Valor inicial para planta
        else:
            planta_entry = ctk.CTkEntry(scrollable_frame, width=250)
            planta_entry.grid(row=len(fields), column=1, padx=10, pady=5)
            planta_entry.insert(0, self.empresa)
            planta_entry.configure(state="disabled")  # No editable para usuarios no admin

        entries["planta"] = planta_entry

        def guardar_cambios():
            """
            Envía los datos modificados al servidor para actualizar el equipo de respiración.
            """
            nuevos_datos = {field: entry.get() for field, entry in entries.items()}

            # Validar que todos los campos están completos
            for campo, valor in nuevos_datos.items():
                if not valor:
                    messagebox.showerror("Error", f"El campo '{campo}' es obligatorio.")
                    return

            # Llamar a la API para actualizar los datos
            respuesta = editar_gabinetes_api(referencia, nuevos_datos)

            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", "Equipo de respiración actualizado correctamente.")
                top.destroy()
                self.cargar_datos_resp()  # Refrescar la tabla con los datos actualizados

        guardar_button = ctk.CTkButton(top, text="Guardar Cambios", command=guardar_cambios)
        guardar_button.pack(pady=10)



    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar sesión?")
        if respuesta:
            self.destroy()

if __name__ == "__main__":
    user_data = {"NombreUsuario": "Gerardo Daniel Lopez Lara"}  # Sustituir por datos reales del usuario
    privilegio = "admin"  # Cambiar según el privilegio del usuario
    app = GuiInicial(user_data, privilegio, "Time or Time")
    app.mainloop()

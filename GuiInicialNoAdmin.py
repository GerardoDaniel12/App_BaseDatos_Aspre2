import customtkinter as ctk
from tkinter import ttk, messagebox, Toplevel
from DB.ConexionExtintores import *
from datetime import datetime
from io import BytesIO


# Configuración para el tema del sistema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class GuiInicialNoAdmin(ctk.CTk):
    def __init__(self, user_data, privilegio, empresa):
        super().__init__()
        self.user_data = user_data
        self.privilegio = privilegio
        self.empresa = empresa  # Almacena el nombre de la empresa
        self.title("Extintores Generales")  # Título principal
        self.after(1, lambda: self.state('zoomed'))


        self.tree = None
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

        # Botón para modificar extintor
        modificar_button = ctk.CTkButton(filtros_frame, text="Modificar", command=self.modificar_extintor, width=80, fg_color="#FFA500")
        modificar_button.pack(side="left", padx=5)

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

    def buscar_extintor(self):
        """
        Función para buscar extintores según un término de búsqueda.
        """
        search_term = self.search_input.get()  # Obtener el término de búsqueda desde la entrada
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda.")
            return

        print(f"Término de búsqueda: {search_term}")  # Depuración

        planta_filtrada = self.empresa  # Aquí se obtiene correctamente la planta de la empresa

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_extintores(planta=planta_filtrada, search=search_term, page=self.current_page)

    def cargar_datos_extintores(self, planta=None, search=None, page=1):
        try:
            # Guardar la planta filtrada actual para mantener el filtro al navegar entre páginas
            self.planta_filtrada_anterior = self.empresa

            # Llamar a la API para obtener los datos (incluyendo búsqueda y paginación)
            datos_extintores = obtener_extintores_api(self.empresa, search=search, page=page)

            if not datos_extintores:
                messagebox.showwarning("Advertencia", "No se encontraron datos de extintores.")
                return

            # Limpia la tabla antes de cargar nuevos datos
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
            print(f"Datos cargados: Planta={self.empresa}, Búsqueda={search}, Página={page}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def exportar_tabla_completa(self):
        """
        Exporta la tabla completa o filtrada según la planta seleccionada o el privilegio del usuario.
        """
        try:
            # Si el usuario es admin, usa el valor del dropdown; si no, usa la empresa predeterminada
            planta_seleccionada = self.empresa

            # Llama a la función de exportación, pasando el filtro de planta
            resultado = exportar_extintores_api(planta_seleccionada, self.privilegio, planta_seleccionada)

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

        scrollable_frame = ctk.CTkScrollableFrame(top, width=380, height=400)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Campos permitidos para editar
        campos_editables = ["area", "numerodeextintor", "ubicacion_extintor"]

        # Campos y widgets
        fields = {
            "referencia": {"editable": False},
            "fecha_fabricacion": {"editable": False},
            "planta": {"editable": False},
            "area": {"editable": True},
            "numerodeextintor": {"editable": True},
            "ubicacion_extintor": {"editable": True},
            "tipo": {"editable": False},
            "capacidad_kg": {"editable": False},
            "fecha_recarga": {"editable": False},
            "fecha_vencimiento": {"editable": False},
            "fecha_ultima_prueba": {"editable": False},
        }

        entries = {}

        for i, (field, config) in enumerate(fields.items()):
            label = ctk.CTkLabel(scrollable_frame, text=field.capitalize(), font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if config["editable"]:  # Si el campo es editable
                entry = ctk.CTkEntry(scrollable_frame)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                entry.insert(0, extintor_data[i])
                entries[field] = entry
            else:  # Si no es editable, solo mostrar el valor actual
                label_value = ctk.CTkLabel(scrollable_frame, text=extintor_data[i], font=("Arial", 12))
                label_value.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        def guardar_cambios():
            nuevos_datos = {}
            for field, widget in entries.items():
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

     # Lógica para paginación (siguiente y retroceder)
    
    def pagina_anterior(self):
        try:
            # Verificar que no se intente ir más atrás de la primera página
            if self.current_page > 1:
                # Decrementar el número de la página
                self.current_page -= 1

                # Usar la empresa vinculada a la cuenta para filtrar los registros
                planta_filtrada = self.empresa

                print(f"Planta filtrada (anterior): {planta_filtrada}, Página: {self.current_page}")

                # Llamar a cargar_datos_extintores con la empresa vinculada y la página anterior
                self.cargar_datos_extintores(planta=planta_filtrada, page=self.current_page)
            else:
                messagebox.showinfo("Información", "Ya estás en la primera página.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cambiar de página: {e}")

    def pagina_siguiente(self):
        try:
            # Usar la empresa vinculada a la cuenta para filtrar los registros
            planta_filtrada = self.empresa

            # Verificar si la planta filtrada es válida
            if not planta_filtrada:
                planta_filtrada = "Aspre Consultores"  # Valor predeterminado en caso de error

            print(f"Planta filtrada (siguiente): {planta_filtrada}")

            # Llamar a cargar_datos_extintores con la empresa vinculada y la siguiente página
            self.cargar_datos_extintores(planta=planta_filtrada, page=self.current_page + 1)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cambiar de página: {e}")

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
            planta_seleccionada = self.empresa

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
                      
    def cargar_datos_resp(self, planta=None, search=None, page=1):
        """
        Carga los datos de equipos de respiración en la tabla.
        """
        try:
            # Determinar la planta a usar
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

        self.search_input_resp = ctk.CTkEntry(filtros_frame, placeholder_text="Número, referencia, ubicación", width=180)
        self.search_input_resp.pack(side="left", padx=5)

        search_button = ctk.CTkButton(filtros_frame, text="Buscar", command=self.buscar_equipo_respiracion, width=40)
        search_button.pack(side="left", padx=5)

        # Botón de refrescar tabla
        refresh_button = ctk.CTkButton(filtros_frame, text="Refrescar", command=self.cargar_datos_resp, width=80)
        refresh_button.pack(side="left", padx=5)

        # Botón para modificar extintor
        modificar_button = ctk.CTkButton(filtros_frame, text="Modificar", command=self.modificar_equipo_respiracion, width=80, fg_color="#FFA500")
        modificar_button.pack(side="left", padx=5)

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
        planta_filtrada = self.empresa

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_resp(planta=planta_filtrada, search=search_term, page=self.current_page)

    def exportar_tabla_completa_resp(self):
        """
        Exporta la tabla completa o filtrada según la planta seleccionada o el privilegio del usuario.
        """
        try:
            #usa la empresa predeterminada
            planta_seleccionada = self.empresa

            # Llama a la función de exportación, pasando el filtro de planta
            resultado = exportar_gabinetes_api(self.empresa, planta_seleccionada)

            # Mostrar mensajes según el resultado
            if "Archivo Excel guardado exitosamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado durante la exportación: {e}")

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

        # Campos a editar (solo numero, area, ubicacion son modificables)
        fields = ["referencia", "numero", "area", "ubicacion", "fecha_ph"]
        values = [referencia, numero, area, ubicacion, fecha_ph]
        entries = {}

        for i, (field, value) in enumerate(zip(fields, values)):
            label = ctk.CTkLabel(scrollable_frame, text=field.capitalize(), font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            if field in ["numero", "area", "ubicacion"]:
                entry = ctk.CTkEntry(scrollable_frame)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                entries[field] = entry
            else:
                value_label = ctk.CTkLabel(scrollable_frame, text=value, font=("Arial", 12))
                value_label.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # Campo de planta (solo visualización)
        planta_label = ctk.CTkLabel(scrollable_frame, text="Planta", font=("Arial", 12))
        planta_label.grid(row=len(fields), column=0, padx=10, pady=5, sticky="w")
        planta_value = ctk.CTkLabel(scrollable_frame, text=planta, font=("Arial", 12))
        planta_value.grid(row=len(fields), column=1, padx=10, pady=5, sticky="w")

        def guardar_cambios():
            nuevos_datos = {field: entry.get() for field, entry in entries.items()}

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
            planta_seleccionada = self.empresa

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
                            initialfile=f"Reporte_Gabinetes_Equipo_Respiracion_{planta_seleccionada}.xlsx"
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

    def cargar_datos_bomberos(self, planta=None, search=None, page=1):
        """
        Carga los datos de equipos de respiración en la tabla.
        """
        try:
            # Determinar la planta a usar
            planta_filtrada = self.empresa

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

        # Botón para modificar extintor
        modificar_button = ctk.CTkButton(filtros_frame, text="Modificar", command=self.modificar_equipo_bomberos, width=80, fg_color="#FFA500")
        modificar_button.pack(side="left", padx=5)

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
        planta_filtrada = self.empresa

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_bomberos(planta=planta_filtrada, search=search_term, page=self.current_page)

    def exportar_tabla_completa_bomberos(self):
        """
        Exporta la tabla completa o filtrada según la planta seleccionada o el privilegio del usuario.
        """
        try:
            # Si el usuario es admin, usa el valor del dropdown; si no, usa la empresa predeterminada
            planta_seleccionada = self.empresa

            # Llama a la función de exportación, pasando el filtro de planta
            resultado = exportar_gabinetes_bomberos_api(self.empresa, planta_seleccionada)

            # Mostrar mensajes según el resultado
            if "Archivo Excel guardado exitosamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado durante la exportación: {e}")

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

        # Mostrar referencia como texto
        referencia_label = ctk.CTkLabel(scrollable_frame, text="Referencia:", font=("Arial", 12))
        referencia_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        referencia_value = ctk.CTkLabel(scrollable_frame, text=referencia, font=("Arial", 12, "bold"))
        referencia_value.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Campos editables
        editable_fields = ["numero", "area", "ubicacion"]
        editable_values = [numero, area, ubicacion]
        entries = {}

        for i, (field, value) in enumerate(zip(editable_fields, editable_values), start=1):
            label = ctk.CTkLabel(scrollable_frame, text=field.capitalize(), font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(scrollable_frame, width=250)
            entry.insert(0, value)  # Prellenar con el valor actual
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry

        # Mostrar planta como texto
        planta_label = ctk.CTkLabel(scrollable_frame, text="Planta:", font=("Arial", 12))
        planta_label.grid(row=len(editable_fields) + 1, column=0, padx=10, pady=5, sticky="w")
        planta_value = ctk.CTkLabel(scrollable_frame, text=planta, font=("Arial", 12, "bold"))
        planta_value.grid(row=len(editable_fields) + 1, column=1, padx=10, pady=5, sticky="w")

        def guardar_cambios():
            """
            Envía los nuevos datos del equipo a la API para actualizar.
            """
            nuevos_datos = {field: entry.get() for field, entry in entries.items()}
            nuevos_datos["referencia"] = referencia  # Incluir referencia en los datos
            nuevos_datos["planta"] = planta  # Incluir planta en los datos

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
            planta_seleccionada = self.empresa

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

    def cargar_datos_hidrantes(self, planta=None, search=None, page=1):
        """
        Carga los datos de equipos de respiración en la tabla.
        """
        try:
            # Determinar la planta a usar
            planta_filtrada = self.empresa

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

        # Botón para modificar extintor
        modificar_button = ctk.CTkButton(filtros_frame, text="Modificar", command=self.modificar_equipo_hidrantes, width=80, fg_color="#FFA500")
        modificar_button.pack(side="left", padx=5)

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
        planta_filtrada = self.empresa

        # Reiniciar a la primera página y cargar los datos filtrados
        self.current_page = 1
        self.cargar_datos_hidrantes(planta=planta_filtrada, search=search_term, page=self.current_page)

    def exportar_tabla_completa_hidrantes(self):
        """
        Exporta la tabla completa o filtrada según la planta seleccionada o el privilegio del usuario.
        """
        try:
            # Si el usuario es admin, usa el valor del dropdown; si no, usa la empresa predeterminada
            planta_seleccionada = self.empresa
            # Llama a la función de exportación, pasando el filtro de planta
            resultado = exportar_gabinetes_hidrantes_mangueras_api(self.empresa, planta_seleccionada)

            # Mostrar mensajes según el resultado
            if "Archivo Excel guardado exitosamente" in resultado:
                messagebox.showinfo("Éxito", resultado)
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado durante la exportación: {e}")

    def modificar_equipo_hidrantes(self):
        """
        Abre una ventana emergente para modificar los datos de un equipo de hidrantes seleccionado en la tabla,
        permitiendo modificar solo los campos 'numero', 'area' y 'ubicacion'.
        """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un equipo de hidrantes para modificar.")
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
        top.title("Modificar Equipo de Hidrantes")
        top.geometry("450x500")

        scrollable_frame = ctk.CTkScrollableFrame(top, width=400, height=350)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Mostrar referencia como texto no editable
        label_referencia = ctk.CTkLabel(scrollable_frame, text="Referencia:", font=("Arial", 12))
        label_referencia.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        referencia_label = ctk.CTkLabel(scrollable_frame, text=referencia, font=("Arial", 12, "bold"))
        referencia_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Mostrar planta como texto no editable
        label_planta = ctk.CTkLabel(scrollable_frame, text="Planta:", font=("Arial", 12))
        label_planta.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        planta_label = ctk.CTkLabel(scrollable_frame, text=planta, font=("Arial", 12, "bold"))
        planta_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Mostrar fecha_ph_manguera como texto no editable
        label_fecha_ph = ctk.CTkLabel(scrollable_frame, text="Fecha PH Manguera:", font=("Arial", 12))
        label_fecha_ph.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        fecha_label = ctk.CTkLabel(scrollable_frame, text=fecha_ph_manguera, font=("Arial", 12, "bold"))
        fecha_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Campos editables: numero, area, ubicacion
        campos_editables = ["numero", "area", "ubicacion"]
        valores_editables = [numero, area, ubicacion]
        entradas = {}

        for idx, (campo, valor) in enumerate(zip(campos_editables, valores_editables), start=3):
            label = ctk.CTkLabel(scrollable_frame, text=campo.capitalize(), font=("Arial", 12))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            entry = ctk.CTkEntry(scrollable_frame, width=250)
            entry.insert(0, valor)  # Prellenar el campo con el valor actual
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entradas[campo] = entry

        def guardar_cambios():
            """
            Envía los nuevos datos del equipo a la API para actualizar.
            """
            nuevos_datos = {
                "referencia": referencia,
                "planta": planta,
                "fecha_ph_manguera": fecha_ph_manguera,
                "numero": entradas["numero"].get(),
                "area": entradas["area"].get(),
                "ubicacion": entradas["ubicacion"].get(),
            }

            # Validación de datos antes de enviar
            for campo in ["numero", "area", "ubicacion"]:
                if not nuevos_datos[campo].strip():
                    messagebox.showerror("Error", f"El campo '{campo}' no puede estar vacío.")
                    return

            # Llamar a la API para actualizar los datos
            respuesta = editar_gabinetes_hidrantes_mangueras_api(referencia, nuevos_datos)
            if "error" in respuesta:
                messagebox.showerror("Error", respuesta["error"])
            else:
                messagebox.showinfo("Éxito", "Equipo de hidrantes actualizado correctamente.")
                top.destroy()
                self.cargar_datos_hidrantes()  # Refrescar la tabla con los datos actualizados

        # Botón para guardar los cambios
        guardar_button = ctk.CTkButton(top, text="Guardar Cambios", command=guardar_cambios)
        guardar_button.pack(pady=10)

    def exportar_reporte_gabinete_hidrantes(self):
        """
        Abre una ventana emergente con opciones para exportar la tabla de datos o un reporte completo de extintores inspeccionados.
        """
        top = ctk.CTkToplevel(self)
        top.title("Exportar Reporte de Mangueras")
        top.geometry("400x200")

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
            planta_seleccionada = self.empresa

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
    app = GuiInicialNoAdmin(user_data, privilegio, "Time or Time")
    app.mainloop()

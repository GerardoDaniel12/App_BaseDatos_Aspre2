import customtkinter as ctk
from tkinter import ttk, messagebox
from DB.ConexionExtintores import crear_conexion, obtener_extintores

def crear_gui_inicial(login_window):
    gui_inicial = GuiInicial(login_window)
    gui_inicial.mainloop()

class GuiInicial(ctk.CTk):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.title("Aspre Consultores")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = ctk.CTkLabel(self, text="Bienvenido a Aspre Consultores", font=("Arial", 24))
        title_label.pack(pady=20)

        # Frame para los botones de navegación
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(side="left", fill="y")

        # Botón para ver extintores inspeccionados
        extintores_button = ctk.CTkButton(self.nav_frame, text="Extintores Inspeccionados", command=self.mostrar_extintores)
        extintores_button.pack(pady=10)

        # Botón para crear tabla en SQL
        crear_tabla_button = ctk.CTkButton(self.nav_frame, text="Crear Tabla SQL", command=self.crear_tabla_sql)
        crear_tabla_button.pack(pady=10)

        # Botón de Cerrar Sesión
        logout_button = ctk.CTkButton(self.nav_frame, text="Cerrar Sesión", command=self.cerrar_sesion)
        logout_button.pack(pady=10)

        # Botón de Información Personal
        info_button = ctk.CTkButton(self.nav_frame, text="Información Personal", command=self.mostrar_informacion_personal)
        info_button.pack(pady=10)

        # Frame para la tabla de extintores
        self.extintores_frame = ctk.CTkFrame(self)
        self.extintores_frame.pack(fill="both", expand=True)
        self.extintores_frame.pack_forget()  # Ocultar inicialmente

    def mostrar_extintores(self):
        self.extintores_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(self.extintores_frame, columns=("Doc", "Fecha realizado", "Planta", "Área", "Número De Extintor",
            "Ubicación de extintor", "TIPO", "Capacidad en KG", "Fecha de fabricacion", "Fecha Recarga", 
            "Fecha Vencimiento", "Fecha ultima de prueba hidrostatica", "Presion", "Manometro", 
            "Seguro", "Etiquetas", "Señalamientos", "Circulo y Numero", "Pintura", "Manguera", 
            "Boquilla", "Golpes o daños", "Obstruido", "Comentarios"), show='headings')

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(self.extintores_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        try:
            # Conectar a la base de datos
            conn = crear_conexion()
            if conn:
                # Obtener los extintores de la base de datos
                extintores = obtener_extintores(conn)

                # Limpiar la tabla
                for item in tree.get_children():
                    tree.delete(item)

                # Insertar datos en la tabla
                for extintor in extintores:
                    tree.insert("", "end", values=extintor)

                conn.close()  # Cerrar la conexión a la base de datos

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la información: {str(e)}")

    def crear_tabla_sql(self):
        # Crear una ventana para solicitar el nombre de la tabla
        def crear_tabla():
            nombre_tabla = nombre_entry.get()
            if nombre_tabla:
                try:
                    # Conectar a la base de datos
                    conn = crear_conexion()
                    cursor = conn.cursor()

                    # Crear la tabla
                    cursor.execute(f"""
                        CREATE TABLE {nombre_tabla} (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            doc VARCHAR(255),
                            fecha_realizado DATE,
                            planta VARCHAR(255),
                            area VARCHAR(255),
                            numero_extintor VARCHAR(255),
                            ubicacion_extintor VARCHAR(255),
                            tipo VARCHAR(255),
                            capacidad_kg DECIMAL(10, 2),
                            fecha_fabricacion DATE,
                            fecha_recarga DATE,
                            fecha_vencimiento DATE,
                            fecha_ultima_prueba DATE,
                            presion VARCHAR(50),
                            manometro VARCHAR(50),
                            seguro VARCHAR(50),
                            etiquetas VARCHAR(50),
                            senalamientos VARCHAR(50),
                            circulo_numero VARCHAR(50),
                            pintura VARCHAR(50),
                            manguera VARCHAR(50),
                            boquilla VARCHAR(50),
                            golpes_danos VARCHAR(50),
                            obstruido VARCHAR(50),
                            comentarios TEXT
                        )
                    """)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo("Éxito", f"Tabla '{nombre_tabla}' creada exitosamente.")

                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo crear la tabla: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "Por favor ingresa un nombre para la tabla.")

            # Cerrar la ventana
            tabla_window.destroy()

        # Ventana para ingresar el nombre de la tabla
        tabla_window = ctk.CTkToplevel(self)
        tabla_window.title("Crear Tabla SQL")
        tabla_window.geometry("300x150")

        ctk.CTkLabel(tabla_window, text="Nombre de la Tabla:").pack(pady=10)
        nombre_entry = ctk.CTkEntry(tabla_window)
        nombre_entry.pack(pady=5)

        crear_button = ctk.CTkButton(tabla_window, text="Crear Tabla", command=crear_tabla)
        crear_button.pack(pady=10)

    def mostrar_informacion_personal(self):
        messagebox.showinfo("Información Personal", "Esta es tu información personal.")

    def cerrar_sesion(self):
        # Opcional: Cancela animaciones o temporizadores aquí, si corresponde
        self.extintores_frame.pack_forget()  # Ocultar el frame antes de cerrar la ventana
        self.destroy()  # Cierra la ventana de GuiInicial
        self.login_window.deiconify()  # Muestra nuevamente la ventana de login

if __name__ == "__main__":
    app = GuiInicial()
    app.mainloop()

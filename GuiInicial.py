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
        self.title("Aspre Consultores - Panel Principal")
        self.geometry("1000x700")
        self.resizable(False, False)

        # Crear la estructura de widgets
        self.create_widgets()

    def create_widgets(self):
        # Contenedor principal
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Bienvenido a Aspre Consultores", font=("Arial", 24, "bold"))
        title_label.pack(pady=(10, 20))

        # Frame de navegación lateral
        nav_frame = ctk.CTkFrame(main_frame, width=200, corner_radius=10)
        nav_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)

        # Botones de navegación
        ctk.CTkLabel(nav_frame, text="Navegación", font=("Arial", 14, "bold")).pack(pady=(20, 10))
        
        extintores_button = ctk.CTkButton(nav_frame, text="Extintores Inspeccionados", command=self.mostrar_extintores, width=180)
        extintores_button.pack(pady=10)
        
        crear_tabla_button = ctk.CTkButton(nav_frame, text="Crear Tabla SQL", command=self.crear_tabla_sql, width=180)
        crear_tabla_button.pack(pady=10)
        
        info_button = ctk.CTkButton(nav_frame, text="Información Personal", command=self.mostrar_informacion_personal, width=180)
        info_button.pack(pady=10)
        
        logout_button = ctk.CTkButton(nav_frame, text="Cerrar Sesión", command=self.cerrar_sesion, fg_color="#d9534f", hover_color="#c9302c", width=180)
        logout_button.pack(pady=20)

        # Frame para mostrar la tabla de extintores
        self.extintores_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        self.extintores_frame.pack(fill="both", expand=True, padx=(0, 20), pady=10)
        self.extintores_frame.pack_forget()  # Ocultar inicialmente

    def mostrar_extintores(self):
        self.extintores_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(self.extintores_frame, columns=("id", "Referencia", "Fecha realizado", "Planta", "Area",
            "Numero de extintor", "Ubicacion de extintor", "Tipo", "Capacidad en kg", "Fecha de fabricacion", 
            "Fecha de recarga", "Fecha de vencimiento", "Fecha ultima de prueba hidrostratica", "Presion", 
            "Manometro", "Seguro", "Etiquetas", "Señalamiento", "Circulo y numero", "Pintura", 
            "Manguera", "Boquilla", "Golpes o daños", "Obstruido","Comentarios"), show='headings')

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(self.extintores_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        try:
            conn = crear_conexion()
            if conn:
                extintores = obtener_extintores(conn)

                for item in tree.get_children():
                    tree.delete(item)

                for extintor in extintores:
                    tree.insert("", "end", values=extintor)

                conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la información: {str(e)}")

    def crear_tabla_sql(self):
        def crear_tabla():
            nombre_tabla = nombre_entry.get()
            if nombre_tabla:
                try:
                    conn = crear_conexion()
                    cursor = conn.cursor()

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

            tabla_window.destroy()

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
        self.extintores_frame.pack_forget()
        self.destroy()
        self.login_window.deiconify()

if __name__ == "__main__":
    app = GuiInicial(None)  # Aquí puedes pasar la ventana de login si corresponde
    app.mainloop()

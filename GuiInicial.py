import customtkinter as ctk
from tkinter import ttk, messagebox
from DB.ConexionExtintores import obtener_referencia

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
            ref = obtener_referencia()
            docs = list(ref.stream())

            for item in tree.get_children():
                tree.delete(item)

            for doc in docs:
                data = doc.to_dict()
                tree.insert("", "end", values=(
                    doc.id, data.get("Fecha realizado", "N/A"), data.get("Planta", "N/A"),
                    data.get("Area", "N/A"), data.get("NumeroDeExtintor", "N/A"), 
                    data.get("Ubicacion de extintor", "N/A"), data.get("TIPO", "N/A"), 
                    data.get("Capacidad en KG", "N/A"), data.get("Fecha de fabricacion", "N/A"), 
                    data.get("Fecha Recarga", "N/A"), data.get("Fecha Vencimiento", "N/A"),
                    data.get("Fecha ultima de prueba hidrostatica", "N/A"), data.get("Presion", "N/A"), 
                    data.get("Manometro", "N/A"), data.get("Seguro", "N/A"), data.get("Etiquetas", "N/A"), 
                    data.get("Señalamientos", "N/A"), data.get("Circulo y Numero", "N/A"), 
                    data.get("Pintura", "N/A"), data.get("Manguera", "N/A"), data.get("Boquilla", "N/A"),
                    data.get("Golpes o daños", "N/A"), data.get("Obstruido", "N/A"), data.get("Comentarios", "N/A")
                ))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la información: {str(e)}")

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

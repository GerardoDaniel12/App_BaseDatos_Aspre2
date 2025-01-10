import requests
import openpyxl
from openpyxl.styles import Alignment, Font
from tkinter import filedialog


def obtener_extintores_api(empresa, search=None, page=1):
    url = "https://timeortimee.onrender.com/api/extintores/generales/aspreconsultores/obtener/extintores/Desktop"
    try:
        params = {
            "search": search,
            "page": page,
            "planta": empresa
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Respuesta de la API: {data}")  # Depuración
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos de la API: {e}")
        return []


def editar_extintores_api(referencia, datos):
    """
    Edita un extintor en la base de datos mediante la API.
    
    Args:
        referencia (str): Referencia del extintor a modificar.
        datos (dict): Diccionario con los campos y valores a actualizar.
    
    Returns:
        dict: Respuesta de la API.
    """
    url = "https://timeortimee.onrender.com/api/extintores/generales/aspreconsultores/editar/extintor"
    payload = {"referencia": referencia, **datos}  # Añadir referencia a los datos

    try:
        # Realizar la solicitud PUT
        response = requests.put(url, json=payload)
        response.raise_for_status()  # Lanzar error si el código de estado no es 200
        return response.json()  # Devolver la respuesta como JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": "No se pudo conectar con la API"}
    
def exportar_extintores_api(empresa, privilegio, planta):
    """
    Descarga el archivo Excel generado por la API y lo guarda localmente, aplicando el filtro de planta.
    
    Args:
        empresa (str): Nombre de la empresa.
        privilegio (str): Privilegio del usuario.
        planta (str): Planta seleccionada para el filtro.
    
    Returns:
        str: Mensaje de éxito o error.
    """
    # Construir la URL con el parámetro de planta
    planta_param = planta if planta != "Todos" else ""
    url = f"https://timeortimee.onrender.com/api/extintores/generales/exportar/excel/desktop?planta={planta_param}"

    try:
        # Solicitar el archivo Excel al endpoint
        response = requests.get(url)
        response.raise_for_status()

        # Guardar el archivo localmente con un diálogo
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            title="Guardar archivo como",
            initialfile="extintores_generales.xlsx"
        )

        if not ruta_archivo:
            return "Operación cancelada por el usuario."

        # Escribir el contenido del archivo
        with open(ruta_archivo, "wb") as archivo:
            archivo.write(response.content)

        return f"Archivo Excel guardado exitosamente en: {ruta_archivo}"
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con la API: {e}"
    except Exception as e:
        return f"Error al guardar el archivo: {e}"

def eliminar_extintor_api(referencia):
    """
    Elimina un extintor de la base de datos mediante la API.

    Args:
        referencia (str): Referencia del extintor a eliminar.

    Returns:
        dict: Respuesta de la API.
    """
    url = "https://timeortimee.onrender.com/api/extintores/aspreconsultores/generales/eliminar"
    try:
        # Realizar la solicitud DELETE
        response = requests.delete(url, json={"referencia": referencia})
        response.raise_for_status()  # Lanza un error si el código de estado no es 200
        return response.json()  # Retorna la respuesta en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": "No se pudo conectar con la API"}

def agregar_extintor_api(datos):
    """
    Conecta al endpoint para agregar un nuevo extintor.

    Args:
        datos (dict): Diccionario con los campos requeridos para agregar un extintor.

    Returns:
        dict: Respuesta de la API en formato JSON.
    """
    url = "https://timeortimee.onrender.com/api/extintores/aspreconsultores/generales/agregar"
    try:
        # Realizar la solicitud POST
        response = requests.post(url, json=datos)
        response.raise_for_status()  # Lanza un error si el código de estado no es 200
        return response.json()  # Retorna la respuesta en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": f"Error al conectar con la API: {str(e)}"}

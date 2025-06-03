import requests
import openpyxl
from openpyxl.styles import Alignment, Font
from tkinter import filedialog
from io import BytesIO
from config import *
from datetime import datetime


###############################################         Extintores         ##############################################
###############################################         Extintores         ##############################################
###############################################         Extintores         ##############################################

def obtener_extintores_api(empresa, search=None, page=1):
    try:
        params = {
            "search": search,
            "page": page,
            "planta": empresa
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(api_url_obtener_extintores, params=params)
        response.raise_for_status()
        data = response.json()
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
    payload = {"referencia": referencia, **datos}  # Añadir referencia a los datos

    try:
        # Realizar la solicitud PUT
        response = requests.put(API_URL_editar_extintores_api, json=payload)
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
    url = f"{API_URL_exportar_extintores_api}{planta_param}"

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
    try:
        # Realizar la solicitud DELETE
        response = requests.delete(API_URL_eliminar_extintor_api, json={"referencia": referencia})
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
    try:
        # Realizar la solicitud POST
        response = requests.post(API_URL_agregar_extintor_api, json=datos)
        response.raise_for_status()  # Lanza un error si el código de estado no es 200
        return response.json()  # Retorna la respuesta en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": f"Error al conectar con la API: {str(e)}"}

def exportar_reporte_extintores_api(planta, mes=None, ano=None):
    """
    Conecta al endpoint para exportar el reporte completo de extintores inspeccionados.

    Args:
        planta (str): Nombre de la planta.
        mes (int, opcional): Mes para filtrar.
        ano (int, opcional): Año para filtrar.

    Returns:
        BytesIO: Archivo Excel en memoria si la solicitud es exitosa.
        str: Mensaje de error en caso de falla.
    """
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(API_URL_exportar_reporte_extintores_api, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)

def obtener_extintores_gabinetes_inspeccionados_en_linea_api(empresa, dia=None, mes=None, ano=None, page=1, search=None, ultima_actualizacion=False):
    """Obtiene datos de inspecciones de extintores desde la API.
    Si 'ultima_actualizacion' es True, devuelve solo el último registro.
    """
    if not empresa:
        print("Error: Se debe especificar una empresa/planta.")
        return []

    fecha_actual = datetime.now()
    mes = mes or fecha_actual.month
    ano = ano or fecha_actual.year

    # Si 'dia' es proporcionado, convertirlo a entero y validar
    if dia:
        try:
            dia = int(dia)
        except ValueError:
            print("Error: El parámetro 'día' debe ser un número válido.")
            return []
    
    params = {
        "mes": mes,
        "ano": ano,
        "planta": empresa,
        "page": page,
        "search": search,
        "ultima_actualizacion": ultima_actualizacion
    }
    
    # Solo añadir 'dia' si está definido
    if dia:
        params["dia"] = dia
    
    print(f"Parámetros enviados a la API: {params}")  # Depuración

    try:
        response = requests.get(
            API_URL_obtener_extintores_gabinetes_inspeccionados_en_linea_api,
            params=params,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        inspecciones = data.get("inspecciones", [])

        # Si se solicita la última actualización, devolver solo el más reciente
        if ultima_actualizacion and inspecciones:
            return sorted(inspecciones, key=lambda x: x["fecha_inspeccionado"], reverse=True)[0]

        return inspecciones

    except requests.exceptions.Timeout:
        print("Error: La solicitud a la API ha tardado demasiado en responder.")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API. Verifica la conexión de red.")
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP al obtener los datos: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error inesperado en la solicitud: {e}")
    except ValueError:
        print("Error: La respuesta de la API no es un JSON válido.")
    
    return []  # Devuelve lista vacía en caso de error

def obtener_extintores_inspeccionados_excel(planta, mes=None, ano=None):
    """
    Conecta al endpoint para exportar el reporte completo de extintores inspeccionados.

    Args:
        planta (str): Nombre de la planta.
        mes (int, opcional): Mes para filtrar.
        ano (int, opcional): Año para filtrar.

    Returns:
        BytesIO: Archivo Excel en memoria si la solicitud es exitosa.
        str: Mensaje de error en caso de falla.
    """
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(API_URL_ubtener_extintores_inspeccionados_para_descargar, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)

def obtener_extintores_no_inspeccionados_excel(planta, mes=None, ano=None):
    """
    Descarga el reporte de extintores no inspeccionados desde la API.

    Args:
        planta (str): Nombre de la planta.
        mes (int, opcional): Mes para filtrar.
        ano (int, opcional): Año para filtrar.

    Returns:
        BytesIO: Archivo Excel en memoria si la solicitud es exitosa.
        str: Mensaje de error en caso de falla.
    """
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        print(f"Solicitando a API con: {params}")  # 🚀 Debug

        response = requests.get(API_URL_ubtener_extintores_no_inspeccionados_para_descargar, params=params)
        response.raise_for_status()

        # Validar que el contenido realmente sea un archivo Excel
        content_type = response.headers.get("Content-Type", "")
        if "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" not in content_type:
            print(f"Error: Respuesta de API no es un Excel. Content-Type recibido: {content_type}")
            return "La API no devolvió un archivo Excel válido."

        # Guardar el contenido como archivo en memoria
        excel_bytes = BytesIO(response.content)

        try:
            # Intentar abrirlo con openpyxl para verificar que no está corrupto
            wb = openpyxl.load_workbook(excel_bytes)
            wb.close()
            excel_bytes.seek(0)  # Volver al inicio del archivo
        except Exception as e:
            print(f"Error al abrir el archivo descargado: {e}")
            return "El archivo descargado está corrupto."

        return excel_bytes  # ✅ Devuelve el archivo válido en memoria

    except requests.exceptions.RequestException as e:
        print(f"No hay inspecciones pendientes")
        return str(e)


###############################################         Gabinetes respiracion         ##############################################
###############################################         Gabinetes respiracion         ##############################################
###############################################         Gabinetes respiracion         ##############################################



def obtener_gabinetes_api(empresa, search=None, page=1):
    try:
        params = {
            "planta": empresa,
            "search": search,
            "page": page
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(API_URL_obtener_gabinetes_api, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Respuesta de la API: {data}")  # Depuración
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return []

def editar_gabinetes_api(referencia, datos):
    """
    Edita un equipo de respiración en la base de datos mediante la API.
    
    Args:
        referencia (str): Referencia del equipo a modificar.
        datos (dict): Diccionario con los campos y valores a actualizar.
    
    Returns:
        dict: Respuesta de la API.
    """
    
    # Asegurarnos de que la referencia está incluida en los datos
    payload = {"referencia": referencia, **datos}

    try:
        # Realizar la solicitud PUT a la API
        response = requests.put(API_URL_editar_gabinetes_api, json=payload)
        
        # Verificar si la respuesta fue exitosa (código HTTP 200)
        response.raise_for_status()
        
        # Devolver la respuesta como un JSON
        return response.json()
    except requests.exceptions.RequestException as e:
        # Imprimir error en la consola para diagnóstico
        print(f"Error al conectar con la API: {e}")
        
        # Devolver un diccionario con un mensaje de error
        return {"error": "No se pudo conectar con la API"}
    except Exception as e:
        # Manejo de otros errores que puedan surgir
        print(f"Error inesperado: {e}")
        return {"error": "Error inesperado al procesar la solicitud"}
    
def exportar_gabinetes_api(empresa, planta):
    """
    Exporta los gabinetes en un archivo Excel generado por la API.

    Args:
        empresa (str): Nombre de la empresa.
        planta (str): Planta seleccionada para el filtro.

    Returns:
        str: Mensaje de éxito o error.
    """
    planta_param = planta if planta != "Todos" else ""
    url = f"{API_URL_exportar_gabinetes_api}{planta_param}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            title="Guardar archivo como",
            initialfile="gabinetes_equipo_respiracion.xlsx"
        )

        if not ruta_archivo:
            return "Operación cancelada por el usuario."

        with open(ruta_archivo, "wb") as archivo:
            archivo.write(response.content)

        return f"Archivo Excel guardado exitosamente en: {ruta_archivo}"
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con la API: {e}"
    except Exception as e:
        return f"Error al guardar el archivo: {e}"

def eliminar_gabinete_api(referencia):
    """
    Elimina un gabinete de la base de datos mediante la API.

    Args:
        referencia (str): Referencia del gabinete a eliminar.

    Returns:
        dict: Respuesta de la API.
    """
    try:
        response = requests.delete(API_URL_eliminar_gabinete_api, json={"referencia": referencia})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": "No se pudo conectar con la API"}

def agregar_gabinete_api(datos):
    """
    Conecta al endpoint para agregar un nuevo gabinete.

    Args:
        datos (dict): Diccionario con los campos requeridos para agregar un gabinete.

    Returns:
        dict: Respuesta de la API en formato JSON.
    """
    try:
        # Realizar la solicitud POST
        response = requests.post(API_URL_agregar_gabinete_api, json=datos)
        response.raise_for_status()  # Lanza un error si el código de estado no es 200
        return response.json()  # Retorna la respuesta en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": f"Error al conectar con la API: {str(e)}"}

def exportar_reporte_gabinetes_equipo_respiracion_api(planta, mes=None, ano=None):
    """
    Conecta al endpoint para exportar el reporte completo de extintores inspeccionados.

    Args:
        planta (str): Nombre de la planta.
        mes (int, opcional): Mes para filtrar.
        ano (int, opcional): Año para filtrar.

    Returns:
        BytesIO: Archivo Excel en memoria si la solicitud es exitosa.
        str: Mensaje de error en caso de falla.
    """
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(API_URL_exportar_reporte_gabinetes_equipo_respiracion_api, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)


###############################################         Gabinetes Bomberos         ##############################################
###############################################         Gabinetes Bomberos         ##############################################
###############################################         Gabinetes Bomberos         ##############################################


def obtener_gabinetes_equipo_bomberos_psc_api(empresa, search=None, page=1):
    try:
        params = {
            "planta": empresa,
            "search": search,
            "page": page
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(API_URL_obtener_gabinetes_equipo_bomberos_psc_api, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Respuesta de la API: {data}")  # Depuración
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return []

def editar_gabinetes_equipo_bomberos_psc_api(referencia, datos):
    """
    Edita un equipo de respiración en la base de datos mediante la API.
    
    Args:
        referencia (str): Referencia del equipo a modificar.
        datos (dict): Diccionario con los campos y valores a actualizar.
    
    Returns:
        dict: Respuesta de la API.
    """
    
    # Asegurarnos de que la referencia está incluida en los datos
    payload = {"referencia": referencia, **datos}

    try:
        # Realizar la solicitud PUT a la API
        response = requests.put(API_URL_editar_gabinetes_equipo_bomberos_psc_api, json=payload)
        
        # Verificar si la respuesta fue exitosa (código HTTP 200)
        response.raise_for_status()
        
        # Devolver la respuesta como un JSON
        return response.json()
    except requests.exceptions.RequestException as e:
        # Imprimir error en la consola para diagnóstico
        print(f"Error al conectar con la API: {e}")
        
        # Devolver un diccionario con un mensaje de error
        return {"error": "No se pudo conectar con la API"}
    except Exception as e:
        # Manejo de otros errores que puedan surgir
        print(f"Error inesperado: {e}")
        return {"error": "Error inesperado al procesar la solicitud"}

def agregar_gabinete_bomberos_api(datos):
    """
    Conecta al endpoint para agregar un nuevo gabinete de bomberos.

    Args:
        datos (dict): Diccionario con los campos requeridos para agregar un gabinete.

    Returns:
        dict: Respuesta de la API en formato JSON.
    """
    try:
        response = requests.post(API_URL_agregar_gabinete_bomberos_api, json=datos)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": f"Error al conectar con la API: {str(e)}"}

def eliminar_gabinete_bomberos_api(referencia):
    """
    Elimina un gabinete de la base de datos mediante la API.

    Args:
        referencia (str): Referencia del gabinete a eliminar.

    Returns:
        dict: Respuesta de la API.
    """
    try:
        # Enviar la referencia como parámetro en la URL
        params = {"referencia": referencia}
        print(f"Enviando datos al servidor como parámetros: {params}")  # Depuración
        response = requests.delete(API_URL_eliminar_gabinete_bomberos_api, params=params)  # Cambiar a 'params' en lugar de 'json'
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Capturar y mostrar detalles del error
        print(f"Error al conectar con la API: {e}")
        return {"error": f"Error al conectar con la API: {str(e)}"}

def exportar_gabinetes_bomberos_api(empresa, planta):
    """
    Exporta los gabinetes en un archivo Excel generado por la API.

    Args:
        empresa (str): Nombre de la empresa.
        planta (str): Planta seleccionada para el filtro.

    Returns:
        str: Mensaje de éxito o error.
    """
    planta_param = planta if planta != "Todos" else ""
    url = f"{API_URL_exportar_gabinetes_bomberos_api}{planta_param}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            title="Guardar archivo como",
            initialfile="gabinetes_equipo_bomberos.xlsx"
        )

        if not ruta_archivo:
            return "Operación cancelada por el usuario."

        with open(ruta_archivo, "wb") as archivo:
            archivo.write(response.content)

        return f"Archivo Excel guardado exitosamente en: {ruta_archivo}"
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con la API: {e}"
    except Exception as e:
        return f"Error al guardar el archivo: {e}"

def exportar_reporte_gabinetes_bomberos_psc_api(planta, mes=None, ano=None):
    """
    Conecta al endpoint para exportar el reporte completo de extintores inspeccionados.

    Args:
        planta (str): Nombre de la planta.
        mes (int, opcional): Mes para filtrar.
        ano (int, opcional): Año para filtrar.

    Returns:
        BytesIO: Archivo Excel en memoria si la solicitud es exitosa.
        str: Mensaje de error en caso de falla.
    """
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(API_URL_exportar_reporte_gabinetes_bomberos_psc_api, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)


###############################################         Gabinetes Hidrantes         ##############################################
###############################################         Gabinetes Hidrantes         ##############################################
###############################################         Gabinetes Hidrantes         ##############################################


def obtener_gabinetes_hidrantes_mangueras_api(empresa, search=None, page=1):
    try:
        params = {
            "planta": empresa,
            "search": search,
            "page": page
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(API_URL_obtener_gabinetes_hidrantes_mangueras_api, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Respuesta de la API: {data}")  # Depuración
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return []
    
def editar_gabinetes_hidrantes_mangueras_api(referencia, datos):
    """
    Edita un equipo de respiración en la base de datos mediante la API.
    
    Args:
        referencia (str): Referencia del equipo a modificar.
        datos (dict): Diccionario con los campos y valores a actualizar.
    
    Returns:
        dict: Respuesta de la API.
    """
    
    # Asegurarnos de que la referencia está incluida en los datos
    payload = {"referencia": referencia, **datos}

    try:
        # Realizar la solicitud PUT a la API
        response = requests.put(API_URL_editar_gabinetes_hidrantes_mangueras_api, json=payload)
        
        # Verificar si la respuesta fue exitosa (código HTTP 200)
        response.raise_for_status()
        
        # Devolver la respuesta como un JSON
        return response.json()
    except requests.exceptions.RequestException as e:
        # Imprimir error en la consola para diagnóstico
        print(f"Error al conectar con la API: {e}")
        
        # Devolver un diccionario con un mensaje de error
        return {"error": "No se pudo conectar con la API"}
    except Exception as e:
        # Manejo de otros errores que puedan surgir
        print(f"Error inesperado: {e}")
        return {"error": "Error inesperado al procesar la solicitud"}

def agregar_gabinete_hidrantes_mangueras(datos):
    """
    Conecta al endpoint para agregar un nuevo gabinete de bomberos.

    Args:
        datos (dict): Diccionario con los campos requeridos para agregar un gabinete.

    Returns:
        dict: Respuesta de la API en formato JSON.
    """
    try:
        response = requests.post(API_URL_agregar_gabinete_hidrantes_mangueras, json=datos)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": f"Error al conectar con la API: {str(e)}"}

def eliminar_gabinete_hidrantes_mangueras_api(referencia):
    """
    Elimina un gabinete de la base de datos mediante la API.

    Args:
        referencia (str): Referencia del gabinete a eliminar.

    Returns:
        dict: Respuesta de la API.
    """
    try:
        # Enviar la referencia como parámetro en la URL
        params = {"referencia": referencia}
        print(f"Enviando datos al servidor como parámetros: {params}")  # Depuración
        response = requests.delete(API_URL_eliminar_gabinete_hidrantes_mangueras_api, params=params)  # Cambiar a 'params' en lugar de 'json'
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Capturar y mostrar detalles del error
        print(f"Error al conectar con la API: {e}")
        return {"error": f"Error al conectar con la API: {str(e)}"}

def exportar_gabinetes_hidrantes_mangueras_api(empresa, planta):
    """
    Exporta los gabinetes en un archivo Excel generado por la API.

    Args:
        empresa (str): Nombre de la empresa.
        planta (str): Planta seleccionada para el filtro.

    Returns:
        str: Mensaje de éxito o error.
    """
    planta_param = planta if planta != "Todos" else ""
    url = f"{API_URL_exportar_gabinetes_hidrantes_mangueras_api}{planta_param}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            title="Guardar archivo como",
            initialfile="gabinetes_mangueras_hidrantes.xlsx"
        )

        if not ruta_archivo:
            return "Operación cancelada por el usuario."

        with open(ruta_archivo, "wb") as archivo:
            archivo.write(response.content)

        return f"Archivo Excel guardado exitosamente en: {ruta_archivo}"
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con la API: {e}"
    except Exception as e:
        return f"Error al guardar el archivo: {e}"

def exportar_reporte_hidrantes_mangueras_psc_api(planta, mes=None, ano=None):
    """
    Conecta al endpoint para exportar el reporte completo de extintores inspeccionados.

    Args:
        planta (str): Nombre de la planta.
        mes (int, opcional): Mes para filtrar.
        ano (int, opcional): Año para filtrar.

    Returns:
        BytesIO: Archivo Excel en memoria si la solicitud es exitosa.
        str: Mensaje de error en caso de falla.
    """
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(API_URL_exportar_reporte_hidrantes_mangueras_psc_api, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)


###############################################         Exportar reporte mensual         ##############################################
###############################################         Exportar reporte mensual         ##############################################
###############################################         Exportar reporte mensual         ##############################################


def exportar_reporte_mensual_extintores_gabinetes_api(planta, mes=None, ano=None):
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(API_URL_obtener_reporte_mensual_gabinetes_extintores_api, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)

###############################################         Ordenes servicio         ##############################################
###############################################         Ordenes servicio         ##############################################
###############################################         Ordenes servicio         ##############################################

def obtener_listado_ordenes_servicio(planta, search, page):
    try:
        params = {
            "cliente": planta,
            "search": search,
            "page": page
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(API_URL_obtener_ordenes_servicio_listado_api, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Respuesta de la API: {data}")  # Depuración
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return []

def aprobar_orden_servicio(datos):
    try:
        response = requests.post(API_URL_aprobar_ordenes_servicio_listado_api, json=datos)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": f"Error al conectar con la API: {str(e)}"}

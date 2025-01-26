import requests
import openpyxl
from openpyxl.styles import Alignment, Font
from tkinter import filedialog
from io import BytesIO


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
    url = "https://timeortimee.onrender.com/api/extintores/aspreconsultores/generales/exportar/reporte/completo"
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(url, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)






def obtener_gabinetes_api(empresa, search=None, page=1):
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/respiracion/obtener/desktop"
    try:
        params = {
            "planta": empresa,
            "search": search,
            "page": page
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(url, params=params)
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
    url = "https://timeortimee.onrender.com/api/gabinetes/equipo/respiracion/aspreconsultores/editar/equipo"
    
    # Asegurarnos de que la referencia está incluida en los datos
    payload = {"referencia": referencia, **datos}

    try:
        # Realizar la solicitud PUT a la API
        response = requests.put(url, json=payload)
        
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
    url = f"https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/respiracion/exportar/desktop?planta={planta_param}"

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
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/respiracion/eliminar/desktop"
    try:
        response = requests.delete(url, json={"referencia": referencia})
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
    url = "https://timeortimee.onrender.com/api/gabinetes/equiporespiracion/aspreconsultores/agregar"
    try:
        # Realizar la solicitud POST
        response = requests.post(url, json=datos)
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
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/respiracion/exportar/reporte/completo"
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(url, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)




def obtener_gabinetes_equipo_bomberos_psc_api(empresa, search=None, page=1):
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/obtener/desktop"
    try:
        params = {
            "planta": empresa,
            "search": search,
            "page": page
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(url, params=params)
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
    url = "https://timeortimee.onrender.com/api/gabinetes/bomberos/psc/aspreconsultores/editar/gabinete"
    
    # Asegurarnos de que la referencia está incluida en los datos
    payload = {"referencia": referencia, **datos}

    try:
        # Realizar la solicitud PUT a la API
        response = requests.put(url, json=payload)
        
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
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/psc/agregar/desktop"
    try:
        response = requests.post(url, json=datos)
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
    url = f"https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/psc/eliminar/desktop"
    try:
        # Enviar la referencia como parámetro en la URL
        params = {"referencia": referencia}
        print(f"Enviando datos al servidor como parámetros: {params}")  # Depuración
        response = requests.delete(url, params=params)  # Cambiar a 'params' en lugar de 'json'
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
    url = f"https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/exportar/desktop?planta={planta_param}"

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
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/psc/exportar/reporte/completo"
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(url, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)





def obtener_gabinetes_hidrantes_mangueras_api(empresa, search=None, page=1):
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/obtener/desktop"
    try:
        params = {
            "planta": empresa,
            "search": search,
            "page": page
        }
        print(f"Parámetros enviados a la API: {params}")  # Depuración
        response = requests.get(url, params=params)
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
    url = "https://timeortimee.onrender.com/api/gabinetes/mangueras/hidrantes/aspreconsultores/editar/gabinete"
    
    # Asegurarnos de que la referencia está incluida en los datos
    payload = {"referencia": referencia, **datos}

    try:
        # Realizar la solicitud PUT a la API
        response = requests.put(url, json=payload)
        
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
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/agregar/desktop"
    try:
        response = requests.post(url, json=datos)
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
    url = f"https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/eliminar/desktop"
    try:
        # Enviar la referencia como parámetro en la URL
        params = {"referencia": referencia}
        print(f"Enviando datos al servidor como parámetros: {params}")  # Depuración
        response = requests.delete(url, params=params)  # Cambiar a 'params' en lugar de 'json'
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
    url = f"https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/exportar/desktop?planta={planta_param}"

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
    url = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/exportar/reporte/completo"
    try:
        params = {"planta": planta}
        if mes:
            params["mes"] = mes
        if ano:
            params["ano"] = ano

        response = requests.get(url, params=params)
        response.raise_for_status()

        # Retornar el contenido del archivo como BytesIO
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return str(e)


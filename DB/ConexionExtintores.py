import requests

def obtener_extintores_api():
    """Obtiene los extintores desde la API."""
    url = "https://timeortimee.onrender.com/api/extintores/generales/aspreconsultores/obtener/extintores"  # Ajusta esta URL según tu servidor
    try:
        response = requests.get(url, params={"search": None, "page": 1})  # Puedes agregar más parámetros aquí si es necesario
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        data = response.json()  # Parsear la respuesta como JSON
        return data["data"]  # Devuelve solo los datos de los extintores
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos de la API: {e}")
        return []

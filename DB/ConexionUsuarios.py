import requests

def login(username, password):
    url = "https://timeortimee.onrender.com/api/data/flutter/login"  # Cambia por la URL de tu API
    headers = {"Content-Type": "application/json"}
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()  # Parsear la respuesta como JSON
        
        if response.status_code == 200:
            # Asume que la API devuelve los datos del usuario si la autenticación es exitosa
            return True, response_data
        else:
            # Devuelve el error o mensaje desde la API
            return False, response_data.get("error", "Error desconocido")
    except requests.RequestException as e:
        # Manejar errores de conexión
        print(f"Error al conectar con la API: {e}")
        return False, "Error de conexión"

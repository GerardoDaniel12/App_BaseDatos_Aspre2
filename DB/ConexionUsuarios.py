# ConexionUsuarios.py
import mysql.connector
from mysql.connector import Error

# Configuración de la conexión a MySQL
db_config = {
    'host': 'localhost',         
    'user': 'root',        
    'password': '1234567Frt', 
    'database': 'extintoresinspeccionados'  
}

# Función para conectar a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(**db_config)
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos MySQL")
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para iniciar sesión
def login(email, password):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, correo, privilegio, empresa FROM usuarios WHERE correo=%s AND contraseña=%s", (email, password))
    user = cursor.fetchone()
    conexion.close()

    if user:
        return True, user  # Retorna el usuario con el privilegio
    else:
        return False, "Usuario o contraseña incorrectos"

# Función para registrar un nuevo usuario
def signup(email, password, privilegio='noadmin', empresa=None):
    try:
        conexion = conectar()
        if conexion is None:
            return False, "No se pudo conectar a la base de datos"

        cursor = conexion.cursor()
        consulta = "INSERT INTO usuarios (correo, contraseña, privilegio, empresa) VALUES (%s, %s, %s, %s)"
        cursor.execute(consulta, (email, password, privilegio, empresa))
        conexion.commit()

        conexion.close()
        return True, "Usuario registrado exitosamente"

    except Error as e:
        return False, f"Error al intentar registrar el usuario: {e}"

# ConexionUsuarios.py
import mysql.connector
from mysql.connector import Error
from customtkinter import CTkImage
from PIL import Image
import io

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
    cursor.execute("SELECT id, correo, privilegio, empresa, imagen FROM usuarios WHERE correo=%s AND contraseña=%s", (email, password))
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
    

# Función para guardar la imagen en la base de datos
def guardar_imagen(imagen_path, user_id):
    try:
        # Abrir la imagen en modo binario
        with open(imagen_path, 'rb') as file:
            imagen_binaria = file.read()

        # Conectar a la base de datos
        conexion = conectar()
        if conexion is None:
            return False, "No se pudo conectar a la base de datos"

        cursor = conexion.cursor()
        consulta = "UPDATE usuarios SET imagen = %s WHERE id = %s"
        cursor.execute(consulta, (imagen_binaria, user_id))
        conexion.commit()

        conexion.close()
        return True, "Imagen guardada correctamente"
    except Error as e:
        return False, f"Error al intentar guardar la imagen: {e}"

# Función para obtener la imagen de la base de datos
from customtkinter import CTkImage
from PIL import Image
import io

def obtener_imagen(user_id):
    try:
        conexion = conectar()  # Asumiendo que esta función establece la conexión con la base de datos
        if conexion is None:
            return False, None  # Devolvemos None si la conexión falla

        cursor = conexion.cursor()
        consulta = "SELECT imagen FROM usuarios WHERE id = %s"
        cursor.execute(consulta, (user_id,))
        imagen_binaria = cursor.fetchone()

        if imagen_binaria and imagen_binaria[0]:  # Si la imagen está en la base de datos
            imagen = Image.open(io.BytesIO(imagen_binaria[0]))  # Usamos Image.open para abrir los datos binarios
            imagen = imagen.resize((100, 100))  # Cambiar el tamaño de la imagen si es necesario
            imagen_ctk = CTkImage(dark_image=imagen, light_image=imagen)  # Usamos CTkImage
            return True, imagen_ctk
        else:
            return False, None  # Si no hay imagen, devolvemos None

    except Exception as e:
        print(f"Error al obtener imagen: {e}")
        return False, None  # En caso de error, devolvemos None
    
def actualizar_usuario(user_id, email=None, password=None, empresa=None, imagen_path=None):
    try:
        conexion = conectar()
        if conexion is None:
            return False, "No se pudo conectar a la base de datos"
        
        cursor = conexion.cursor()
        
        # Construimos la consulta de actualización
        consulta = "UPDATE usuarios SET "
        valores = []
        
        if email is not None:
            consulta += "correo = %s, "
            valores.append(email)
        
        if password is not None:
            consulta += "contraseña = %s, "
            valores.append(password)
        
        if empresa is not None:
            consulta += "empresa = %s, "
            valores.append(empresa)
        
        if imagen_path is not None:
            with open(imagen_path, 'rb') as file:
                imagen_binaria = file.read()
            consulta += "imagen = %s, "
            valores.append(imagen_binaria)
        
        consulta = consulta.rstrip(', ') + " WHERE id = %s"
        valores.append(user_id)
        
        cursor.execute(consulta, tuple(valores))
        conexion.commit()
        conexion.close()
        return True, "Información actualizada exitosamente"
    
    except Error as e:
        return False, f"Error al actualizar la información: {e}"
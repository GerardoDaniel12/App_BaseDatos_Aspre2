import mysql.connector
from mysql.connector import Error

def crear_conexion():
    """Crea una conexión a la base de datos MySQL."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234567Frt',
            database='extintoresinspeccionados'  # Cambia esto al nombre de tu base de datos
        )
        if conn.is_connected():
            print("Conexión exitosa a MySQL")
            return conn
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

def obtener_extintores(conn):
    """Obtiene los extintores desde la base de datos."""
    extintores = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM formulario_inspeccion")  # Cambia esto al nombre de tu tabla
        rows = cursor.fetchall()
        
        for row in rows:
            extintores.append(row)
        
        cursor.close()
    except Error as e:
        print(f"Error al obtener los extintores: {e}")

    return extintores

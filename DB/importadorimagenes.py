import mysql.connector

# Conexión a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234567Frt",
    database="extintoresinspeccionados"
)

def guardar_imagen(ruta_imagen, id_extintor):
    with open(ruta_imagen, "rb") as file:
        imagen_binaria = file.read()

    cursor = conn.cursor()
    consulta = "UPDATE usuarios SET imagen = %s WHERE id = %s"
    cursor.execute(consulta, (imagen_binaria, id_extintor))
    conn.commit()

# Llamada a la función para guardar la imagen
guardar_imagen("img/frisa.png", 1)  # Cambia 'nombre_imagen.jpg' por el nombre de tu archivo
conn.close()

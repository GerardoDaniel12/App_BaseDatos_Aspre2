# DB/ConexionExtintores.py

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Cargar las credenciales desde la carpeta DB
cred = credentials.Certificate("DB/extintoresinspeccionados-firebase-adminsdk-qgq23-ef2db6ee41.json")
firebase_admin.initialize_app(cred)

# Crear un cliente de Firestore
db = firestore.client()

# Función para obtener la referencia a la colección "Extintores"
def obtener_referencia():
    ExtitnroesAñoActual = f""
    return db.collection("25-10-2024")  # Cambia "Extintores" al nombre de tu colección

from flask import Flask, request, jsonify
import pyrebase
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración de Firebase usando variables de entorno
firebaseConfig = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

# Inicializar Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return jsonify({"message": "Usuario registrado exitosamente", "user": user}), 201
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return jsonify({"message": "Inicio de sesión exitoso", "user": user}), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)

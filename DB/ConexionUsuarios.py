# ConexionUsuarios.py
import pyrebase

# Configuración de Firebase
firebaseConfig = {
    "apiKey": "AIzaSyChAKnvmT8TVMIvOBUB1n14HU0sf-bBnu4",
    "authDomain": "extintoresaspreconsultores.firebaseapp.com",
    "databaseURL": "https://extintoresaspreconsultores-default-rtdb.firebaseio.com",
    "projectId": "extintoresaspreconsultores",
    "storageBucket": "extintoresaspreconsultores.appspot.com",
    "messagingSenderId": "265222328549",
    "appId": "1:265222328549:web:5ac7c70a0e91272b7d040c",
    "measurementId": "G-ZPW8Y4HSZC"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return True, user  # Devuelve True y el objeto de usuario
    except Exception as e:
        return False, str(e)  # Devuelve False y el error como cadena

def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return True, user  # Devuelve True y el objeto de usuario
    except Exception as e:
        return False, str(e)  # Devuelve False y el error como cadena

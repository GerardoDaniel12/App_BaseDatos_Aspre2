# ConexionUsuarios.py
import pyrebase

# Configuración de Firebase
firebaseConfig = {
  "apiKey": "AIzaSyCje6AsUznBpCbiTApEOFJAmSvpuyHrrPk",
  "authDomain": "extintoresinspeccionados.firebaseapp.com",
  "databaseURL": "https://extintoresinspeccionados-default-rtdb.firebaseio.com",
  "projectId": "extintoresinspeccionados",
  "storageBucket": "extintoresinspeccionados.appspot.com",
  "messagingSenderId": "798108528905",
  "appId": "1:798108528905:web:f7ec1d66bdb5cfc431e3d8",
  "measurementId": "G-SMZZY6GDLJ"
};

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

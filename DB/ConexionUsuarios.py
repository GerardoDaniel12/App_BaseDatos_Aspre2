import pyrebase

# Configuración de Firebase (reemplaza los valores con los de tu proyecto)
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

# Inicializar la aplicación de Firebase usando Pyrebase4
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login():
    print("Iniciar sesión")
    email = input("Introduce tu correo: ")
    password = input("Introduce tu contraseña: ")
    
    try:
        # Intenta iniciar sesión con el email y contraseña proporcionados
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Inicio de sesión exitoso para {email}")
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
    return

def signup():
    print("Registro de usuario")
    email = input("Introduce tu correo: ")
    password = input("Introduce tu contraseña: ")
    
    try:
        # Intenta registrar al usuario con el email y contraseña proporcionados
        user = auth.create_user_with_email_and_password(email, password)
        print(f"Usuario registrado con éxito: {email}")
    except Exception as e:
        print(f"Error durante el registro: {e}")
    return

# Pregunta si el usuario es nuevo o ya tiene cuenta
ans = input("¿Eres un nuevo usuario? (y/n): ").lower()

if ans == "n":
    login()
elif ans == "y":
    signup()
else:
    print("Opción no válida, por favor elige 'y' para nuevo usuario o 'n' para iniciar sesión.")

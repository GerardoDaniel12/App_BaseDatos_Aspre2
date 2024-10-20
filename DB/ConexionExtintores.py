import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Cargo de certificado
firebase_sdk = credentials.Certificate("extintoresaspreconsultores-firebase-adminsdk-b7nd9-0d717de68e.json")

#Referencia a la base de datos en tiempo real
firebase_admin.initialize_app(firebase_sdk,{"databaseURL":"https://extintoresaspreconsultores-default-rtdb.firebaseio.com/"})

#Creo una coleccion
ref = db.reference("/Productos")
ref.push({"tipo":"monitor", "marca":"Powerpack"})
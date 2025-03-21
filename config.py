import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()



#Login
login_api_url = "https://timeortimee.onrender.com/api/data/flutter/login"

# Obtener la URL de la API desde el .env
api_url_obtener_extintores = "https://timeortimee.onrender.com/api/extintores/generales/aspreconsultores/obtener/extintores/Desktop"
API_URL_editar_extintores_api = "https://timeortimee.onrender.com/api/extintores/generales/aspreconsultores/editar/extintor"
API_URL_exportar_extintores_api = "https://timeortimee.onrender.com/api/extintores/generales/exportar/excel/desktop?planta="
API_URL_eliminar_extintor_api = "https://timeortimee.onrender.com/api/extintores/aspreconsultores/generales/eliminar"
API_URL_agregar_extintor_api = "https://timeortimee.onrender.com/api/extintores/aspreconsultores/generales/agregar"
API_URL_exportar_reporte_extintores_api = "https://timeortimee.onrender.com/api/extintores/aspreconsultores/generales/exportar/reporte/completo"
API_URL_ubtener_extintores_inspeccionados_para_descargar = "https://timeortimee.onrender.com/api/extintores/inspecciones/descargar"
API_URL_obtener_extintores_gabinetes_inspeccionados_en_linea_api = "https://timeortimee.onrender.com/api/extintores/aspreconsultores/generales/aspreconsultores/inspecciones/visualizador"
API_URL_ubtener_extintores_no_inspeccionados_para_descargar = "https://timeortimee.onrender.com/api/extintores/no_inspeccionados/descargar"



API_URL_obtener_gabinetes_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/respiracion/obtener/desktop"
API_URL_editar_gabinetes_api = "https://timeortimee.onrender.com/api/gabinetes/equipo/respiracion/aspreconsultores/editar/equipo"
API_URL_exportar_gabinetes_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/respiracion/exportar/desktop?planta="
API_URL_eliminar_gabinete_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/respiracion/eliminar/desktop"
API_URL_agregar_gabinete_api = "https://timeortimee.onrender.com/api/gabinetes/equiporespiracion/aspreconsultores/agregar"
API_URL_exportar_reporte_gabinetes_equipo_respiracion_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/respiracion/exportar/reporte/completo"



API_URL_obtener_gabinetes_equipo_bomberos_psc_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/obtener/desktop"
API_URL_editar_gabinetes_equipo_bomberos_psc_api = "https://timeortimee.onrender.com/api/gabinetes/bomberos/psc/aspreconsultores/editar/gabinete"
API_URL_agregar_gabinete_bomberos_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/psc/agregar/desktop"
API_URL_eliminar_gabinete_bomberos_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/psc/eliminar/desktop"
API_URL_exportar_gabinetes_bomberos_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/exportar/desktop?planta="
API_URL_exportar_reporte_gabinetes_bomberos_psc_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/bomberos/psc/exportar/reporte/completo"



API_URL_obtener_gabinetes_hidrantes_mangueras_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/obtener/desktop"
API_URL_editar_gabinetes_hidrantes_mangueras_api = "https://timeortimee.onrender.com/api/gabinetes/mangueras/hidrantes/aspreconsultores/editar/gabinete"
API_URL_agregar_gabinete_hidrantes_mangueras = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/agregar/desktop"
API_URL_eliminar_gabinete_hidrantes_mangueras_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/eliminar/desktop"
API_URL_exportar_gabinetes_hidrantes_mangueras_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/exportar/desktop?planta="
API_URL_exportar_reporte_hidrantes_mangueras_psc_api = "https://timeortimee.onrender.com/api/gabinetes/aspreconsultores/mangueras/hidrantes/exportar/reporte/completo"


API_URL_obtener_reporte_mensual_gabinetes_extintores_api = "https://timeortimee.onrender.com/api/reporte/completo/exportar/extintores/gabinetes/excel"
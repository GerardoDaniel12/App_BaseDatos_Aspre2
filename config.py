import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()


#Login
login_api_url = os.getenv("login_api_url")

# Obtener la URL de la API desde el .env
api_url_obtener_extintores = os.getenv("API_URL_OBTENER_EXTINTORES")
API_URL_editar_extintores_api = os.getenv("API_URL_editar_extintores_api")
API_URL_exportar_extintores_api = os.getenv("API_URL_exportar_extintores_api")
API_URL_eliminar_extintor_api = os.getenv("API_URL_eliminar_extintor_api")
API_URL_agregar_extintor_api = os.getenv("API_URL_agregar_extintor_api")
API_URL_exportar_reporte_extintores_api = os.getenv("API_URL_exportar_reporte_extintores_api")
API_URL_ubtener_extintores_inspeccionados_para_descargar = os.getenv("API_URL_ubtener_extintores_inspeccionados_para_descargar")
API_URL_obtener_extintores_gabinetes_inspeccionados_en_linea_api = os.getenv("API_URL_obtener_extintores_gabinetes_inspeccionados_en_linea_api")
API_URL_ubtener_extintores_no_inspeccionados_para_descargar = os.getenv("API_URL_ubtener_extintores_no_inspeccionados_para_descargar")



API_URL_obtener_gabinetes_api = os.getenv("API_URL_obtener_gabinetes_api")
API_URL_editar_gabinetes_api = os.getenv("API_URL_editar_gabinetes_api")
API_URL_exportar_gabinetes_api = os.getenv("API_URL_exportar_gabinetes_api")
API_URL_eliminar_gabinete_api = os.getenv("API_URL_eliminar_gabinete_api")
API_URL_agregar_gabinete_api = os.getenv("API_URL_agregar_gabinete_api")
API_URL_exportar_reporte_gabinetes_equipo_respiracion_api = os.getenv("API_URL_exportar_reporte_gabinetes_equipo_respiracion_api")



API_URL_obtener_gabinetes_equipo_bomberos_psc_api = os.getenv("API_URL_obtener_gabinetes_equipo_bomberos_psc_api")
API_URL_editar_gabinetes_equipo_bomberos_psc_api = os.getenv("API_URL_editar_gabinetes_equipo_bomberos_psc_api")
API_URL_agregar_gabinete_bomberos_api = os.getenv("API_URL_agregar_gabinete_bomberos_api")
API_URL_eliminar_gabinete_bomberos_api = os.getenv("API_URL_eliminar_gabinete_bomberos_api")
API_URL_exportar_gabinetes_bomberos_api = os.getenv("API_URL_exportar_gabinetes_bomberos_api")
API_URL_exportar_reporte_gabinetes_bomberos_psc_api = os.getenv("API_URL_exportar_reporte_gabinetes_bomberos_psc_api")



API_URL_obtener_gabinetes_hidrantes_mangueras_api = os.getenv("API_URL_obtener_gabinetes_hidrantes_mangueras_api")
API_URL_editar_gabinetes_hidrantes_mangueras_api = os.getenv("API_URL_editar_gabinetes_hidrantes_mangueras_api")
API_URL_agregar_gabinete_hidrantes_mangueras = os.getenv("API_URL_agregar_gabinete_hidrantes_mangueras")
API_URL_eliminar_gabinete_hidrantes_mangueras_api = os.getenv("API_URL_eliminar_gabinete_hidrantes_mangueras_api")
API_URL_exportar_gabinetes_hidrantes_mangueras_api = os.getenv("API_URL_exportar_gabinetes_hidrantes_mangueras_api")
API_URL_exportar_reporte_hidrantes_mangueras_psc_api = os.getenv("API_URL_exportar_reporte_hidrantes_mangueras_psc_api")


API_URL_obtener_reporte_mensual_gabinetes_extintores_api = os.getenv("API_URL_obtener_reporte_mensual_gabinetes_extintores_api")
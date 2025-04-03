# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import requests
import time


#******************************************************************************************************************************
# servicio para capturar el token de descarga
def obtener_token_con_el_id_rinex(id_rinex, token):
    url = f"https://serviciosgeovisor.igac.gov.co:8080/Geovisor/descargas?cmd=request&tipo=rinex&id={id_rinex}&token={token}"
    
    time.sleep(1)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo un error en la solicitud

        # Analizar la respuesta JSON y extraer el valor de 'token' si existe
        data = response.json()
        token_rinex = data.get('token', None)
        
        return token_rinex
    except requests.exceptions.RequestException as e:
        agregar_log("Error en la solicitud:", e)
        return None
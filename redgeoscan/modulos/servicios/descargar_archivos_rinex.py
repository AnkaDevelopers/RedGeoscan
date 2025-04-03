# Importar modulos redgeoscan
from monitor.log.log import agregar_log

# Importaciones adicionales
import requests
import time
import os

#********************************************************************************************************************************
# Servicio para capturar el token de descarga y descargar el archivo

def descargar_archivo(token, ruta_red_activa_gps, administrador, subcarpeta, nombre_archivo):
    try:
        agregar_log(f"Iniciando proceso para el archivo {nombre_archivo} en la subcarpeta {subcarpeta}...")
        time.sleep(1)
                        
        # Ruta de la carpeta del administrador de la antena
        ruta_red_activa_administrador = os.path.join(ruta_red_activa_gps, administrador)
        ruta_red_activa_administrador_subcarpeta = os.path.join(ruta_red_activa_administrador, subcarpeta)
        
        # Crear las carpetas si no existen
        os.makedirs(ruta_red_activa_administrador_subcarpeta, exist_ok=True)
        agregar_log(f"Carpeta creada/verificada: {ruta_red_activa_administrador_subcarpeta}")
        
        # Ruta completa del archivo que se descargará dentro de la subcarpeta
        ruta_red_activa_administrador_subcarpeta_archivo_rinex = os.path.join(ruta_red_activa_administrador_subcarpeta, nombre_archivo)

        # Verificar si el archivo ya existe
        if os.path.exists(ruta_red_activa_administrador_subcarpeta_archivo_rinex):
            agregar_log(f"El archivo {nombre_archivo} ya existe en la ruta: {ruta_red_activa_administrador_subcarpeta_archivo_rinex}. Descarga omitida.")
            return True  # Retornamos True ya que no hay error y el archivo está disponible
        
        # Construcción de la URL del servicio de descarga con el token proporcionado
        url = f"https://serviciosgeovisor.igac.gov.co:8080/Geovisor/descargas?cmd=download&token={token}"
        agregar_log(f"URL de descarga construida: {url}")
        
        # Encabezados para la solicitud
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        agregar_log("Realizando solicitud GET para la descarga...")
        
        # Realizar la solicitud GET
        response = requests.get(url, headers=headers, stream=True)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            agregar_log(f"Solicitud exitosa. Guardando el archivo en: {ruta_red_activa_administrador_subcarpeta_archivo_rinex}")
            # Guardar el contenido en el archivo
            with open(ruta_red_activa_administrador_subcarpeta_archivo_rinex, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            agregar_log(f"Archivo {nombre_archivo} descargado exitosamente.")
            return True
        else:
            agregar_log(f"Error en la descarga del archivo {nombre_archivo}. Código de estado: {response.status_code}")
            return False
    except Exception as e:
        mensaje_error = f"Error al intentar descargar el archivo {nombre_archivo}: {e}"
        agregar_log(mensaje_error)
        return False


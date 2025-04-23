# Importar modulos redgeoscan
from monitor.log.log import agregar_log

# Importar Utils 
from redgeoscan.utils.cambiar_extencion import ejecutar_crx2rnx_desde_consola

# Importaciones adicionales
import requests
import time
import os
import gzip
import shutil

#********************************************************************************************************************************
# Servicio para capturar el token de descarga y descargar el archivo

def descargar_archivo(token, ruta_red_activa_gps, administrador, subcarpeta, nombre_archivo):
    try:
        agregar_log(f"Iniciando proceso para el archivo {nombre_archivo} en la subcarpeta {subcarpeta}...")
        print(nombre_archivo)
        time.sleep(0.5)
                        
        # Ruta de la carpeta del administrador de la antena
        ruta_red_activa_administrador = os.path.join(ruta_red_activa_gps, administrador)
        ruta_red_activa_administrador_subcarpeta = os.path.join(ruta_red_activa_administrador, subcarpeta)
        
        # Crear las carpetas si no existen
        os.makedirs(ruta_red_activa_administrador_subcarpeta, exist_ok=True)
        agregar_log(f"Carpeta creada/verificada: {ruta_red_activa_administrador_subcarpeta}")
        
        # Ruta completa del archivo descargado
        ruta_comprimido = os.path.join(ruta_red_activa_administrador_subcarpeta, nombre_archivo)
        agregar_log(f"Ruta destino del archivo descargado: {ruta_comprimido}")

        ruta_comprimida = ruta_comprimido[:-3]  # para verificar si ya fue descomprimido

        # Verificar si el archivo ya existe descomprimido
        if os.path.exists(ruta_comprimida):
            agregar_log(f"El archivo ya existe en la ruta: {ruta_comprimido}. Descarga omitida.")
            return True
        
        # URL de descarga
        url = f"https://serviciosgeovisor.igac.gov.co:8080/Geovisor/descargas?cmd=download&token={token}"
        agregar_log(f"URL de descarga construida: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }

        # Solicitud GET
        response = requests.get(url, headers=headers, stream=True)
        
        if response.status_code == 200:
            with open(ruta_comprimido, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            agregar_log(f"Archivo {nombre_archivo} descargado exitosamente.")

            # ✅ Verificar tamaño del archivo descargado
            size_bytes = os.path.getsize(ruta_comprimido)
            if size_bytes <= 1024:
                agregar_log(f"Archivo {nombre_archivo} es muy pequeño (≤ 1 KB). Se omite su uso y no se descomprime.")
                return False

            # ---------- Intentar descomprimir ----------
            ruta_descomprimida = os.path.join(
                ruta_red_activa_administrador_subcarpeta,
                os.path.splitext(nombre_archivo)[0]  # quita la extensión
            )
            try:
                with gzip.open(ruta_comprimido, 'rb') as f_in:
                    with open(ruta_descomprimida, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                agregar_log(f"Archivo descomprimido exitosamente en: {ruta_descomprimida}")

                # ✅ Solo ejecutar la conversión si termina en _MO.crx
                if ruta_descomprimida.lower().endswith("_mo.crx"):
                    exito_conversion = ejecutar_crx2rnx_desde_consola(ruta_descomprimida)

                    # ✅ Si se generó archivo .rnx con sufijo MO, cambiar a .24O
                    if exito_conversion:
                        carpeta = os.path.dirname(ruta_descomprimida)
                        for archivo in os.listdir(carpeta):
                            if archivo.endswith("MO.rnx"):
                                ruta_original = os.path.join(carpeta, archivo)
                                nuevo_nombre = archivo.replace(".rnx", ".24O")
                                ruta_nuevo = os.path.join(carpeta, nuevo_nombre)
                                os.rename(ruta_original, ruta_nuevo)
                                agregar_log(f"Archivo renombrado a: {ruta_nuevo}")
                                break
                else:
                    agregar_log(f"Archivo {ruta_descomprimida} no termina en _MO.crx. Conversión omitida.")

                # Eliminar el archivo comprimido
                time.sleep(1)
                print(ruta_comprimido)
                os.remove(ruta_comprimido)
                agregar_log(f"Archivo comprimido eliminado: {ruta_comprimido}")

                return True

            except Exception as e:
                agregar_log(f"Error al descomprimir el archivo {nombre_archivo}: {e}")
                return False

        else:
            agregar_log(f"Error en la descarga del archivo {nombre_archivo}. Código de estado: {response.status_code}")
            return False

    except Exception as e:
        mensaje_error = f"Error al intentar descargar el archivo {nombre_archivo}: {e}"
        agregar_log(mensaje_error)
        return False

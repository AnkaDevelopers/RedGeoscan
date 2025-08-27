# Importaciones adicionales
from datetime import datetime
import requests
import json
import time
import os

# Importar módulos de monitor
from monitor.log.log import agregar_log



#********************************************************************************************************************************
# Función para realizar la solicitud al servicio y almacenar los datos en `C:\RedGeoscan\docs`
def servicio_administrador_antenas():
    
    try:
        # Define el directorio y nombre base del archivo según la fecha actual
        fecha_actual = datetime.now()
        nombre_base = f"antenas-{fecha_actual.strftime('%d-%B-%Y')}"
        ruta_antenas = os.path.join( r"C:\RedGeoscan\docs" )
        os.makedirs(ruta_antenas, exist_ok=True)  # Asegúrate de que la carpeta exista

        # Buscar archivo existente con la fecha actual
        archivos_existentes = [f for f in os.listdir(ruta_antenas) if f.startswith(nombre_base) and f.endswith('.json')]
        if archivos_existentes:
            # Si existe un archivo con la fecha actual, capturamos su ruta
            ruta_archivo_actual = os.path.join(ruta_antenas, archivos_existentes[0])
            agregar_log(f"Archivo existente para la fecha actual encontrado: {ruta_archivo_actual}. No se realiza la solicitud al servicio.")
            return ruta_archivo_actual, True

        # Si no hay archivo para la fecha actual, continuamos con el consumo del servicio
        agregar_log("No se encontró archivo para la fecha actual. Iniciando solicitud al servicio...")

        # Configuración inicial
        intentos = 0
        max_intentos = 3
        length = 500  # Longitud inicial predeterminada
        url_base = "https://serviciosgeovisor.igac.gov.co:8080/Geovisor/geodesia"
        params = {
            "draw": 1,
            "columns[0][data]": "ID_ESTACION",
            "columns[0][name]": "",
            "columns[0][searchable]": "true",
            "columns[0][orderable]": "false",
            "columns[0][search][value]": "",
            "columns[0][search][regex]": "false",
            "order[0][column]": 0,
            "order[0][dir]": "asc",
            "start": 0,
            "length": length,
            "search[value]": "",
            "search[regex]": "false",
            "cmd": "query_estaciones",
            "tipo": "Activa",
            "administrador": "",
            "estacion": "",
        }

        while intentos < max_intentos:
            try:
                # Realiza la solicitud GET al servicio
                respuesta = requests.get(url_base, params=params, timeout=10)

                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    estaciones = datos.get("estaciones", [])

                    if not estaciones:
                        msj_depuracion = "Advertencia: No se encontraron datos válidos en el campo 'estaciones'."
                        return msj_depuracion, False

                    # Procesamiento de los datos
                    datos_limpios = [
                        {
                            "ADMINISTRADOR": estacion.get("ADMINISTRADOR", ""),
                            "ESTADO": estacion.get("ESTADO", ""),
                            "TIPO_ESTACION": estacion.get("TIPO_ESTACION", ""),
                            "MATERIALIZADA": estacion.get("MATERIALIZADA", ""),
                            "ESTACION": estacion.get("CODIGO", "")
                        }
                        for estacion in estaciones
                    ]

                    # Eliminar archivo JSON anterior si existe
                    archivos_anteriores = [f for f in os.listdir(ruta_antenas) if f.endswith('.json') and f != f"{nombre_base}.json"]
                    
                    for archivo_anterior in archivos_anteriores:
                        
                        ruta_anterior = os.path.join(ruta_antenas, archivo_anterior)
                        os.remove(ruta_anterior)

                        agregar_log(f"Archivo anterior eliminado: {ruta_anterior}")

                    # Guardar los datos en un archivo JSON
                    ruta_archivo = os.path.join(ruta_antenas, f"{nombre_base}.json")
                    
                    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                        json.dump(datos_limpios, archivo, ensure_ascii=False, indent=4)

                    agregar_log(f"Datos guardados correctamente en {ruta_archivo}")
                    return ruta_archivo, True

                else:
                    agregar_log(f"No hay respuesta por parte del servicio (status code: {respuesta.status_code}).")
                    break

            except requests.exceptions.RequestException as e:
                intentos += 1
                agregar_log(f"Error de conexión ({intentos}/{max_intentos}): {e}")
                time.sleep(2) 

        msj_depuracion = f"Falla en el servicio {respuesta}"
        return msj_depuracion, False

    except Exception as e:
        
        msj_depuracion = f"Error inesperado: {e}"
        return msj_depuracion, False

# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import time
import json
import os

#********************************************************************************************************************************
# Función para actualizar el diccionario con los administradores de las antenas
def actualizar_diccionario_con_administradores_antenas(diccionario, ruta):
    try:
        
        # Registrar el inicio del proceso en el log
        agregar_log("Inicio del proceso: Consulta de administradores de antenas.")

        # Ruta al archivo JSON con los datos de las antenas
        ruta_json = ruta

        # Verificar si el archivo existe
        if not os.path.exists(ruta_json):
            msj_depuracion = f"El archivo JSON con los administradores no se encontró en la ruta: {ruta_json}"
            return msj_depuracion, None

        # Cargar los datos del archivo JSON
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            datos_antenas = json.load(archivo)

        # Crear un diccionario para acceder rápidamente por nombre de antena
        mapa_antenas = {
            antena["ESTACION"]: {
                "MATERIALIZADA": antena.get("MATERIALIZADA", "")
            }
            for antena in datos_antenas
        }

        # Iterar sobre los días de rastreo en el diccionario
        for dia, info_dia in diccionario.get("dias_rastreos", {}).items():
            base_subcarpetas = info_dia.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})

            for gps_nombre, gps_info in base_subcarpetas.items():
                antenas_cercanas = gps_info.get("antenas_cercanas", [])

                for antena in antenas_cercanas:
                    nombre_antena = antena.get("NAME")

                    if nombre_antena and nombre_antena in mapa_antenas:
                        # Actualizar la antena con los datos del administrador
                        antena.update(mapa_antenas[nombre_antena])
                        agregar_log(f"Administrador agregado para la antena {nombre_antena}.")
                    else:
                        agregar_log(f"Administrador no encontrado para la antena {nombre_antena}.")

        # Registrar el fin del proceso
        agregar_log("Proceso completado: Actualización de administradores de antenas finalizada.")

        return None, diccionario

    except Exception as e:
        # Registrar cualquier error que ocurra durante el proceso
        msj_depuracion = f"Error durante el proceso de actualización del diccionario: {e}"
        return msj_depuracion, None

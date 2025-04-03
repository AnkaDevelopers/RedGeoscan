# Importar modulos redgeoscan
from redgeoscan.modulos.servicios.obtener_coordenada_antenas_orden_cero import descargar_archivo_sirgas

# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import time

#********************************************************************************************************************************
# Función para actualizar el diccionario con la información de las coordenadas SIRGAS de cada antena
def actualizar_diccionario_con_coordenada(diccionario):
    try:
        agregar_log("Inicio actualización del diccionario con la coordenada SIRGAS.")

        # Iterar sobre los días de rastreo en el diccionario
        for dia, info_dia in diccionario.get("dias_rastreos", {}).items():
            base_subcarpetas = info_dia.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})

            for gps_nombre, gps_info in base_subcarpetas.items():
                antenas_cercanas = gps_info.get("antenas_cercanas", [])

                for antena in antenas_cercanas:
                    nombre_antena = antena.get("NAME")

                    if not nombre_antena:
                        agregar_log(f"Antena sin nombre encontrada en el GPS: {gps_nombre}.")
                        continue

                    # Consumir el servicio para obtener la coordenada SIRGAS
                    time.sleep(0)
                    coordenada = descargar_archivo_sirgas(nombre_antena)

                    if coordenada:
                        # Almacenar la coordenada obtenida
                        antena["ORDEN"] = "0"
                        antena["COORDENADA"] = coordenada
                        agregar_log(f"Coordenada SIRGAS actualizada para la antena {nombre_antena}: {coordenada}.")
                    else:
                        # Dejar vacío si no se encuentra la coordenada
                        antena["ORDEN"] = "1"
                        antena["COORDENADA"] = ""
                        agregar_log(f"No se encontró coordenada SIRGAS para la antena {nombre_antena}.")

        agregar_log("Finalizada la actualización del diccionario con coordenadas SIRGAS.")
        return None, diccionario

    except Exception as e:
        
        msj_depuracion = f"Error durante la actualización del diccionario con coordenadas SIRGAS: {e}"
        return msj_depuracion, None

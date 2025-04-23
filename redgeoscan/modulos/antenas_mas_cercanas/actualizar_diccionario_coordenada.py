# Importar módulos redgeoscan
from redgeoscan.modulos.servicios.obtener_coordenada_antenas_orden_cero import descargar_archivo_sirgas

# Importar módulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
import time

#********************************************************************************************************************************
# Función para actualizar el diccionario con la información de las coordenadas SIRGAS de cada antena
def actualizar_diccionario_con_coordenada(diccionario):
    try:
        agregar_log("Inicio actualización del diccionario con la coordenada SIRGAS.")

        # Recorremos los días de rastreo
        for dia, info_dia in diccionario.get("dias_rastreos", {}).items():
            subcarpetas = info_dia.get("subcarpetas", {})
            base_subcarpetas = subcarpetas.get("Base", {}).get("sub_carpetas", {})
            red_activa = subcarpetas.get("Red activa", "")

            for gps_nombre, gps_info in base_subcarpetas.items():
                antenas_cercanas = gps_info.get("antenas_cercanas", [])

                # Generar ruta donde se almacenarán los archivos de esta antena
                ruta_por_antena = os.path.join(red_activa, gps_nombre)

                for antena in antenas_cercanas:
                    nombre_antena = antena.get("NAME")
                    descarga_estado = antena.get("DESCARGA", "")
                    materializada = antena.get("MATERIALIZADA")

                    if not nombre_antena:
                        agregar_log(f"Antena sin nombre encontrada en el GPS: {gps_nombre}.")
                        continue

                    # Verificar que la descarga esté completa antes de continuar
                    if descarga_estado != "COMPLETA":
                        agregar_log(f"Se omite la antena {nombre_antena} porque la descarga no es completa.")
                        continue

                    agregar_log(f"Solicitando coordenada SIRGAS para antena {nombre_antena} en ruta: {ruta_por_antena}")

                    # Consumir el servicio con ruta personalizada
                    time.sleep(0)
                    coordenada_str = descargar_archivo_sirgas( nombre_antena,ruta_por_antena, materializada )

                    if coordenada_str:
                        partes = coordenada_str.strip().split()

                        if len(partes) >= 10:
                            try:
                                x = partes[6]
                                y = partes[7]
                                z = partes[8]

                                antena["ORDEN"] = "0"
                                antena["COORDENADA"] = coordenada_str
                                antena["x"] = x
                                antena["y"] = y
                                antena["z"] = z

                                agregar_log(f"Coordenadas SIRGAS actualizadas para la antena {nombre_antena}: X={x}, Y={y}, Z={z}.")
                            except Exception as e:
                                agregar_log(f"Error al extraer coordenadas para la antena {nombre_antena}: {e}")
                        else:
                            antena["ORDEN"] = "1"
                            antena["COORDENADA"] = coordenada_str
                            agregar_log(f"Formato inesperado en coordenada para la antena {nombre_antena}.")
                    else:
                        antena["ORDEN"] = "1"
                        antena["COORDENADA"] = ""
                        agregar_log(f"No se encontró coordenada SIRGAS para la antena {nombre_antena}.")

        agregar_log("Finalizada la actualización del diccionario con coordenadas SIRGAS.")
        return None, diccionario

    except Exception as e:
        msj_depuracion = f"Error durante la actualización del diccionario con coordenadas SIRGAS: {e}"
        return msj_depuracion, None

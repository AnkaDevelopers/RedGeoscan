import os
from shutil import move
from redgeoscan.modulos.validacion_estructura_proyecto.obtener_lista_subcarpetas import obtener_lista_sub_carpetas
from monitor.log.log import agregar_log
from os.path import join, dirname, basename

def sub_carpetas_gps(diccionario_proyecto):
    try:
        agregar_log("Inicio de procesamiento de subcarpetas en la carpeta 'Base'...")

        nuevos_dias_rastreos = {}

        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            subcarpetas = info.get("subcarpetas", {})
            
            if "Base" in subcarpetas:
                ruta_base = subcarpetas["Base"] if isinstance(subcarpetas["Base"], str) else subcarpetas["Base"]["ruta"]

                # Verificar si el nombre del día termina en '-sinGPS'
                es_sin_gps = "-completo" in ruta_base
                dia_original = dia.replace("-completo", "") if es_sin_gps else dia

                rpta, subcarpetas_base = obtener_lista_sub_carpetas(ruta_base, dia_original)

                if not subcarpetas_base:
                    agregar_log(rpta)
                    agregar_log(f"No se encontraron subcarpetas GPS en la carpeta 'Base' para el día {dia}")

                    # Si no tenía '-sinGPS', entonces se lo agregamos
                    if not es_sin_gps:
                        ruta_dia = dirname(ruta_base)
                        nueva_ruta = ruta_dia + "-completo"
                        try:
                            move(ruta_dia, nueva_ruta)
                            agregar_log(f"Se renombró la carpeta del día {dia} a {nueva_ruta} por falta de subcarpetas GPS.")
                        except Exception as err:
                            agregar_log(f"Error al renombrar la carpeta del día {dia}: {err}")
                else:
                    # Si tiene GPS y estaba con '-sinGPS', lo restauramos
                    if es_sin_gps:
                        ruta_dia = dirname(ruta_base)
                        nueva_ruta = ruta_dia.replace("-completo", "")
                        try:
                            move(ruta_dia, nueva_ruta)
                            agregar_log(f"Se restauró el nombre original de la carpeta del día {dia_original} a {nueva_ruta}.")
                            ruta_base = join(nueva_ruta, "Base")  # nueva ruta a la carpeta Base
                        except Exception as err:
                            agregar_log(f"Error al restaurar el nombre de la carpeta del día {dia_original}: {err}")
                    
                    # Generar las subcarpetas GPS con rutas completas
                    subcarpetas_base = {nombre: join(ruta_base, nombre) for nombre in subcarpetas_base}
                    subcarpetas["Base"] = {
                        "ruta": ruta_base,
                        "sub_carpetas": subcarpetas_base
                    }
                    nuevos_dias_rastreos[dia_original] = {"subcarpetas": subcarpetas}
                    agregar_log(f"Subcarpetas de 'Base' actualizadas para el día {dia_original}")
            else:
                agregar_log(f"La carpeta 'Base' no está presente en las subcarpetas para el día {dia}")
                # Si no tiene Base, no se agrega

        diccionario_proyecto["dias_rastreos"] = nuevos_dias_rastreos
        agregar_log("Procesamiento de subcarpetas en 'Base' completado exitosamente.")
        return None, diccionario_proyecto

    except Exception as e:
        msj = f"Error al procesar subcarpetas en 'Base': {e}"
        return msj, None

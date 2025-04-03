# Importar modulos monitor
from monitor.responder_correo.responder_correo import obtener_mensaje_por_id
from monitor.responder_correo.responder_correo import enviar_correo_proceso_redgeoscan
from monitor.log.log import agregar_log

# Importaciones adiconales
import os
import re
import time

def procesar_archivos_gps(diccionario_proyecto):
    try:
        agregar_log("Inicio de procesamiento de archivos GPS en las carpetas 'Base'...")

        # Expresión regular para extensiones dinámicas
        patron_extensiones = re.compile(r"\.\d{2}[on]$|\.nav$|\.obs$")

        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            subcarpetas = info.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})

            # Crear una lista de subcarpetas para iterar sobre ella, ya que estamos modificando el diccionario
            subcarpetas_a_eliminar = []

            for gps_nombre, gps_ruta in subcarpetas.items():
                agregar_log(f"Procesando carpeta GPS: {gps_nombre} en {gps_ruta}")

                archivos_encontrados = {}

                # Iterar sobre los archivos en la carpeta GPS
                for archivo in os.listdir(gps_ruta):
                    archivo_ruta = os.path.join(gps_ruta, archivo)

                    if os.path.isfile(archivo_ruta) and os.path.getsize(archivo_ruta) > 1024:
                        extension = os.path.splitext(archivo)[1].lower()

                        # Verificar si la extensión coincide con .pos, .obs o el patrón dinámico
                        if extension in [".pos"] or patron_extensiones.match(extension):
                            if extension not in archivos_encontrados:
                                archivos_encontrados[extension] = archivo_ruta

                # Verificar condiciones
                archivo_pos = archivos_encontrados.get(".pos")
                archivos_secundarios = {
                    ext[1:]: ruta for ext, ruta in archivos_encontrados.items() if ext in [".obs"] or patron_extensiones.match(ext)
                }

                if archivo_pos:
                    subcarpetas[gps_nombre] = {
                        "ruta": gps_ruta,
                        "archivos": {"pos": archivo_pos}
                    }
                    agregar_log(f"Archivo .pos encontrado: {archivo_pos} para {gps_nombre}")
                elif len(archivos_secundarios) >= 2:
                    subcarpetas[gps_nombre] = {
                        "ruta": gps_ruta,
                        "archivos": archivos_secundarios
                    }
                    agregar_log(f"Archivos secundarios encontrados: ")
                    agregar_log(f"{archivos_secundarios} para {gps_nombre} ")
                else:
                    msj = f"No se encontraron archivos rinex en {gps_ruta}"
                    agregar_log(msj)
                    #traza_conversacion = obtener_mensaje_por_id(id_correo)
                    #enviar_correo_proceso_redgeoscan(traza_conversacion, msj)

                    # Marcar la subcarpeta para eliminación
                    subcarpetas_a_eliminar.append(gps_nombre)
                    agregar_log(f"Subcarpeta {gps_nombre} marcada para eliminación debido a la falta de archivos RINEX.")
            
            # Eliminar las subcarpetas que no cumplen con los requisitos
            for gps_nombre in subcarpetas_a_eliminar:
                del subcarpetas[gps_nombre]
                agregar_log(f"Subcarpeta {gps_nombre} eliminada.")

        agregar_log("Procesamiento de archivos GPS completado exitosamente.")
        return None, diccionario_proyecto

    except Exception as e:
        msj = f"Error al procesar archivos GPS: {e}"
        agregar_log(msj)
        return msj, None

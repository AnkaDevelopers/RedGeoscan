# Importar modulos monitor
from monitor.responder_correo.responder_correo import obtener_mensaje_por_id
from monitor.responder_correo.responder_correo import enviar_correo_proceso_redgeoscan
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
import re
import time
import shutil

def procesar_archivos_gps(diccionario_proyecto):
    try:
        agregar_log("Inicio de procesamiento de archivos GPS en las carpetas 'Base'...")

        # Expresión regular para extensiones tipo .24O, .25n, etc.
        patron_extensiones = re.compile(r"\.\d{2}[onON]$|\.obs$|\.OBS$|\.nav$|\.NAV$")

        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            subcarpetas = info.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})

            subcarpetas_a_eliminar = []
            subcarpetas_a_renombrar = []

            for gps_nombre in list(subcarpetas.keys()):
                gps_ruta = subcarpetas[gps_nombre]
                agregar_log(f"Procesando carpeta GPS: {gps_nombre} en {gps_ruta}")

                archivos_encontrados = {}

                for archivo in os.listdir(gps_ruta):
                    archivo_ruta = os.path.join(gps_ruta, archivo)

                    if os.path.isfile(archivo_ruta):
                        extension = os.path.splitext(archivo)[1]

                        if extension.lower() == ".pos" and os.path.getsize(archivo_ruta) <= 1024:
                            os.remove(archivo_ruta)
                            agregar_log(f"Archivo .pos eliminado por ser ≤1KB: {archivo_ruta}")
                            continue

                        if os.path.getsize(archivo_ruta) > 1024 and (
                            extension.lower() == ".pos" or patron_extensiones.match(extension)
                        ):
                            if extension.lower() not in archivos_encontrados:
                                archivos_encontrados[extension.lower()] = archivo_ruta

                archivo_pos = archivos_encontrados.get(".pos")
                archivos_secundarios = {
                    ext[1:]: ruta for ext, ruta in archivos_encontrados.items()
                    if ext in [".obs", ".obs"] or patron_extensiones.match(ext)
                }

                if archivo_pos:
                    subcarpetas[gps_nombre] = {
                        "ruta": gps_ruta,
                        "archivos": {"pos": archivo_pos}
                    }
                    agregar_log(f"Archivo .pos encontrado: {archivo_pos} para {gps_nombre}")

                    # Si el nombre termina en -vacio, renombrar carpeta
                    if gps_nombre.endswith("-vacio"):
                        nuevo_nombre = gps_nombre.replace("-vacio", "")
                        nueva_ruta = gps_ruta.replace("-vacio", "")

                        try:
                            os.rename(gps_ruta, nueva_ruta)
                            agregar_log(f"Carpeta renombrada físicamente a: {nueva_ruta}")
                            subcarpetas[nuevo_nombre] = subcarpetas[gps_nombre]
                            subcarpetas[nuevo_nombre]["ruta"] = nueva_ruta
                            del subcarpetas[gps_nombre]
                        except Exception as e:
                            agregar_log(f"Error al renombrar la carpeta {gps_ruta} a {nueva_ruta}: {e}")

                elif len(archivos_secundarios) >= 2:
                    subcarpetas[gps_nombre] = {
                        "ruta": gps_ruta,
                        "archivos": archivos_secundarios
                    }
                    agregar_log(f"Archivos secundarios encontrados:")
                    agregar_log(f"{archivos_secundarios} para {gps_nombre}")

                    # Si el nombre termina en -vacio, renombrar carpeta
                    if gps_nombre.endswith("-vacio"):
                        nuevo_nombre = gps_nombre.replace("-vacio", "")
                        nueva_ruta = gps_ruta.replace("-vacio", "")

                        try:
                            os.rename(gps_ruta, nueva_ruta)
                            agregar_log(f"Carpeta renombrada físicamente a: {nueva_ruta}")
                            subcarpetas[nuevo_nombre] = subcarpetas[gps_nombre]
                            subcarpetas[nuevo_nombre]["ruta"] = nueva_ruta
                            del subcarpetas[gps_nombre]
                        except Exception as e:
                            agregar_log(f"Error al renombrar la carpeta {gps_ruta} a {nueva_ruta}: {e}")

                else:
                    gps_nuevo_nombre = gps_nombre + "-vacio"
                    nueva_ruta = gps_ruta + "-vacio"

                    try:
                        os.rename(gps_ruta, nueva_ruta)
                        agregar_log(f"Carpeta renombrada físicamente a: {nueva_ruta}")
                    except Exception as e:
                        agregar_log(f"Error al renombrar la carpeta {gps_ruta} a {nueva_ruta}: {e}")

                    del subcarpetas[gps_nombre]
                    subcarpetas_a_eliminar.append(gps_nuevo_nombre)
                    agregar_log(f"Subcarpeta lógica renombrada como {gps_nuevo_nombre} y marcada para eliminación.")

            # Eliminar del diccionario las vacías
            for gps_nombre in subcarpetas_a_eliminar:
                if gps_nombre in subcarpetas:
                    del subcarpetas[gps_nombre]
                agregar_log(f"Subcarpeta {gps_nombre} eliminada del diccionario.")

        agregar_log("Procesamiento de archivos GPS completado exitosamente.")
        return None, diccionario_proyecto

    except Exception as e:
        msj = f"Error al procesar archivos GPS: {e}"
        agregar_log(msj)
        return msj, None

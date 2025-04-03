# Importar modulos de monitor
from config import config
from monitor.log.log import agregar_log

# Importaciones adicionales
import os

#*****************************************************************************************************
# Función para actualizar el diccionario solo con archivos .pos
def actualizar_diccionario_con_pos(diccionario_sub_carpeta_gps):

    try:
        agregar_log("Iniciando actualización del diccionario con archivos .pos...")

        # Iterar sobre los días de rastreo
        for dia, info in diccionario_sub_carpeta_gps.get("dias_rastreos", {}).items():
            agregar_log(f"Procesando día de rastreo: {dia}")

            # Asegurar que la clave 'subcarpetas' y 'Base' existen
            subcarpetas = info.get("subcarpetas", {})
            base = subcarpetas.get("Base", {})

            if not base or "sub_carpetas" not in base:
                agregar_log(f"Clave 'Base' o 'sub_carpetas' faltante en el día {dia}.")
                continue

            # Iterar sobre las subcarpetas
            for gps_nombre, gps_info in base["sub_carpetas"].items():
                agregar_log(f"Procesando subcarpeta: {gps_nombre}")

                # Obtener la ruta de la subcarpeta
                ruta_subcarpeta = gps_info.get("ruta")
                if not ruta_subcarpeta or not os.path.exists(ruta_subcarpeta):
                    agregar_log(f"La ruta de la subcarpeta {gps_nombre} no existe: {ruta_subcarpeta}")
                    continue

                # Buscar archivos .pos en la ruta de la subcarpeta
                archivo_pos = None
                for archivo in os.listdir(ruta_subcarpeta):
                    if archivo.lower().endswith(".pos"):
                        ruta_archivo = os.path.join(ruta_subcarpeta, archivo)
                        if os.path.getsize(ruta_archivo) > 1024:  # Verificar que pese más de 1 KB
                            archivo_pos = ruta_archivo
                            break

                # Actualizar el diccionario con la ruta del archivo .pos si se encontró
                if archivo_pos:
                    agregar_log(f"Archivo .pos válido encontrado en {gps_nombre}: {archivo_pos}")
                    gps_info["archivos"]["pos"] = archivo_pos
                else:
                    agregar_log(f"No se encontró archivo .pos válido en {gps_nombre}.")
                    gps_info["archivos"].pop("pos", None)  # Eliminar clave 'pos' si no es válida

        agregar_log("Actualización completada exitosamente.")
        return None, diccionario_sub_carpeta_gps

    except Exception as e:
        msj_depuracion = f"Error al actualizar el diccionario: {e}"
        return msj_depuracion, None


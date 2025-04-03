# Importar modulos redgeoscan
from redgeoscan.modulos.validacion_estructura_proyecto.obtener_lista_subcarpetas import obtener_lista_sub_carpetas

# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
from os.path import join

#*******************************************************************************************************************
#   Modulo que se encarga de traer la información de las rutas de las carpetas gps
def sub_carpetas_gps(diccionario_proyecto):

    try:
        agregar_log("Inicio de procesamiento de subcarpetas en la carpeta 'Base'...")

        # Iterar sobre los días de rastreo
        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            subcarpetas = info.get("subcarpetas", {})
            
            # Verificar si "Base" está presente en las subcarpetas
            if "Base" in subcarpetas:
                ruta_base = subcarpetas["Base"] if isinstance(subcarpetas["Base"], str) else subcarpetas["Base"]["ruta"]

                # Obtener las subcarpetas de "Base"
                rpta, subcarpetas_base = obtener_lista_sub_carpetas(ruta_base, dia)

                if not subcarpetas_base:
                    agregar_log(rpta)
                    msj = f"No se encontraron subcarpetas GPS en la carpeta 'Base' para el día {dia}"
                    return msj, None
                else:
                    # Generar subcarpetas con rutas completas
                    subcarpetas_base = {nombre: join(ruta_base, nombre) for nombre in subcarpetas_base}

                # Actualizar "Base" en el diccionario
                subcarpetas["Base"] = {
                    "ruta": ruta_base,
                    "sub_carpetas": subcarpetas_base
                }

                agregar_log(f"Subcarpetas de 'Base' actualizadas para el día {dia}")
            else:
                msj = f"La carpeta 'Base' no está presente en las subcarpetas para el día {dia}"
                return msj , None

        agregar_log("Procesamiento de subcarpetas en 'Base' completado exitosamente.")
        return None, diccionario_proyecto

    except Exception as e:
        msj: f"Error al procesar subcarpetas en 'Base': {e}"

        return msj,  None

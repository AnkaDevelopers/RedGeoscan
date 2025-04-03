# Importar modulos redgeoscan
from redgeoscan.modulos.validacion_estructura_proyecto.obtener_lista_subcarpetas import obtener_lista_sub_carpetas

# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
from os.path import join


def sub_carpeta_info(diccionario_proyecto_uno):

    try:
        agregar_log("Inicio de procesamiento de días de rastreos...")

        # Crear un nuevo diccionario para almacenar los resultados
        resultado = {
            "nombre": diccionario_proyecto_uno["nombre"],
            "ruta_principal": diccionario_proyecto_uno["ruta_principal"],
            "dias_rastreos": {}
        }

        # Iterar sobre los días de rastreo
        for dia, info in diccionario_proyecto_uno["dias_rastreos"].items():
            
            # Obtener subcarpetas de la ruta del día
            res, subcarpetas = obtener_lista_sub_carpetas(info["ruta"], dia)

            if not subcarpetas:
                agregar_log(res)
                msj = f"No se encontraron subcarpetas para el día {dia}"
                return  msj, None
            else:
                # Generar subcarpetas con rutas completas
                subcarpetas = {nombre: join(info["ruta"], nombre) for nombre in subcarpetas}

            # Actualizar la información del día en el resultado
            resultado["dias_rastreos"][dia] = {
                "subcarpetas": subcarpetas
            }

        agregar_log("Procesamiento completado exitosamente.")
        return None, resultado

    except Exception as e:
        msj = f"Error al procesar días de rastreos:{e}"
        return msj, None

# Importar modulos de monitor
from monitor.log.log import agregar_log


def proyecto_info(ruta_proyecto,respuesta_estructura, respuesta_dias_rastreos, nombre_proyecto):

    # Mensaje de depuración
    agregar_log("Generando diccionario 1...")
    
    try:
        
        # Crear el diccionario con días de rastreos
        dias_rastreos = {
            dia: {"ruta": f"{respuesta_estructura}\\{dia}"}
            for dia in respuesta_dias_rastreos
        }
        
        # Crear el diccionario del proyecto
        diccionario_proyecto_uno = {
            "nombre": nombre_proyecto,
            "ruta_principal": ruta_proyecto,
            "ruta": respuesta_estructura,
            "dias_rastreos": dias_rastreos
        }

        # Mensaje de depuración
        agregar_log("Diccionario generado exitosamente.")
        return None, diccionario_proyecto_uno
    
    except Exception as e:
        msj = f"Error al generar el diccionario: \n {e}"
        return msj, None
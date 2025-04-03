# Importar modulos monitor
from monitor.log.log import agregar_log

# Otras Importaciones 
import json
import os

#*************************************************************************************
# Funcion que se encarga de guardar el diccionario como un.json oculto
def guardar_diccionario_oculto(diccionario):
    try:
        # Obtiene la ruta principal del diccionario
        ruta_principal = diccionario.get("ruta_principal")
        agregar_log(f"Ruta_principal: {ruta_principal}")

        if not ruta_principal:
            msj_depuracion = "La clave 'ruta_principal' no está presente en el diccionario o está vacía."
            return msj_depuracion,None

        # Verifica si la ruta principal existe
        if not os.path.exists(ruta_principal):
            msj_depuracion = f"La ruta principal no existe: {ruta_principal}"
            return msj_depuracion,None

        # Extrae el nombre del proyecto de la ruta principal
        nombre_proyecto = os.path.basename(ruta_principal)
        agregar_log(f"Nombre_proyecto: {nombre_proyecto}")

        if not nombre_proyecto:
            msj_depuracion = "No se pudo extraer el nombre del proyecto de la ruta principal."
            return msj_depuracion,None

        # Define el nombre del archivo JSON oculto
        nombre_archivo = f".{nombre_proyecto}.json"
        ruta_archivo = os.path.join(ruta_principal, nombre_archivo)
        agregar_log(f"Ruta_archivo: {ruta_archivo}")

        # Verifica si la ruta tiene permisos de escritura
        if not os.access(ruta_principal, os.W_OK):
            msj_depuracion = f"No se tiene permiso de escritura en la carpeta: {ruta_principal}"
            return msj_depuracion,None

        # Verifica si el archivo ya existe
        if os.path.exists(ruta_archivo):
            if not os.access(ruta_archivo, os.W_OK):
                msj_depuracion = f"El archivo existente no se puede escribir: {ruta_archivo}"
                return msj_depuracion,None

            # Comprueba si el archivo está oculto y lo reemplaza
            if os.name == 'nt':
                try:
                    atributos = os.popen(f'attrib "{ruta_archivo}"').read()
                    if 'H' in atributos:
                        agregar_log(f"El archivo está oculto: {ruta_archivo}")
                        os.system(f'attrib -h "{ruta_archivo}"')
                        agregar_log(f"Archivo desocultado temporalmente: {ruta_archivo}")
                except Exception as e:
                    msj_depuracion = f"Error al verificar o desocultar el archivo existente: {e}"
                    return msj_depuracion,None

        # Intenta guardar el archivo
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo_json:
                json.dump(diccionario, archivo_json, indent=4, ensure_ascii=False)
            agregar_log(f"Archivo JSON guardado correctamente: {ruta_archivo}")
        except PermissionError:
            msj_depuracion = f"Error de permisos al intentar escribir el archivo: {ruta_archivo}"
            return msj_depuracion,None
        except Exception as e:
            msj_depuracion = f"Error inesperado al intentar escribir el archivo JSON: {e}"
            return msj_depuracion,None

        # Marca el archivo como oculto en sistemas Windows
        if os.name == 'nt':
            try:
                comando = f'attrib +h "{ruta_archivo}"'
                os.system(comando)
                agregar_log(f"Archivo marcado como oculto: {ruta_archivo}")
            except Exception as e:
                agregar_log(f"Error al marcar el archivo como oculto: {e}")

        mensaje_exito = f"Archivo JSON oculto guardado exitosamente como: {ruta_archivo}"
        agregar_log(mensaje_exito)
        return None, True

    except Exception as e:
        msj_depuracion = f"Error al guardar el archivo JSON oculto: {e}"
        return msj_depuracion,None

# Importar modulos de monitor
from config import config
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
from datetime import datetime

# Ruta fija donde buscar el archivo
ruta_token_txt = config.ruta_token

#************************************************************************************************
# Función para actualizar el archivo del token principal
def actualizar_token_principal(token_principal):

    try:
        # Verificar si el directorio existe; si no, crearlo
        if not os.path.exists(ruta_token_txt):
            os.makedirs(ruta_token_txt)
            agregar_log(f"Directorio creado: {ruta_token_txt}")

        # Buscar y eliminar archivos existentes que contengan 'token-principal'
        for archivo in os.listdir(ruta_token_txt):
            if "token-principal" in archivo and archivo.endswith('.txt'):
                ruta_archivo_existente = os.path.join(ruta_token_txt, archivo)
                os.remove(ruta_archivo_existente)
                agregar_log(f"Archivo existente eliminado: {ruta_archivo_existente}")

        # Crear un nuevo archivo con el token actualizado
        fecha_hora_actual = datetime.now()
        nombre_archivo = fecha_hora_actual.strftime("%H-%M-%d-%m-%y") + "-token-principal.txt"
        ruta_nuevo_archivo = os.path.join(ruta_token_txt, nombre_archivo)

        # Escribir el nuevo token en el archivo
        with open(ruta_nuevo_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(token_principal)
        agregar_log(f"Nuevo archivo de token creado: {ruta_nuevo_archivo}")

        # Retornar True si todo funciona correctamente
        return None, True

    except Exception as e:
        
        msj_depuracion = f"Error al actualizar el archivo del token principal: {e}"
        return msj_depuracion, None

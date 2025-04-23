# Importar modulos de monitor
from config import config
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
import time

# Ruta fija donde buscar el archivo
ruta_token = config.ruta_token

#************************************************************************************************
# Función para validar si un archivo es válido por tiempo (en minutos)
def archivo_valido_por_tiempo(ruta_archivo, minutos):
    
    try:
        
        # Capturamos el tiempo actual en segundos desde el epoch (1970-01-01 00:00:00 UTC)
        tiempo_actual = time.time()

        # Obtenemos el tiempo de la última modificación del archivo en segundos desde el epoch
        tiempo_modificacion = os.path.getmtime(ruta_archivo)

        # Calculamos la diferencia de tiempo entre el tiempo actual y el tiempo de modificación
        # Dividimos por 60 para convertir de segundos a minutos
        diferencia_tiempo = (tiempo_actual - tiempo_modificacion) / 60

        # Registrar en el log que el archivo ha sido validado con éxito
        agregar_log(f"El archivo {ruta_archivo} tiene {diferencia_tiempo:.2f} minutos de antigüedad.")

        # Devolvemos True si la diferencia de tiempo es menor o igual al límite establecido
        # Esto indica que el archivo es reciente (válido)
        return diferencia_tiempo <= minutos

    except Exception as e:
        # En caso de cualquier error, registramos el mensaje de error en el log
        agregar_log(f"Error al verificar tiempo del archivo {ruta_archivo}: {e}")

        # Devolvemos False porque no pudimos validar el tiempo del archivo
        return False

#************************************************************************************************
# Función para buscar y leer el archivo con el token principal en la carpeta `docs`
def buscar_y_leer_archivo_token():
    
    agregar_log("Buscando token en base...")
    
    # Verificar si la carpeta especificada existe
    if not os.path.isdir(ruta_token):
        
        # Si la carpeta no existe, se registra un mensaje y se retorna una cadena vacía
        agregar_log(f'La carpeta {ruta_token} no existe.')
        return None, 1

    # Buscar archivos en la carpeta cuyo nombre contenga 'token-principal' y terminen en '.txt'
    token_txt = [archivo for archivo in os.listdir(ruta_token)
                 if "token-principal" in archivo and archivo.endswith('.txt')]

    # Si no se encuentran archivos que cumplan los criterios, se notifica y se retorna una cadena vacía
    if not token_txt:
        agregar_log('No se encontró un archivo txt con el token.')
        return None, 1

    # Seleccionar el primer archivo que cumple con el criterio
    token_txt_encontrado = token_txt[0]

    # Construir la ruta completa del archivo seleccionado
    ruta_txt = os.path.join(ruta_token, token_txt_encontrado)

    # Verificar si el archivo tiene menos de 20 minutos de antigüedad
    if not archivo_valido_por_tiempo(ruta_txt, minutos=10):
        # Si el archivo es demasiado antiguo, se registra un mensaje y se retorna una cadena vacía
        agregar_log(f'El archivo {ruta_txt} tiene más de 20 minutos de antigüedad.')
        return None, 1

    # Intentar leer el token_principal del archivo
    try:
        
        # Abrir el archivo en modo lectura con codificación UTF-8
        with open(ruta_txt, "r", encoding="utf8") as archivo:
            
            # Leer todo el token_principal del archivo
            token_principal = archivo.read()
            
        # Registrar en el log que el archivo fue leído correctamente
        agregar_log(f"El archivo {ruta_txt} se leyó correctamente.")
        
        # Retornar el token_principal leído si todo es exitoso
        return None, token_principal
    
    except Exception as e:
        # Si ocurre un error al leer el archivo, se registra el error en el log y se retorna una cadena vacía
        msj_depuracion = f"Error al leer el archivo {ruta_txt}: {e}"
        return msj_depuracion, 0

import os
from datetime import datetime, timedelta

def crear_archivo_con_fecha_y_hora(contenido):
    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now()
    nombre_archivo = fecha_hora_actual.strftime("%H-%M-%d-%m-%y") + "-token-principal.txt"
    
    # Ruta al nivel del componente actual
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(ruta_actual, nombre_archivo)
    
    # Verificar si ya existe un archivo con el patrón "*-token-principal.txt"
    for archivo in os.listdir(ruta_actual):
        if archivo.endswith("-token-principal.txt"):
            archivo_existente = os.path.join(ruta_actual, archivo)
            try:
                os.remove(archivo_existente)
                print(f"Archivo existente eliminado: {archivo_existente}")
            except Exception as e:
                print(f"Error al eliminar el archivo existente: {e}")

    # Crear y escribir el nuevo archivo
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        print(f"Archivo creado exitosamente: {ruta_archivo}")
    except Exception as e:
        print(f"Error al crear el archivo: {e}")


# Función para buscar y leer el archivo con el token principal
def buscar_y_leer_archivo_token():
    
    # Obtener la ruta del directorio actual
    ruta = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar archivos que contengan el string 'token-principal' en su nombre
    token_txt = [archivo for archivo in os.listdir(ruta) 
                 if "token-principal" in archivo and archivo.endswith('txt')]
    
    # Validamos en caso de que el archivo no exista
    if not token_txt:
        print('No se encontró un archivo txt con el token')
        return ""
    
    # Seleccionamos el primer archivo encontrado
    token_txt_encontrado = token_txt[0]
    ruta_txt = os.path.join(ruta, token_txt_encontrado)
    
    # Validar si el archivo tiene máximo 30 minutos de creado
    tiempo_creacion = datetime.fromtimestamp(os.path.getctime(ruta_txt))
    tiempo_actual = datetime.now()
    if tiempo_actual - tiempo_creacion > timedelta(minutes=10):
        print('El archivo tiene más de 30 minutos de antigüedad')
        return ""
    
    # Leer el contenido del archivo si es válido
    try:
        with open(ruta_txt, "r", encoding="utf8") as archivo:
            contenido = archivo.read()
        return contenido 
    except Exception as e:
        print("Error al leer el archivo:", e)
        return ""  
    
   
    
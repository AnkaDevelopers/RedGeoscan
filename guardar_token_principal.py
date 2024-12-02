import os
from datetime import datetime

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

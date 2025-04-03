# Importar modulos redgeoscan
from redgeoscan.modulos.validacion_estructura_proyecto.buscar_carpeta import buscar_carpeta_en_estructura

# Importar modulos de monitor
from monitor.log.log import agregar_log
import time

#**********************************************************************************************************
# Función para Validar la estructura del proyecto
def validar_carpetacion(ruta_carpeta_proyecto):

    # Lista de la carpetacion de un proyecto
    lista_carpetacion = ['Procesamiento','1.Topografia','Rastreos']

    try:
        agregar_log("Inicio Validación de estructura proyecto....")
        ruta_full = ruta_carpeta_proyecto
        
        for carpeta in lista_carpetacion:
            
            # Validar la estructura de carpetas del proyecto
            #print(ruta_full) 
            #print(carpeta) 

            ruta = ruta_full
            ruta_full = buscar_carpeta_en_estructura(ruta_full, carpeta) 
        
            # Validamos que la carpeta Procesamiento exista en el proyecto
            if not ruta_full:
                msj = f'Carpeta "{carpeta}" no fue encontrada en la ruta {ruta}'
                print(msj)
                return msj, None

            # Mensajde de depuración
            agregar_log("Ruta encontrada: " + ruta_full)
            
        
        # Mensaje de depuración
        agregar_log("Ruta completa: " + ruta_full)
        return None, ruta_full
        
    except Exception as e:
        
        # Mensaje de depuración
        msj = f"Ocurrio un error al validar la estructura \n {e}"
        return msj, None
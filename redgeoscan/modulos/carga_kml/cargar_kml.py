# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import pandas as pd
import os

# ***************************************************************************************************************
# Funcion para cargar el archivo excel con las antenas
def cargar_kml(ruta_archivo_excel_kml):
    
    try:

        # Mensaje de depuracion carga de base KML
        agregar_log("Cargando Base informacion antenas KML...")
    
        # Verificar si el archivo existe
        if not os.path.exists(ruta_archivo_excel_kml):
            agregar_log(f"No se encontró el archivo KML en la ruta: {ruta_archivo_excel_kml}")
            return None
        
        # Cargamos la base de antenas KML
        data_frame_kml = pd.read_excel(ruta_archivo_excel_kml)

        # Validar si contiene datos necesarios
        if data_frame_kml.empty:
            agregar_log("El archivo KML está vacío.")
            return None
        
        # Mensaje de depuración
        agregar_log("Carga de la base de antenas KML fue exitosa.")
        return data_frame_kml

    except ValueError as e:
        # Error de formato del archivo Excel
        agregar_log(f"El archivo KML no tiene un formato válido: {e}")
        return None
    
    except Exception as e:
        # Mensaje de depuración con detalles del error
        agregar_log(f"No se pudo cargar el archivo KML: {e}")
        return None
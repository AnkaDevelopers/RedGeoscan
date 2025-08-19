# Importar modulos de monitor 
from monitor.log.log import agregar_log

# Importaciones adicionales
import difflib
import os

def buscar_carpeta_en_estructura(origen, nombre_carpeta):
    # Porcentaje de similitud
    umbral_similitud = 0.7

    try:
        # Lista los elementos del nivel actual en la ruta origen
        elementos = os.listdir(origen)

        # Filtrar solo las carpetas
        carpetas = [d for d in elementos if os.path.isdir(os.path.join(origen, d))]

        # Normalizar el parámetro de búsqueda
        nombre_carpeta_normalizado = nombre_carpeta.lower().strip().replace(":", "")
        
        for d in carpetas:
            # Normalizamos el nombre de la carpeta actual
            nombre_actual = d.lower().strip().replace(":", "")

            # Verificamos similitud usando difflib
            similitud = difflib.SequenceMatcher(None, nombre_carpeta_normalizado, nombre_actual).ratio()

            # Si la similitud es mayor o igual al umbral, consideramos que es la carpeta buscada
            if similitud >= umbral_similitud:
                return os.path.join(origen, d)

    except Exception as e:
        agregar_log("Error al acceder a la ruta")
        agregar_log(e)
        return None

    # Si no se encuentra la carpeta, devolver None 
    return None



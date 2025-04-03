# Importaciones adicionales
import requests

#********************************************************************************************************************************
# Servicio para descargar la coordenada de las antenas
def descargar_archivo_sirgas(nombre_archivo):
    
    # URL del archivo
    url = f"https://www.sirgas.org/fileadmin/docs/SIRGAS_CRD/{nombre_archivo.upper()}.XYZ"
    
    # Realizar la solicitud GET al servicio
    response = requests.get(url)
    
    # Verificar el estado de la respuesta
    if response.status_code != 200:
        return False

    # Decodificar el contenido de la respuesta en texto y dividirlo en líneas
    contenido = response.text
    lineas = contenido.splitlines()

    # Obtener la última línea
    ultima_linea = lineas[-2] if lineas else None

    return ultima_linea

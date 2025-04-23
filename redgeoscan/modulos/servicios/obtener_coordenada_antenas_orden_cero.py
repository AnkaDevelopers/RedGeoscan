# Importaciones adicionales
import requests
import time
import os

#********************************************************************************************************************************
# Servicio para descargar la coordenada de las antenas
def descargar_archivo_sirgas(nombre_archivo, ruta_por_antena, materializada):
    print(f"nombre_archivo:  {nombre_archivo}")
    print(f"ruta_por_antena:  {ruta_por_antena}")
    print(f"materializada:  {materializada}")

    time.sleep(1)  # Ajusta si necesitas pruebas largas

    # URL del archivo
    url = f"https://www.sirgas.org/fileadmin/docs/SIRGAS_CRD/{nombre_archivo.upper()}.XYZ"

    # Realizar la solicitud GET al servicio
    response = requests.get(url)

    # Verificar el estado de la respuesta
    if response.status_code != 200:
        return False

    # Decodificar el contenido de la respuesta
    contenido = response.text
    lineas = contenido.splitlines()

    # Obtener la última línea (la válida con coordenadas)
    ultima_linea = lineas[-2] if len(lineas) >= 2 else None

    # Si no hay línea válida, salir
    if not ultima_linea:
        return False

    # Construir ruta destino: ...\Red activa\GPS1\IGAC\CALI
    ruta_destino = os.path.join(ruta_por_antena, materializada, nombre_archivo)
    os.makedirs(ruta_destino, exist_ok=True)

    # Guardar contenido en archivo .txt
    nombre_txt = f"coordenada-antena-{nombre_archivo.upper()}.TXT"
    ruta_txt = os.path.join(ruta_destino, nombre_txt)

    with open(ruta_txt, 'w', encoding='utf-8') as f:
        f.write(contenido)

    return ultima_linea

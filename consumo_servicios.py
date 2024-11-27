from buscador_de_carpetas import buscar_y_crear_carpeta
from datetime import datetime
from tkinter import filedialog
from zipfile import ZipFile
import tkinter as tk
import requests
import config 
import json
import time
import os

antenasIgac = config.antenas_igac
ruta_descarga = config.ruta_descargas

#********************************************************************************************************************************
# Servicio para ver toda la red geodésica
def servicio_administrador_antenas():
    
    try:
        # Define el nombre del archivo basado en la fecha actual
        fecha_actual = datetime.now()
        mes_actual = fecha_actual.strftime("%B-%Y")
        nombre_archivo = f"antenas-{fecha_actual.strftime('%d-%B-%Y')}.json"

        # Verificar si ya existe un archivo JSON del mes actual
        archivos_json = [archivo for archivo in os.listdir() if archivo.startswith("antenas_") and archivo.endswith(".json")]
        for archivo in archivos_json:
            if mes_actual in archivo:  # Comprobar si el archivo pertenece al mes actual
                print(f"El archivo {archivo} ya existe y pertenece al mes actual. No se realiza la solicitud.")
                return None
        
        print("Iniciando solicitud al servicio...")

        intentos = 0
        max_intentos = 3
        datos = {}

        while intentos < max_intentos:
            try:
                # Realiza la solicitud GET al servicio
                respuesta = requests.get(antenasIgac, timeout=10)
                
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    estaciones = datos.get("estaciones", [])

                    if not estaciones:
                        print("Advertencia: No se encontraron datos válidos en el campo 'estaciones'.")
                        return None

                    # Procesamiento de los datos
                    datos_limpios = [
                        {
                            "ADMINISTRADOR": estacion["ADMINISTRADOR"],
                            "ESTADO": estacion["ESTADO"],
                            "TIPO_ESTACION": estacion["TIPO_ESTACION"],
                            "MATERIALIZADA": estacion["MATERIALIZADA"],
                            "ESTACION": estacion["CODIGO"]
                        }
                        for estacion in estaciones
                    ]

                    # Guarda los datos en un archivo JSON
                    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                        json.dump(datos_limpios, archivo, ensure_ascii=False, indent=4)

                    print(f"Datos guardados correctamente en {nombre_archivo}")
                    
                    # Eliminar otros archivos JSON con fechas diferentes al mes actual
                    for archivo in archivos_json:
                        if mes_actual not in archivo:  # Archivos fuera del mes actual
                            os.remove(archivo)
                            print(f"Archivo {archivo} eliminado.")

                    return datos_limpios
                
                else:
                    print(f"No hay respuesta por parte del servicio.")
                    break
            
            except requests.exceptions.RequestException as e:
                intentos += 1
                print(f"Error de conexión ({intentos}/{max_intentos}): {e}")
                time.sleep(2)  # Espera antes de intentar de nuevo

    except Exception as e:
        print(f"Error inesperado: {e}")

#********************************************************************************************************************************
# Servicio para poder ver los links de descarga de las antenas
def servicio_comprobar_rinex_por_fecha(fechaInicial, fechaFinal, estacion):
    # URL base de la solicitud
    url = "https://serviciosgeovisor.igac.gov.co:8080/Geovisor/geodesia"

    # Parámetros de la solicitud
    params = {
        "draw": 1,
        "columns[0][data]": "ID_RINEX",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "false",
        "columns[1][data]": "ID_RINEX",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[2][data]": "ID_RINEX",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "true",
        "order[0][column]": 1,
        "order[0][dir]": "desc",
        "start": 0,
        "length": 10,
        "search[value]": "",
        "search[regex]": "false",
        "cmd": "query",
        "estacion": estacion,
        "fechaInicial": fechaInicial,
        "fechaFinal": fechaFinal,
        "tipo": ""
    }

    try:
        # Realizar la solicitud GET con los parámetros
        response = requests.get(url, params=params)

        # Comprobar si la solicitud fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta en formato JSON
            datos = response.json()
            # Extraer los datos requeridos
            resultados = []
            for rinex in datos.get("rinex", []):
                resultado = {
                    "NOMBRE_ARCHIVO": rinex.get("NOMBRE_ARCHIVO"),
                    "ID_RINEX": rinex.get("ID_RINEX"),
                }
                resultados.append(resultado)
            return resultados
        else:
            print(f"Error en la solicitud: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None

#********************************************************************************************************************************
# servicio para capturar el token de descarga
def consumir_servicio_descarga(id_rinex, token):
    url = f"https://serviciosgeovisor.igac.gov.co:8080/Geovisor/descargas?cmd=request&tipo=rinex&id={id_rinex}&token={token}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo un error en la solicitud

        # Analizar la respuesta JSON y extraer el valor de 'token' si existe
        data = response.json()
        token_rinex = data.get('token', None)
        
        print('exito')
        
        return token_rinex
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)
        return None
    
#********************************************************************************************************************************
# Servicio para capturar el token de descarga y descargar el archivo
def descargar_archivo(token, subcarpeta, nombre_archivo,fecha, administrador, ruta_carpeta_inicial):
    #verifico si ya existe la ruta donde voy a guardar mis archivos
    if  not ruta_carpeta_inicial:
        ruta_carpeta_inicial = buscar_y_crear_carpeta(ruta_descarga, fecha)
        
    #nombre de la carpeta del administrador
    nombre_carpeta_red_geoscan = administrador            

    # Ruta de la carpeta del administrador de la antena
    ruta_redgeoscan = os.path.join(ruta_carpeta_inicial, nombre_carpeta_red_geoscan)
    ruta_carpeta = os.path.join(ruta_redgeoscan, subcarpeta)
    
    # Crear las carpetas si no existen
    os.makedirs(ruta_carpeta, exist_ok=True)
    
    # Ruta completa del archivo que se descargará dentro de la subcarpeta
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

    # Construcción de la URL del servicio de descarga con el token proporcionado
    url = f"https://serviciosgeovisor.igac.gov.co:8080/Geovisor/descargas?cmd=download&token={token}"
    
    # Encabezados para la solicitud
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    
    # Realizar la solicitud GET
    response = requests.get(url, headers=headers, stream=True)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Guardar el contenido en el archivo
        with open(ruta_archivo, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print("Archivo descargado exitosamente")
        return ruta_carpeta_inicial  # Retorna la ruta completa del archivo descargado
    else:
        print(f"Error en la descarga. Código de estado: {response.status_code}")
        return ruta_carpeta_inicial
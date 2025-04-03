# Importar modulos redgeoscan
from redgeoscan.modulos.servicios.obtener_token_rinex import obtener_token_con_el_id_rinex

# Importar modulos de monitor
from monitor.log.log import agregar_log
from config import config

# Ruta fija donde buscar el archivo
ruta_token_txt = config.ruta_token

# Importaciones adicionales
import os
import time


#************************************************************************************************
# Función para buscar y leer el archivo con el token principal en la carpeta `docs`
def buscar_y_leer_archivo_token(ruta_token):

    # Validar si la carpeta existe
    if not os.path.isdir(ruta_token):
        print(f'La carpeta {ruta_token} no existe.')
        return None

    # Buscar archivos que contengan el string 'token-principal' en su nombre
    token_txt = [archivo for archivo in os.listdir(ruta_token)
                 if "token-principal" in archivo and archivo.endswith('.txt')]
    
    # Validar si no se encuentra el archivo
    if not token_txt:
        print('No se encontró un archivo txt con el token.')
        return None

    # Seleccionamos el primer archivo encontrado
    token_txt_encontrado = token_txt[0]
    ruta_txt = os.path.join(ruta_token, token_txt_encontrado)


    # Leer el contenido del archivo si es válido
    try:
        with open(ruta_txt, "r", encoding="utf8") as archivo:
            contenido = archivo.read()
        return contenido
    except Exception as e:
        print("Error al leer el archivo:", e)
        return None
    
#********************************************************************************************************************************
# Función para actualizar el diccionario con la información de los RINEX de las antenas donde ORDEN es "0"
def actualizar_diccionario_con_el_token_rinex(diccionario):

    # Llamamos el token principal
    token_principal = buscar_y_leer_archivo_token(ruta_token_txt)
    
    try:
        
        # Validamos que tengamos el token
        if not token_principal:
            msj_depuracion = "FALLO EL TOKEN PRINCIPAL NO ESTA O YA CADUCO, NO ES POSIBLE EXTRAER EL TOKEN DE DESCARGA DE LOS RINEX!!!"
            return msj_depuracion, None
        
        agregar_log("Inicio actualización del diccionario con Token de descarga de archivos RINEX.")

        # Iterar sobre los días de rastreo en el diccionario
        for dia, info_dia in diccionario.get("dias_rastreos", {}).items():
            base_subcarpetas = info_dia.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})

            for gps_nombre, gps_info in base_subcarpetas.items():
                antenas_cercanas = gps_info.get("antenas_cercanas", [])

                for antena in antenas_cercanas:
                    # Ignorar antenas con ORDEN distinto de "0"
                    #if antena.get("ORDEN") != "0":
                     #   continue

                    rinex_archivos = antena.get("RINEX_ARCHIVOS", [])
                    for rinex in rinex_archivos:
                        id_rinex = rinex.get("ID_RINEX")
                        agregar_log(f"buscando token de Antena: {antena.get('NAME')}, archivo {rinex.get('NOMBRE_ARCHIVO')} con Id: {id_rinex}")
                        # Validar que exista el ID_RINEX
                        if not id_rinex:
                            agregar_log(f"No se encontró ID_RINEX para el archivo RINEX en la antena {antena.get('NAME')}.")
                            continue
                        
                        # Obtener el token para este ID_RINEX
                        try:
                            token_rinex = obtener_token_con_el_id_rinex(id_rinex, token_principal)
                            if token_rinex:
                                rinex["TOKEN_RINEX"] = token_rinex
                                agregar_log(f"Token asignado al archivo RINEX {rinex.get('NOMBRE_ARCHIVO')} de la antena {antena.get('NAME')}.")
                            else:
                                agregar_log(f"No se pudo obtener el token para el archivo RINEX {rinex.get('NOMBRE_ARCHIVO')} de la antena {antena.get('NAME')}.")
                        except Exception as e:
                            agregar_log(f"Error al obtener el token para el archivo RINEX {rinex.get('NOMBRE_ARCHIVO')} de la antena {antena.get('NAME')}: {e}")
                            rinex["TOKEN_RINEX"] = None

        agregar_log("Finalizada la actualización del diccionario con Token de descarga de archivos RINEX.")
        return None, diccionario

    except Exception as e:
        msj_depuracion = f"Error durante la actualización del diccionario con Tokens RINEX: {e}"
        return msj_depuracion,  None

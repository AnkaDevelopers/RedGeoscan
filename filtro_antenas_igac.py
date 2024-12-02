import os
import glob
import json

def filtro_antenas(antenas_kml):

    # Buscar el archivo JSON que comienza con 'antenas' en el mismo proyecto
    ruta_directorio = os.path.dirname(__file__)
    archivos_json = glob.glob(os.path.join(ruta_directorio, "antenas*.json"))

    if not archivos_json:
        print("No se encontró ningún archivo JSON que comience con 'antenas'.")
        return []  # Retornar una lista vacía en caso de error

    # Usar el primer archivo que coincida con el patrón
    ruta_json = archivos_json[0]

    # Cargar el archivo JSON
    with open(ruta_json, 'r', encoding='utf-8') as archivo_json:
        datos_json = json.load(archivo_json)

    antenas_filtradas = []  # Lista para almacenar antenas presentes en el archivo JSON

    # Iterar sobre cada antena en la lista
    for antena in antenas_kml:
        nombre_antena = antena.get("NAME", "")

        # Buscar si la antena está en el archivo JSON
        for registro in datos_json:
            if registro.get("ESTACION") == nombre_antena:
                antena_filtrada = {
                    "NAME": antena["NAME"],
                    "Latitud (Decimal)": antena["Latitud (Decimal)"],
                    "Longitud (Decimal)": antena["Longitud (Decimal)"],
                    "Distancia": antena["Distancia"],
                    "ADMINISTRADOR": registro.get("ADMINISTRADOR", "")
                }
                antenas_filtradas.append(antena_filtrada)
                break

        else:
            print(f"Antena {nombre_antena} no encontrada en el archivo JSON.")

    # Retornar la lista de antenas filtradas
    return antenas_filtradas


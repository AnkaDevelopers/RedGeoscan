import json
import os
import glob
import pandas as pd  # Importar pandas para manejar DataFrames

def filtro_antenas_igac(Antenas_kml):
    # Buscar el archivo JSON que comienza con 'antenas' en el mismo proyecto
    ruta_directorio = os.path.dirname(__file__)
    archivos_json = glob.glob(os.path.join(ruta_directorio, "antenas*.json"))

    if not archivos_json:
        print("No se encontró ningún archivo JSON que comience con 'antenas'.")
        return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error

    # Usar el primer archivo que coincida con el patrón
    ruta_json = archivos_json[0]

    # Cargar el archivo JSON
    with open(ruta_json, 'r') as archivo_json:
        datos_json = json.load(archivo_json)

    antenas_con_administrador = []  # Lista para almacenar antenas administradas por IGAC o IGAC-SGC

    # Iterar sobre cada antena en Antenas_kml
    for _, antena in Antenas_kml.iterrows():
        nombre_antena = antena['NAME']

        # Buscar si la antena está en el archivo JSON
        for registro in datos_json:
            if registro.get("ESTACION") == nombre_antena:
                # Verificar si el administrador es IGAC o IGAC-SGC
                administrador = registro.get("ADMINISTRADOR", "")
                antena_filtrada = {
                    "NAME": antena["NAME"],
                    "Latitud (Decimal)": antena["Latitud (Decimal)"],
                    "Longitud (Decimal)": antena["Longitud (Decimal)"],
                    "Distancia": antena["Distancia"],
                    "ADMINISTRADOR": administrador
                }
                
                antenas_con_administrador.append(antena_filtrada)
                break

        else:
            print(f"Antena {nombre_antena} no encontrada en el archivo JSON.")

    # Convertir la lista de antenas filtradas a un DataFrame
    df_antenas_con_administrador = pd.DataFrame(antenas_con_administrador)
    return df_antenas_con_administrador

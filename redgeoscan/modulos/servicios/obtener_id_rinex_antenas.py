# Importar modulos de monitor
#from modulos.log.log import agregar_log

# Importaciones adicionales
import requests
import time

#********************************************************************************************************************************
# Servicio para poder EXTRAER EL TOKEN DE DESCARGA DE LOS ARCHIVOS RINEX DE LAS ANTENAS
def servicio_comprobar_rinex_por_fecha(fecha, estacion):
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
        "estacion": estacion,  # ejemplo BACO
        "fechaInicial": fecha,  # formato fecha: 10-10-2024
        "fechaFinal": fecha,  # formato fecha: 10-10-2024
        "tipo": ""
    }

    try:
        # Realizar la solicitud GET con los parámetros
        response = requests.get(url, params=params)

        # Comprobar si la solicitud fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta en formato JSON
            datos = response.json()
            # Extraer todos los datos requeridos
            resultados = [
                {
                    "NOMBRE_ARCHIVO": rinex.get("NOMBRE_ARCHIVO"),
                    "ID_RINEX": rinex.get("ID_RINEX"),
                }
                for rinex in datos.get("rinex", [])
            ]
            return resultados
        else:
            print(f"Error en la solicitud: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None



# PRUEBA DEL SERVICIO
#servicio_comprobar_rinex_por_fecha("15-01-2025","PGTN")
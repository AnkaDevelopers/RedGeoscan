# Importar módulos de monitor
from monitor.log.log import agregar_log

import requests

def consumoServicioProyectos(api_url):
    # Definir el número máximo de intentos
    intentos_maximos = 3
    agregar_log(f"Intentando consumir el servicio en: {api_url}")

    for intento in range(intentos_maximos):
        agregar_log(f"Intento {intento + 1} de {intentos_maximos}")
        try:
            agregar_log("Realizando la solicitud GET...")
            response = requests.get(api_url, timeout=5)
            
            # Verificar si la respuesta es exitosa
            if response.status_code == 200:
                agregar_log("Respuesta exitosa (200 OK). Procesando datos...")
                return response.json()
            else:
                agregar_log(f"Respuesta no exitosa. Código de estado: {response.status_code}. Intentando nuevamente...")
                continue  

        except requests.ConnectionError:
            # Si no se puede conectar, mostrar mensaje de depuración
            agregar_log("Error de conexión. Intentando nuevamente...")
            continue  
        
        except Exception as e:
            # Capturar cualquier otro error y mostrarlo
            agregar_log(f"Error inesperado: {e}. Abortando la operación.")
            return None  
    
    # Si después de todos los intentos no funcionó
    agregar_log("No se pudo completar la solicitud después de varios intentos. Abortando.")
    return None

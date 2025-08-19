# consumoServicioProyectos.py
import requests

def consumoServicioProyectos(api_url):
    
    intentos_maximos = 3

    for intento in range(intentos_maximos):
        try:
            response = requests.get(api_url, timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                # Si la respuesta no es 200, vuelve a intentar
                continue  

        except requests.ConnectionError:
            # Si no se puede conectar, vuelve a intentar
            continue  
        
        except Exception:
            # Error inesperado
            return None  
    # Si después de todos los intentos no funcionó
    return None  

import pyautogui
import time
from monitor.log.log import agregar_log  

def esperar_carga_interfaz(imagen_referencia):
    agregar_log('🔎 Inicio del proceso de espera para la carga de la interfaz...')

    
    timeout = 60  # Tiempo máximo de espera en segundos
    intervalo = 2  # Tiempo entre cada intento de búsqueda

    tiempo_inicio = time.time()
    intentos = 0

    while True:
        intentos += 1

        # Intentar localizar la imagen en la pantalla con manejo de errores
        try:
            ubicacion = pyautogui.locateOnScreen(imagen_referencia, confidence=0.7)
        except pyautogui.ImageNotFoundException:
            ubicacion = None
        except Exception as e:
            agregar_log(f"❌ Error inesperado al buscar imagen en pantalla: {e}")
            return None

        if ubicacion:
            tiempo_transcurrido = time.time() - tiempo_inicio
            agregar_log(f"✅ Imagen detectada tras {tiempo_transcurrido:.2f} segundos ({intentos} intentos).")
            return True

        tiempo_transcurrido = time.time() - tiempo_inicio
        if tiempo_transcurrido > timeout:
            agregar_log(f"⏰ Tiempo agotado: {tiempo_transcurrido:.2f} segundos sin detectar la imagen ({intentos} intentos).")
            return None

        time.sleep(intervalo)

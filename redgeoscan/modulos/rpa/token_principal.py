import os
import sys
import ctypes

# 🔐 Verificar y elevar permisos si es necesario
def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not es_admin():
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    sys.exit()

# ------------------------------------------------------------------------------------------------
# Importar modulos de monitor
from config import config
from monitor.log.log import agregar_log

# Importaciones adicionales
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from seleniumwire import webdriver
import threading
import logging
import json
import time

# Variables
ruta = config.ruta_gov
ruta_perfil = config.ruta_perfil
nombre_perfil = config.nombre_perfil
webdriver_path = config.webdriver_path
target_url = config.target_url

# Variable global para almacenar el idToken
ID_TOKEN = None

# Función para cerrar todas las instancias de Edge y su driver
def cerrar_edge():
    try:
        os.system("taskkill /IM msedge.exe /F")
        os.system("taskkill /IM msedgedriver.exe /F")
        agregar_log("Se cerraron todas las instancias de Microsoft Edge y EdgeDriver.")
    except Exception as e:
        agregar_log(f"Error al cerrar Microsoft Edge: {e}")

def rpa_igac():
    global ID_TOKEN

    try:
        # Redirigir stderr para evitar mensajes de error en la consola
        sys.stderr = open(os.devnull, 'w')

        cerrar_edge()
        time.sleep(1)

        options = Options()
        options.add_argument(f"user-data-dir={ruta_perfil}")
        options.add_argument(f"profile-directory={nombre_perfil}")
        options.add_argument("--headless=new")

        # Eliminar archivo DevToolsActivePort si quedó colgado
        devtools_file = os.path.join(ruta_perfil, "DevToolsActivePort")
        try:
            if os.path.exists(devtools_file):
                os.remove(devtools_file)
                agregar_log("Archivo DevToolsActivePort eliminado manualmente.")
        except Exception as e:
            agregar_log(f"Error al eliminar DevToolsActivePort: {e}")

        # Deshabilitar HTTP/2 en Selenium Wire
        seleniumwire_options = {'disable_http2': True}

        # Crear instancia del navegador
        os.environ["PATH"] += os.pathsep + os.path.dirname(webdriver_path)
        driver = webdriver.Edge(options=options, seleniumwire_options=seleniumwire_options)

        agregar_log("Iniciando el navegador y abriendo la página.")
        driver.get(ruta)

        try:
            WebDriverWait(driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
            agregar_log("La página ha cargado completamente.")
        except Exception as e:
            agregar_log(f"Error al esperar que la página cargue completamente: {e}")

        driver.refresh()
        agregar_log("Página recargada.")
        time.sleep(5)

        # Capturar solicitudes
        for request in driver.requests:
            if request.url.startswith(target_url) and request.method == 'POST':
                try:
                    if request.body:
                        body_data = request.body.decode('utf-8')
                        json_data = json.loads(body_data)
                        if "idToken" in json_data:
                            ID_TOKEN = json_data["idToken"]
                            agregar_log("idToken capturado correctamente.")
                            driver.quit()
                            sys.stderr.close()  # Restaurar stderr antes de salir
                            sys.stderr = sys.__stderr__
                            return None, ID_TOKEN
                        else:
                            msj_depuracion = "No se encontró el idToken en la solicitud."
                            driver.quit()
                            sys.stderr.close()
                            sys.stderr = sys.__stderr__
                            return msj_depuracion, None
                except Exception as e:
                    msj_depuracion = f"Error al procesar el cuerpo de la solicitud getAccountInfo: {e}"
                    driver.quit()
                    sys.stderr.close()
                    sys.stderr = sys.__stderr__
                    return msj_depuracion, None
                break
        else:
            msj_depuracion = "No se encontró la solicitud `getAccountInfo` después de recargar la página."
            driver.quit()
            sys.stderr.close()
            sys.stderr = sys.__stderr__
            return msj_depuracion, None

        agregar_log("El navegador se cerró correctamente.")

    except Exception as e:
        msj_depuracion = f"Error general en rpa_igac: {e}"
        if 'driver' in locals():
            driver.quit()
        sys.stderr.close()
        sys.stderr = sys.__stderr__
        return msj_depuracion, None

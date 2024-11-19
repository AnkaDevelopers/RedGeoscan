from seleniumwire import webdriver  # Usamos selenium-wire para interceptar solicitudes
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import json
import os
import time

# Variable global para almacenar el idToken
ID_TOKEN = None

# Ruta de la página
ruta = '''https://www.colombiaenmapas.gov.co/?e=-74.19790397936877,4.606824129536961,
-74.05594002062873,4.715639657991442,4686&b=igac&u=0&t=25&servicio=8#'''

# Verifica la ruta del perfil de usuario
ruta_perfil = "C:/Users/camil-code/AppData/Local/Microsoft/Edge/User Data"
nombre_perfil = "Default"
webdriver_path = "C:/webdriver/msedgedriver.exe"
target_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo"

# Función para cerrar todas las instancias de Edge
def cerrar_edge():
    try:
        os.system("taskkill /IM msedge.exe /F")
    except Exception:
        pass

def rpa_igac():
    global ID_TOKEN
    cerrar_edge()
    time.sleep(1)
    service = Service(webdriver_path)

    options = Options()
    options.add_argument(f"user-data-dir={ruta_perfil}")
    options.add_argument(f"profile-directory={nombre_perfil}")
    options.add_argument("--headless")  # Ejecuta el navegador en modo "headless"

    seleniumwire_options = {
        'disable_http2': True  # Deshabilitar HTTP/2
    }

    # Crear instancia de Edge con las opciones de Selenium Wire
    driver = webdriver.Edge(service=service, options=options, seleniumwire_options=seleniumwire_options)

    # Abre la página
    driver.get(ruta)

    try:
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("La página ha cargado completamente.")
    except Exception as e:
        print(f"Error al esperar que la página cargue completamente: {e}")

    driver.refresh()
    print("Página recargada.")

    time.sleep(1)

    # Captura la solicitud `getAccountInfo`
    for request in driver.requests:
        if request.url.startswith(target_url) and request.method == 'POST':
            try:
                if request.body:
                    body_data = request.body.decode('utf-8')
                    json_data = json.loads(body_data)
                    if "idToken" in json_data:
                        ID_TOKEN = json_data["idToken"]
                        print("idToken capturado", ID_TOKEN)
                        driver.quit()
                        return ID_TOKEN
                    else:
                        print("idToken no encontrado en el cuerpo de la solicitud.")
            except Exception as e:
                print(f"Error al procesar el cuerpo de la solicitud getAccountInfo: {e}")
            break
    else:
        print("No se encontró la solicitud `getAccountInfo` después de recargar la página.")
    driver.quit()


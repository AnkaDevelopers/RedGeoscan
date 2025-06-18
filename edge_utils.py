import os
import re
import zipfile
import shutil
import subprocess
import requests

DESTINO_DRIVER = r"C:\Webdriver"
DRIVER_PATH = os.path.join(DESTINO_DRIVER, "msedgedriver.exe")

def obtener_version_edge():
    try:
        output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version',
            shell=True
        ).decode("utf-8")
        match = re.search(r"version\s+REG_SZ\s+([0-9.]+)", output)
        if match:
            return match.group(1)
    except:
        return None

def obtener_version_driver():
    try:
        output = subprocess.check_output(f'"{DRIVER_PATH}" --version', shell=True).decode("utf-8")
        match = re.search(r"Microsoft Edge WebDriver (\d+\.\d+\.\d+)", output)

        if match:
            return match.group(1)
    except:
        return None

def construir_url_driver(version_edge):
    version_base = ".".join(version_edge.split(".")[:3])

    # Intento 1: LATEST_RELEASE_{version}
    try:
        r = requests.get(f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{version_base}")
        if r.status_code == 200:
            latest_version = r.text.strip()
            return f"https://msedgedriver.azureedge.net/{latest_version}/edgedriver_win64.zip"
    except:
        pass

    # Intento 2: LATEST_RELEASE (última versión general)
    try:
        r = requests.get("https://msedgedriver.azureedge.net/LATEST_RELEASE")
        if r.status_code == 200:
            latest_version = r.text.strip()
            return f"https://msedgedriver.azureedge.net/{latest_version}/edgedriver_win64.zip"
    except:
        pass

    # Intento 3: construir la URL directamente con la versión de Edge instalada
    try:
        fallback_url = f"https://msedgedriver.microsoft.com/{version_edge}/edgedriver_win64.zip"
        test = requests.head(fallback_url)
        if test.status_code == 200:
            return fallback_url
    except:
        pass

    raise Exception("No se pudo obtener ninguna versión compatible desde los endpoints de Microsoft.")

def descargar_y_extraer_driver(url, destino):
    zip_path = os.path.join(destino, "edgedriver.zip")
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise Exception("No se pudo descargar el EdgeDriver.")
    with open(zip_path, "wb") as f:
        f.write(r.content)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destino)
    os.remove(zip_path)

def verificar_y_actualizar_edgedriver(agregar_log=None):
    version_edge = obtener_version_edge()
    version_driver = obtener_version_driver()

    if version_edge is None:
        if agregar_log: agregar_log("No se pudo detectar la versión de Microsoft Edge.")
        return False

    version_edge_base = ".".join(version_edge.split(".")[:3])
    version_driver_base = version_driver if version_driver else "No detectado"

    if version_edge_base == version_driver_base:
        if agregar_log: agregar_log(f"EdgeDriver se encuentra actualizado en la (versión {version_driver_base}).")
        return True

    if agregar_log: 
        agregar_log(f"Versión de Edge: {version_edge_base} | EdgeDriver: {version_driver_base}")
        agregar_log("EdgeDriver desactualizado. Iniciando actualización...")

    try:
        url = construir_url_driver(version_edge)
        descargar_y_extraer_driver(url, DESTINO_DRIVER)
        if agregar_log: agregar_log("EdgeDriver actualizado correctamente.")
        return True
    except Exception as e:
        if agregar_log: agregar_log(f"Error actualizando EdgeDriver: {e}")
        return False


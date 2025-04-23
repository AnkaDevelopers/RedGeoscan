# Importar modulos de monitor
from config import config
from monitor.log.log import agregar_log

# Importaciones adicionales
import subprocess
import pyautogui
import time
import ctypes
import os
from PIL import ImageGrab
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Variables globales
ruta_directorio = config.ruta_rtk
nombre_ejecutable = config.nombre_exe

# Ruta completa del ejecutable
ruta_ejecutable = os.path.join(ruta_directorio, nombre_ejecutable)

#*****************************************************************************************************
# Función auxiliar para esperar hasta que RTKLIB muestre "done"
def esperar_done(timeout=160):
    inicio = time.time()
    while time.time() - inicio < timeout:
        img = ImageGrab.grab()
        texto = pytesseract.image_to_string(img).lower()
        if "done" in texto:
            agregar_log("RTKLIB ha terminado el proceso (detected 'done').")
            return True
        time.sleep(2)
    agregar_log("Tiempo agotado esperando 'done' en RTKLIB.")
    return False

#*****************************************************************************************************
# Función para ejecutar el RTKLIB para todas las carpetas GPS
def ejecutar_rtk_para_gps(diccionario_proyecto):
    try:
        # Verificar si el ejecutable existe
        if not os.path.exists(ruta_ejecutable):
            raise FileNotFoundError(f"El archivo {ruta_ejecutable} no existe.")

        # 🔍 Verificar si ya están todos los archivos .pos antes de abrir RTKLIB
        faltan_pos = False
        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            base = info.get("subcarpetas", {}).get("Base", {})
            gps_subcarpetas = base.get("sub_carpetas", {})

            for gps_nombre, gps_info in gps_subcarpetas.items():
                archivos = gps_info.get("archivos", {})
                ruta_pos = archivos.get("pos")
                if not ruta_pos:
                    faltan_pos = True
                    break
            if faltan_pos:
                break

        if not faltan_pos:
            agregar_log("Todos los archivos .pos ya existen. No se requiere ejecutar RTKLIB.")
            return None, True

        # 🧠 Verificar y desactivar Bloq Mayús si está activo
        if ctypes.WinDLL("User32.dll").GetKeyState(0x14):
            agregar_log("Bloq Mayús estaba activado. Desactivando...")
            pyautogui.press('capslock')
            time.sleep(0.5)

        # Ejecutar el programa RTKLIB una vez
        agregar_log("Iniciando RTKLIB...")
        proceso_rtk = subprocess.Popen(ruta_ejecutable)
        agregar_log(f"El archivo {nombre_ejecutable} se ha ejecutado correctamente.")
        
        time.sleep(5)

        iteracion = 0
        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            for gps_nombre, gps_info in info["subcarpetas"]["Base"]["sub_carpetas"].items():
                agregar_log(f"Procesando carpeta {gps_nombre} en día {dia}...")

                archivos = gps_info.get("archivos", {})
                ruta_pos = archivos.get("pos")
                if ruta_pos:
                    agregar_log(f"Saltando {gps_nombre} en {dia} porque ya tiene un archivo .pos.")
                    continue

                ruta_obs = archivos.get("25o") or archivos.get("obs") or archivos.get("OBS") or archivos.get("24o") or archivos.get("26o") or archivos.get("27o")
                ruta_nav = archivos.get("25n") or archivos.get("nav") or archivos.get("NAV") or archivos.get("24n") or archivos.get("26n") or archivos.get("27n")

                if not ruta_obs:
                    agregar_log(f"Error: No se encontró archivos .o o .obs para {gps_nombre} en {dia}.")
                    continue
                if not ruta_nav:
                    agregar_log(f"Error: No se encontró un archivo .n para {gps_nombre} en {dia}.")
                    continue

                ruta_gps = gps_info["ruta"]

                agregar_log(f"Rutas utilizadas para {gps_nombre}:")
                agregar_log(f"  - OBS: {ruta_obs}")
                agregar_log(f"  - NAV: {ruta_nav}")
                agregar_log(f"  - GPS carpeta: {ruta_gps}")

                rutas_rtkilb = {
                    "ruta_obs": ruta_obs,
                    "ruta_nav": ruta_nav,
                    "carpeta_gps": ruta_gps
                }

                if iteracion > 0:
                    pyautogui.press('tab')
                    time.sleep(0.2)

                pyautogui.press('tab')
                time.sleep(0.2)

                pyautogui.press('tab')
                time.sleep(0.2)

                pyautogui.press('tab')
                time.sleep(0.2)

                pyautogui.write(rutas_rtkilb['ruta_obs'])
                time.sleep(0.2)

                pyautogui.press('tab')
                time.sleep(0.2)

                pyautogui.press('tab')
                time.sleep(0.2)

                pyautogui.write(rutas_rtkilb['ruta_nav'])
                time.sleep(0.1)

                for i in range(0, 9):
                    pyautogui.press('tab')
                    time.sleep(0.2)

                pyautogui.write(rutas_rtkilb['carpeta_gps'])
                
                pyautogui.press('tab', presses=8, interval=0.2)
                time.sleep(0.2)
                
                pyautogui.press('enter')
                time.sleep(1)

                iteracion += 1

                time.sleep(20)
                # Esperar a que el proceso de RTKLIB diga "done"
                esperar_done(timeout=180)
        
        agregar_log('nueva carpeta días rastreos')
        time.sleep(0)   

        agregar_log("Procesamiento completado para todas las carpetas GPS.")
        proceso_rtk.terminate()
        agregar_log("RTKLIB ha sido cerrado.")
        return None, True

    except FileNotFoundError as e:
        msj_depuracion = f"Error: {e}"
        return msj_depuracion, False
    except subprocess.CalledProcessError:
        msj_depuracion = f"Error al ejecutar {nombre_ejecutable}. Verifica los permisos o parámetros."
        return msj_depuracion, False
    except Exception as e:
        msj_depuracion = f"Se produjo un error al intentar ejecutar el archivo: {e}"
        return msj_depuracion, False
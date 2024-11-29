import config
import subprocess
import pyautogui
import time
import os

# Variables globales
ruta_directorio = config.ruta_rtk
nombre_ejecutable = config.nombre_exe

# Ruta completa del ejecutable
ruta_ejecutable = os.path.join(ruta_directorio, nombre_ejecutable)

#*****************************************************************************************************
# Función para ejecutar el RTKLIB para todas las carpetas GPS
def ejecutar_rtk_para_gps(diccionario_proyecto):
    """
    Inicia el programa RTKLIB y procesa las carpetas GPS en el diccionario.
    :param diccionario_proyecto: Diccionario con rutas y datos de las carpetas GPS.
    """
    try:
        # Verificar si el ejecutable existe
        if not os.path.exists(ruta_ejecutable):
            raise FileNotFoundError(f"El archivo {ruta_ejecutable} no existe.")

        # Ejecutar el programa RTKLIB una vez
        print("Iniciando RTKLIB...")
        proceso_rtk = subprocess.Popen(ruta_ejecutable)
        print(f"El archivo {nombre_ejecutable} se ha ejecutado correctamente.")
        
        # Esperar un tiempo para asegurarse de que la ventana del programa esté activa
        time.sleep(5)

        # Iterar sobre los días de rastreo
        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            for gps_nombre, rutas in info["subcarpetas_base"].items():
                print(f"Procesando carpeta {gps_nombre} en día {dia}...")

                # Verificar si ya existe un archivo .pos en esta carpeta
                if rutas["pos"] != 0:
                    print(f"Saltando {gps_nombre} en {dia} porque ya tiene un archivo .pos.")
                    continue

                # Validar que las rutas necesarias existen
                ruta_obs = rutas["obs"] if rutas["obs"] != 0 else rutas["24o"]
                ruta_nav = rutas["24n"]

                # Validar las rutas antes de usarlas
                if not ruta_obs or ruta_obs == 0:
                    print(f"Error: No se encontró un archivo .obs o .24o para {gps_nombre} en {dia}.")
                    continue
                if not ruta_nav or ruta_nav == 0:
                    print(f"Error: No se encontró un archivo .24n para {gps_nombre} en {dia}.")
                    continue

                # Mensajes de depuración
                print(f"Rutas utilizadas para {gps_nombre}:")
                print(f"  - OBS: {ruta_obs}")
                print(f"  - NAV: {ruta_nav}")

                rutas_rtkilb = {
                    "ruta_obs": ruta_obs,
                    "ruta_nav": ruta_nav,
                    "carpeta_gps": rutas.get(gps_nombre, "")
                }

                # Simular la interacción con la interfaz gráfica usando PyAutoGUI
                print(f"Llenando datos para {gps_nombre} en {dia}...")
                pyautogui.press('tab')                  
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.write(rutas_rtkilb['ruta_obs'])
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.write(rutas_rtkilb['ruta_nav'])
                for i in range(0, 9):
                    pyautogui.press('tab')
                pyautogui.write(rutas_rtkilb['carpeta_gps'])
                for i in range(0, 8):
                    pyautogui.press('tab')
                pyautogui.press('enter')  
                
                # Esperar a que termine el proceso de RTKLIB para esta carpeta
                time.sleep(50)

        print("Procesamiento completado para todas las carpetas GPS.")

        # Opcional: Finalizar el proceso del programa RTKLIB si es necesario
        proceso_rtk.terminate()
        print("RTKLIB ha sido cerrado.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError:
        print(f"Error al ejecutar {nombre_ejecutable}. Verifica los permisos o parámetros.")
    except Exception as e:
        print(f"Se produjo un error al intentar ejecutar el archivo: {e}")

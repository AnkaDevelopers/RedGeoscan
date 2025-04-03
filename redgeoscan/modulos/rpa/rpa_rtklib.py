# Importar modulos de monitor
from config import config
from monitor.log.log import agregar_log

# Importaciones adicionales
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
    try:
        # Verificar si el ejecutable existe
        if not os.path.exists(ruta_ejecutable):
            raise FileNotFoundError(f"El archivo {ruta_ejecutable} no existe.")

        # Ejecutar el programa RTKLIB una vez
        agregar_log("Iniciando RTKLIB...")
        proceso_rtk = subprocess.Popen(ruta_ejecutable)
        agregar_log(f"El archivo {nombre_ejecutable} se ha ejecutado correctamente.")
        
        # Esperar un tiempo para asegurarse de que la ventana del programa esté activa
        time.sleep(2)

        iteracion = 0  # Contador de iteraciones para manejar el tab adicional
        # Iterar sobre los días de rastreo
        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            
            for gps_nombre, gps_info in info["subcarpetas"]["Base"]["sub_carpetas"].items():
                agregar_log(f"Procesando carpeta {gps_nombre} en día {dia}...")

                # Validar si ya existe un archivo .pos en esta carpeta
                archivos = gps_info.get("archivos", {})
                ruta_pos = archivos.get("pos")
                if ruta_pos:
                    agregar_log(f"Saltando {gps_nombre} en {dia} porque ya tiene un archivo .pos.")
                    continue

                # Validar que las rutas necesarias existen
                ruta_obs = archivos.get("25o") or archivos.get("obs") or archivos.get("24o")
                ruta_nav = archivos.get("25n") or archivos.get("nav") or archivos.get("24n")

                # Validar las rutas antes de usarlas
                if not ruta_obs:
                    agregar_log(f"Error: No se encontró archivos .o o .obs para {gps_nombre} en {dia}.")
                    continue
                if not ruta_nav:
                    agregar_log(f"Error: No se encontró un archivo .n para {gps_nombre} en {dia}.")
                    continue

                # Construir la ruta completa para la carpeta GPS
                ruta_gps = gps_info["ruta"]

                agregar_log(f"Rutas utilizadas para {gps_nombre}:")
                agregar_log(f"  - OBS: {ruta_obs}")
                agregar_log(f"  - NAV: {ruta_nav}")
                agregar_log(f"  - GPS carpeta: {ruta_gps}")

                rutas_rtkilb = {
                    "ruta_obs": ruta_obs,
                    "ruta_nav": ruta_nav,
                    "carpeta_gps": ruta_gps  # Aquí está la ruta GPS completa
                }

                # Agregar tab extra después de la primera iteración
                if iteracion > 0:
                    #agregar_log('Tab extra para iteraciones adicionales...')
                    pyautogui.press('tab')
                    time.sleep(0)

                # Simular la interacción con la interfaz gráfica
                #agregar_log('Tab1')  
                pyautogui.press('tab')
                time.sleep(0)

                #agregar_log('Tab2')
                pyautogui.press('tab')
                time.sleep(0)

                #agregar_log('Tab3')
                pyautogui.press('tab')
                time.sleep(0)

                #agregar_log('Escribir ruta_obs')
                pyautogui.write(rutas_rtkilb['ruta_obs'])
                time.sleep(0)

                #agregar_log('Tab4')
                pyautogui.press('tab')
                time.sleep(0)

                #agregar_log('Tab5')
                pyautogui.press('tab')
                time.sleep(0)

                #agregar_log('Escribir ruta_nav')
                pyautogui.write(rutas_rtkilb['ruta_nav'])
                time.sleep(0)

                for i in range(0, 9):
                    #agregar_log(f'Tab {i}')
                    pyautogui.press('tab')
                    time.sleep(0)

                #agregar_log('Escribir ruta gps')
                print(rutas_rtkilb)
                #pyautogui.write(rutas_rtkilb['carpeta_gps'])
                time.sleep(10)

                for i in range(0, 6):
                    #agregar_log(f'Tab {i}')
                    pyautogui.press('tab')
                    time.sleep(0)

                #agregar_log('Presionar enter')
                pyautogui.press('enter')
                time.sleep(0)

                # Incrementar contador de iteraciones
                iteracion += 1

                # Esperar a que termine el proceso de RTKLIB para esta carpeta
                time.sleep(120)
        
        agregar_log('nueva carpeta días rastreos')
        time.sleep(0)     

        agregar_log("Procesamiento completado para todas las carpetas GPS.")

        # Opcional: Finalizar el proceso del programa RTKLIB si es necesario
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
        msj_depuracion =f"Se produjo un error al intentar ejecutar el archivo: {e}"
        return msj_depuracion, False

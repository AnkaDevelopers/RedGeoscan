import subprocess
import pyautogui
import config
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
        print("Iniciando RTKLIB...")
        proceso_rtk = subprocess.Popen(ruta_ejecutable)
        print(f"El archivo {nombre_ejecutable} se ha ejecutado correctamente.")
        
        # Esperar un tiempo para asegurarse de que la ventana del programa esté activa
        time.sleep(1)

        # Iterar sobre los días de rastreo
        for dia, info in diccionario_proyecto["dias_rastreos"].items():
            
            iteracion = 0  # Contador de iteraciones para manejar el tab adicional
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

                # Construir la ruta completa para la carpeta GPS
                ruta_gps = os.path.join(
                    diccionario_proyecto["ruta_proyecto"], 
                    f"1.Procesamiento/1.Topografia/Rastreos/{dia}/Base/{gps_nombre}"
                )

                print(f"Rutas utilizadas para {gps_nombre}:")
                print(f"  - OBS: {ruta_obs}")
                print(f"  - NAV: {ruta_nav}")
                print(f"  - GPS carpeta: {ruta_gps}")

                rutas_rtkilb = {
                    "ruta_obs": ruta_obs,
                    "ruta_nav": ruta_nav,
                    "carpeta_gps": ruta_gps  # Aquí está la ruta GPS completa
                }
            
                # Agregar tab extra después de la primera iteración
                if iteracion > 0:
                    print('tab extra para iteraciones adicionales...')
                    pyautogui.press('tab')
                    time.sleep(0)

                # Simular la interacción con la interfaz gráfica
                print('tab1')  
                pyautogui.press('tab')
                time.sleep(0)

                print('tab2')
                pyautogui.press('tab')
                time.sleep(0)

                print('tab3')
                pyautogui.press('tab')
                time.sleep(0)

                print('escribir ruta_obs')
                pyautogui.write(rutas_rtkilb['ruta_obs'])
                time.sleep(0)

                print('tab4')
                pyautogui.press('tab')
                time.sleep(0)

                print('tab5')
                pyautogui.press('tab')
                time.sleep(0)

                print('escribir ruta_nav')
                pyautogui.write(rutas_rtkilb['ruta_nav'])
                time.sleep(0)

                for i in range(0, 9):
                    print(f'tab {i}')
                    pyautogui.press('tab')
                    time.sleep(0)

                print('escribir ruta gps')
                pyautogui.write(rutas_rtkilb['carpeta_gps'])
                time.sleep(0)

                for i in range(0, 8):
                    print(f'tab {i}')
                    pyautogui.press('tab')
                    time.sleep(0)

                print('presionar enter')
                pyautogui.press('enter')
                time.sleep(0)

                # Incrementar contador de iteraciones
                iteracion += 1

                # Esperar a que termine el proceso de RTKLIB para esta carpeta
                time.sleep(35)
        
            print('tab nueva carpeta dias rastreos')
            pyautogui.press('tab')
            time.sleep(0)     

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
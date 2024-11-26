import subprocess
import config
import pyautogui
import time
import os

# Variable globales
ruta_directorio = config.ruta_rtk
nombre_ejecutable = config.nombre_exe

# Ruta completa del ejecutable
ruta_ejecutable = os.path.join(ruta_directorio, nombre_ejecutable)

#*****************************************************************************************************
# Función para ejecutar el RTKLIB
def ejecutar_rtk(rutas_rtkilb):
    ejecucion = False
    try:
        # Comprueba si el archivo existe
        if not os.path.exists(ruta_ejecutable):
            raise FileNotFoundError(f"El archivo {ruta_ejecutable} no existe.")

        # Abre el ejecutable
        subprocess.Popen(ruta_ejecutable)
        print(f"El archivo {nombre_ejecutable} se ha ejecutado correctamente.")

        # Espera un tiempo para asegurarte de que la ventana del programa esté activa
        time.sleep(2)  # Ajusta este tiempo según la carga del programa

        # Simula la pulsación de la tecla Tab
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
        
        time.sleep(35)
           
        for i in range(0, 24):
            pyautogui.press('tab')
        pyautogui.press('enter')  
        
        time.sleep(3)
        print('*'*100,'\n','el programa se cerro')
        ejecucion = True
        return ejecucion
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError:
        print(f"Error al ejecutar {nombre_ejecutable}. Verifica los permisos o parámetros.")
    except Exception as e:
        print(f"Se produjo un error al intentar ejecutar el archivo: {e}")
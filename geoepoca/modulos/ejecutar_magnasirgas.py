# Importar módulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import psutil
import subprocess
import os
import tkinter as tk
from tkinter import messagebox

# *********************************************************************************
def ejecutar_magna_sirgas():
    java_path = r"c:\Program Files\Java\jre1.8.0_421\bin\java.exe"

    try:
        resultado = subprocess.run([java_path, "-version"], capture_output=True, text=True)
        if resultado.returncode != 0:
            agregar_log("❌ Java no se ejecutó correctamente. Mostrando advertencia.")
            mostrar_error_java()
            return False

        subprocess.Popen(
            [java_path, "-jar", "MagnaSirgas5.jar"],
            cwd=r"C:\bot-auto\geoepoca\MagnaSirgas5.1",
            shell=True
        )
        agregar_log("✅ MagnaSirgas ejecutado correctamente.")
        return True

    except FileNotFoundError:
        agregar_log("❌ Java no encontrado en la ruta especificada. Mostrando advertencia.")
        mostrar_error_java()
        return False
    except Exception as e:
        agregar_log(f"❌ Error al ejecutar MagnaSirgas: {e}")
        return False

# *********************************************************************************
def mostrar_error_java():
    """
    Muestra un messagebox indicando que Java no está disponible.
    """
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    messagebox.showerror(
        "Java requerido no encontrado",
        "No se pudo ejecutar MagnaSirgas.\n\nSe requiere Java 1.8.0_421 específicamente.\nAsegúrese de que esté instalado en:\nc:\\Program Files\\Java"
    )
    root.destroy()

# **********************************************************************************
def cerrar_magna_sirgas():
    """
    Cierra el proceso que ejecuta MagnaSirgas5.jar si está en ejecución.
    Retorna True si lo encuentra y cierra, False si no estaba corriendo.
    """
    cerrados = 0

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if (
                proc.info['name'] and 'java' in proc.info['name'].lower()
                and proc.info['cmdline']
                and any('MagnaSirgas5.jar' in arg for arg in proc.info['cmdline'])
            ):
                proc.terminate()
                cerrados += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if cerrados > 0:
        agregar_log(f"✅ Procesos MagnaSirgas cerrados: {cerrados}")
        return True
    else:
        agregar_log("ℹ️ No se encontró ningún proceso MagnaSirgas en ejecución.")
        return False

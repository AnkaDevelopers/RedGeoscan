# Importaciones de módulos
from geoepoca.modulos.ejecutar_magnasirgas import ejecutar_magna_sirgas, cerrar_magna_sirgas
from geoepoca.modulos.espera_carga_interfaz import esperar_carga_interfaz
from geoepoca.modulos.rpa_conver_epoc import converir_epoc
from geoepoca.modulos.rpa_conver_elip_decimales import conver_elip_decimales
from geoepoca.modulos.rpa_conver_ctm_12 import conver_ctm12
from geoepoca.modulos.rpa_ondulacion_geoidal import ondulacion_geoidal
from geoepoca.modulos.rpa_velocidades import calculo_velocidades

# Importar módulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
from PIL import Image, ImageTk
import tkinter as tk
import threading
import time
import sys
import os

def rpa_magnasirgas():
    ventana = tk.Tk()
    ventana.attributes('-fullscreen', True)
    ventana.configure(background='black')

    ruta_imagen = r"C:\RedGeoscan\geoepoca\Anka.png"
    if not os.path.isfile(ruta_imagen):
        agregar_log(f"❌ Imagen Anka.png no encontrada en {ruta_imagen}.")
        ventana.destroy()
        return None

    try:
        imagen = Image.open(ruta_imagen)
        ancho, alto = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
        imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen)
        label = tk.Label(ventana, image=imagen_tk)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # ✅ Previene que se borre la imagen de memoria
        label.image = imagen_tk
        ventana.label = label

        ventana.update()
    except Exception as e:
        agregar_log(f"❌ Error al cargar la imagen de fondo: {e}")
        ventana.destroy()
        return None
    time.sleep(3)
    agregar_log("▶️ Iniciando MagnaSirgas...")
    if not ejecutar_magna_sirgas():
        agregar_log("❌ Error al ejecutar MagnaSirgas.")
        ventana.destroy()
        return None

    def ejecutar_proceso():
        imagen_ref = r"C:\RedGeoscan\geoepoca\Imagenes\CargaInterfaz.png"
        time.sleep(5)
        if not esperar_carga_interfaz(imagen_ref):
            agregar_log("❌ No se detectó la interfaz de MagnaSirgas.")
            cerrar_magna_sirgas()
            ventana.destroy()
            return None

        pasos = [
            (converir_epoc, "conversión de época (año - 2018)"),
            (conver_elip_decimales, "conversión a coordenadas elipsoidales"),
            (conver_ctm12, "conversión a coordenadas origen nacional"),
            (ondulacion_geoidal, "cálculo de ondulación geoidal"),
            (calculo_velocidades, "cálculo de velocidades"),
        ]

        for func, desc in pasos:
            res, msj = func()
            if not res:
                agregar_log(f"❌ Error en {desc}: {msj}")
                cerrar_magna_sirgas()
                ventana.destroy()
                return None

            agregar_log(f"✅ {msj}")

        agregar_log("🎉 Todos los cálculos se completaron correctamente.")
        cerrar_magna_sirgas()
        ventana.destroy()

    ventana.after(1000, ejecutar_proceso)
    ventana.mainloop()

    return True

from tkinter import filedialog
from buscador_de_carpetas import buscar_y_crear_carpeta, buscar_carpeta_en_estructura
import os
import tkinter as tk

#**********************************************************************************************************
# Funcion para seleccionar una carpeta por su indice 
def seleccionar_carpeta_por_indice(ruta, indice):

    try:
        # Verificar que la ruta exista y sea un directorio
        if not os.path.isdir(ruta):
            print(f"La ruta {ruta} no es válida o no es un directorio.")
            return None

        # Listar todas las subcarpetas en la ruta
        subcarpetas = [f for f in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, f))]

        # Imprimir las subcarpetas y sus índices
        print(f"Subcarpetas encontradas en '{ruta}':")
        # imprimimos esto para depuración
        for i, subcarpeta in enumerate(subcarpetas):
            print(f"{i}: {subcarpeta}")

        # Verificar si el índice está dentro del rango válido
        if 0 <= indice < len(subcarpetas):
            carpeta_seleccionada = os.path.join(ruta, subcarpetas[indice])
            print(f"Carpeta seleccionada: {carpeta_seleccionada}")
            return carpeta_seleccionada
        else:
            return None
        
    except Exception as e:
        print(f"Error al seleccionar la carpeta: {e}")
        return None

#**********************************************************************************************************
# Funcion para seleccioanr y alamacenar la ruta del proyecto
def seleccionar_carpeta():
    
    # La fecha siempre será None
    fecha = None
    # Crear una ventana oculta de Tkinter
    root = tk.Tk()
    # Ocultar la ventana principal
    root.withdraw()  
    # Abrir la ventana para seleccionar una carpeta
    ruta_carpeta = filedialog.askdirectory(title="Selecciona la carpeta de tu proyecto")
    
    # Comprobar si el usuario seleccionó una carpeta
    if ruta_carpeta:
        # mensaje de depuracion
        print(f"Has seleccionado la carpeta: {ruta_carpeta}")
        
        # Validar la estructura de carpetas
        validacion_estructura = buscar_y_crear_carpeta(ruta_carpeta, fecha) 
        if not validacion_estructura:
            return print('la carpeta seleccionada no cumple el estadar')
               
        # Seleccionamos la primer subcarpeta de la carpeta rastreos
        carpeta_con_fecha = seleccionar_carpeta_por_indice(validacion_estructura,0)
        if not carpeta_con_fecha:
            print("No se encontro ninguna carpeta en la ruta: ")
            return print(validacion_estructura)
        
        # Seleccionamos la carpeta base de la carpeta con fecha      
        carpeta_base = buscar_carpeta_en_estructura(carpeta_con_fecha,'base')
        if not carpeta_base:
            print("No se encontro la carpeta base en la ruta: ")
            return print(carpeta_con_fecha)
        
        # Seleccionamos la primera carpeta_gps
        carpeta_gps = seleccionar_carpeta_por_indice(carpeta_base, 0)
        if not carpeta_gps:
            print("No se encontro la carpeta base en la ruta: ")
            print(carpeta_base)
        
        # devolvemos la ruta de la carpeta GPS en donde se enceuntran las rutas del
        # archivo navegado y el observado, una vez capturadas estas rutas sebe de ir el RPA 
        # con el sotfware RTKLIB
        return carpeta_gps
        
    else:
        print("No se selecciono ninguna carpeta.")




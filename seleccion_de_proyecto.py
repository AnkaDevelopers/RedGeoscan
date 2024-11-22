from tkinter import filedialog
from buscador_de_carpetas import buscar_y_crear_carpeta, buscar_carpeta_en_estructura
import os
import tkinter as tk



#**********************************************************************************************************
# Funcion para seleccionar una carpeta por su indice 
def select_archivo(ruta, extension):
    if not os.path.exists(ruta):
        return print("La ruta no existe")
    if not os.path.isdir(ruta):
        return print("la ruta no es un directorio")
    
    # listar archivos de la ruta
    archivos_encontrados = [
        archivo for archivo in os.listdir(ruta)
        if archivo.endswith(extension)
    ]
    # validamos si encontramos el archivo con la extención ingresada
    if not archivos_encontrados:
        return print("no se encontro el archivo con extencion ", extension)
    
    # retorna la ruta completa 
    ruta_archivo = os.path.join(ruta, archivos_encontrados[0])  # Selecciona el primer archivo
    return ruta_archivo

    
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
        
        # Seleccionamos el archivo .obs de nuestra primera carperta GPS
        ruta_obs = select_archivo(carpeta_gps, '.obs')
        if not ruta_obs:
            print("no se encontro el archivo .OBS")
            
        # Seleccionamos ela rchivo .n de nuestra carpeta gps
        ruta_navegado = select_archivo(carpeta_gps, '.24N')    
        if not ruta_navegado:
            print("no se encontro el archivo navegado")
            
            
        print('*'*20)
        # Diccionario
        rutas_rinex_proyecto = {}
        rutas_rinex_proyecto["ruta_obs"] = ruta_obs
        rutas_rinex_proyecto["ruta_nav"] = ruta_navegado
        rutas_rinex_proyecto["carpeta_gps"] = carpeta_gps
        
        return rutas_rinex_proyecto
        
    else:
        return print("No se selecciono ninguna carpeta.")




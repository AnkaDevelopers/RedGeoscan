from buscador_de_carpetas import buscar_y_crear_carpeta, buscar_carpeta_en_estructura
from tkinter import filedialog
import tkinter as tk
import config
import os

mensaje = config.msj_select_proyect

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
def selec_proyect():
    
    # Variable para almacenar las rutas para el RPA del programa RTKLIB
    rutas_rinex_proyecto = {}
    
    # Se establecio esta variable fecha en none para reutilizar otro componente
    fecha = None
    
    # Crear una ventana oculta de Tkinter
    root = tk.Tk()
    
    # Ocultar la ventana principal
    root.withdraw()  
    
    # Abrir la ventana para seleccionar una carpeta
    ruta_carpeta = filedialog.askdirectory(title= mensaje[0])
    
    # Comprobar si el usuario seleccionó una carpeta
    if ruta_carpeta:
        
        # Mensaje de depuración
        print('*'*50,'\n',mensaje[1],'\n',ruta_carpeta)

        # Ejecución de función para Validar la estructura de carpetas del proyecto
        validacion_estructura = buscar_y_crear_carpeta(ruta_carpeta, fecha) 
        
        # Validación mensaje de depuración
        if not validacion_estructura:
            print('*'*50,'\n',mensaje[2])
            return rutas_rinex_proyecto 
               
        # Ejecución de función para extraer el nombre de las carpetas por indice 0
        carpeta_con_fecha = seleccionar_carpeta_por_indice(validacion_estructura,0)
        
        # Validación mensaje de depuración
        if not carpeta_con_fecha:
            print('*'*50,'\n',mensaje[3],'\n',validacion_estructura)
            return rutas_rinex_proyecto 
        
        # Ejecución de función para Seleccionar la carpeta base de la carpeta con nombre de fecha      
        carpeta_base = buscar_carpeta_en_estructura(carpeta_con_fecha,'base')
        
        # Validación mensaje de depuración
        if not carpeta_base:
            print('*'*50,'\n',mensaje[3],'\n',carpeta_con_fecha)
            return rutas_rinex_proyecto 
        
        # Ejecución de función para extraer el nombre de las carpetas por indice 0
        carpeta_gps = seleccionar_carpeta_por_indice(carpeta_base, 0)
        
        # Validación mensaje de depuración
        if not carpeta_gps:
            print('*'*50,'\n',mensaje[3],'\n',carpeta_base)
            return rutas_rinex_proyecto 
        
        # Ejecución de función para extraer ruta archivo .OBS
        ruta_obs = select_archivo(carpeta_gps, '.obs')
        
        # Validación mensaje de depuración
        if not ruta_obs:
            print('*'*50,'\n',mensaje[4],'\n','.obs')
            return rutas_rinex_proyecto 
            
        # Ejecución de función para extraer ruta archivo .24N
        ruta_navegado = select_archivo(carpeta_gps, '.24N')  
        
        # Validación mensaje de depuración
        if not ruta_navegado:
            print('*'*50,'\n',mensaje[4],'\n','.24n')
            return rutas_rinex_proyecto 
            
        # Creacion de un Diccionario con las rutas para el RPA de RTKLIB
        rutas_rinex_proyecto["ruta_obs"] = ruta_obs
        rutas_rinex_proyecto["ruta_nav"] = ruta_navegado
        rutas_rinex_proyecto["carpeta_gps"] = carpeta_gps
        
        return rutas_rinex_proyecto
        
    else:
        print('*'*50,'\n',mensaje[5])
        return rutas_rinex_proyecto




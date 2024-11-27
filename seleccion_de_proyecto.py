from buscador_de_carpetas import buscar_y_crear_carpeta, buscar_carpeta_en_estructura
from rpa_rtklib import ejecutar_rtk
from tkinter import filedialog
import tkinter as tk
import config
import time
import os

mensaje = config.msj_select_proyect

#**********************************************************************************************************
# Función para seleccionar un archivo por su extensión y ruta
def select_archivo(ruta, extension):
    
    # Validación: En caso de que la ruta no exista
    if not os.path.exists(ruta):
        return print('*'*50,'\n',mensaje[10],'\n', ruta)
    
    # Validación: En caso de que el directorio no exista
    if not os.path.isdir(ruta):
        return print('*'*50,'\n',mensaje[5],'\n', ruta)
    
    # Listar archivos con la extensión deseada en la ruta
    archivos_encontrados = [
        archivo for archivo in os.listdir(ruta)
        if archivo.endswith(extension)
    ]
    
    # Validar si se encontraron archivos con la extensión ingresada
    if not archivos_encontrados:
        return print('*'*50,'\n',mensaje[11],'\n',extension)

    # Creamos la ruta dek archivo encontrado    
    ruta_archivo = os.path.join(ruta, archivos_encontrados[0])
    print('*' * 50, '\n', "Archivo seleccionado:", '\n', ruta_archivo)
    
    # Retorna la ruta completa del archivo seleccionado
    return ruta_archivo

#**********************************************************************************************************
# Funcion para seleccionar una carpeta por su indice 
def seleccionar_carpeta_por_indice(ruta, indice):

    try:
        
        # Validación de que la ruta exista y sea un directorio
        if not os.path.isdir(ruta):
            print('*'*50,'\n',mensaje[6],'\n',ruta)
            return None

        # Listar todas las subcarpetas en la ruta
        subcarpetas = [f for f in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, f))]

        # Imprimir las subcarpetas y sus índices
        print('*'*50,'\n',mensaje[7],'\n',ruta)
        
        # imprimimos esto para depuración
        for i, subcarpeta in enumerate(subcarpetas):
            print(f"{i}: {subcarpeta}")

        # Verificar si el índice está dentro del rango válido
        if 0 <= indice < len(subcarpetas):
            carpeta_seleccionada = os.path.join(ruta, subcarpetas[indice])
            print('*'*50,'\n',mensaje[8],'\n',carpeta_seleccionada)
            return carpeta_seleccionada
        else:
            return None
        
    except Exception as e:
        print('*'*50,'\n',mensaje[9],'\n',e)
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
    ruta_carpeta_proyecto = filedialog.askdirectory(title= mensaje[0])
    
    # Comprobar si el usuario seleccionó una carpeta
    if ruta_carpeta_proyecto:
        
        # Mensaje de depuración
        print('*'*50,'\n',mensaje[1],'\n',ruta_carpeta_proyecto)

        # Ejecución de función para Validar la estructura de carpetas del proyecto
        validacion_estructura = buscar_y_crear_carpeta(ruta_carpeta_proyecto, fecha) 
        
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
        
        # Verificamos si ya existe un archivo .pos
        ruta_pos = select_archivo(carpeta_gps, '.pos')
        
        # Validamos si encontgramos un archivo .pos
        if ruta_pos:
            
            # Si post existe entonses enviamos la ruta del proyecto la carpeta gps y confirmamos que si existe un archivo .pos en el directorio
            return ruta_carpeta_proyecto, ruta_pos
        
        # En caso de no encontrar un archivo .pos          
        else:    
        
            # Ejecución de función para extraer ruta archivo .OBS
            ruta_obs = select_archivo(carpeta_gps, '.obs')
        
            # Validación mensaje de depuración
            if not ruta_obs:
                ruta_obs = select_archivo(carpeta_gps, '.24O')
            
                if not ruta_obs:
                 return print('*'*50,'\n',mensaje[4],'\n','.obs ni .24O')
            
            # Ejecución de función para extraer ruta archivo .24N
            ruta_navegado = select_archivo(carpeta_gps, '.24N')  
        
            # Validación mensaje de depuración
            if not ruta_navegado:
                print('*'*50,'\n',mensaje[4],'\n','.24n')
                return rutas_rinex_proyecto 
        
            # Creación de un Diccionario con las rutas para el RPA de RTKLIB
            rutas_rinex_proyecto["ruta_obs"] = ruta_obs
            rutas_rinex_proyecto["ruta_nav"] = ruta_navegado
            rutas_rinex_proyecto["carpeta_gps"] = carpeta_gps
            
            # Retornamos una lista con la lista de los archivos necesarios para el RPA
            exito = ejecutar_rtk(rutas_rinex_proyecto)
              
            # Validamos si la funcion se ejecuto correctamente
            if not exito:
                 return print('*'*50,'\n','error en rpa')
            
            # Extraemos la ruta de nuestro archivo .pos
            ruta_pos = select_archivo(carpeta_gps, '.pos')

            # Si todo va bien seguira por este camino
            return ruta_carpeta_proyecto, ruta_pos
    
    # Mensaje en caso de no seleccionar ninguna carpeta de proyecto        
    else:
        print('*'*50,'\n',mensaje[5])
        return rutas_rinex_proyecto, ruta_pos




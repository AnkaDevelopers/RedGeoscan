from buscador_de_carpetas import buscar_carpeta_en_estructura, listar_carpetas_en_ruta
from tkinter import filedialog
import tkinter as tk
import config
import os

mensaje = config.msj_select_proyect

#**********************************************************************************************************
# Función para seleccionar y almacenar la ruta del proyecto
def selec_proyect():
  
    # Variable donde almaceno la ruta de mi proyecto
    ruta_carpeta_proyecto = None
    
    # Crear una ventana oculta de Tkinter
    root = tk.Tk()
    
    # Ocultar la ventana principal
    root.withdraw()  
    
    # Abrir la ventana para seleccionar una carpeta
    ruta_carpeta_proyecto = filedialog.askdirectory(title=mensaje[0])
    
    # Comprobar si el usuario seleccionó una carpeta
    if ruta_carpeta_proyecto:
        
        # Validar la estructura de carpetas del proyecto
        carpeta_procesamiento = buscar_carpeta_en_estructura(ruta_carpeta_proyecto, 'Procesamiento') 
        
        if not carpeta_procesamiento:
            return ruta_carpeta_proyecto
        
        carpeta_topografia = buscar_carpeta_en_estructura(carpeta_procesamiento, 'Topografia')
        
        if not carpeta_topografia:
            return ruta_carpeta_proyecto
        
        carpeta_rastreos = buscar_carpeta_en_estructura(carpeta_topografia, 'Rastreos')
        
        if not carpeta_rastreos:
            return ruta_carpeta_proyecto
        
        # Obtener la lista de carpetas días-rastreos
        lista_carpeta_dias_rastreos = listar_carpetas_en_ruta(carpeta_rastreos)
        
        if not lista_carpeta_dias_rastreos:
            return ruta_carpeta_proyecto
        
        # Obtener el nombre del proyecto desde la ruta
        nombre_proyecto = os.path.basename(ruta_carpeta_proyecto)
        
        # Inicializar las listas para las rutas
        proyecto_info = {
            "ruta_proyecto": ruta_carpeta_proyecto,
            "nombre_proyecto": nombre_proyecto,
            "dias_rastreos": {}
        }
        
        # Recorrer cada carpeta días-rastreos
        for carpeta_dia in lista_carpeta_dias_rastreos:
            ruta_carpeta_dia = os.path.join(carpeta_rastreos, carpeta_dia)
            
            # Inicializar el diccionario para cada día
            proyecto_info["dias_rastreos"][carpeta_dia] = {
                "subcarpetas_base": [],
                "redActiva": None
            }
            
            # Buscar carpeta base
            carpeta_base = buscar_carpeta_en_estructura(ruta_carpeta_dia, 'base')
            
            if carpeta_base:
                # Listar subcarpetas dentro de la carpeta base
                subcarpetas_base = [
                    os.path.join(carpeta_base, subcarpeta)
                    for subcarpeta in os.listdir(carpeta_base)
                    if os.path.isdir(os.path.join(carpeta_base, subcarpeta))
                ]
                proyecto_info["dias_rastreos"][carpeta_dia]["subcarpetas_base"] = subcarpetas_base
            
            # Buscar carpeta redActiva
            carpeta_red_activa = buscar_carpeta_en_estructura(ruta_carpeta_dia, 'redActiva')
            if carpeta_red_activa:
                proyecto_info["dias_rastreos"][carpeta_dia]["redActiva"] = carpeta_red_activa
        
        # Imprimir el resultado
        #print(proyecto_info)
        
        return proyecto_info
    
    else:
        print('*' * 50, '\n', mensaje[5])
        return None

#**********************************************************************************************************
# Función para almacenar las rutas de las sub carpetas
def transformar_subcarpetas(diccionario_proyecto):
    
    # Iterar sobre los días de rastreo
    for dia, info in diccionario_proyecto["dias_rastreos"].items():
        subcarpetas_dict = {}  # Diccionario para las nuevas claves y valores
        
        # Recorrer las rutas de subcarpetas_base
        for ruta in info["subcarpetas_base"]:
            # Extraer el nombre de la carpeta GPS (última parte de la ruta)
            nombre_carpeta = os.path.basename(ruta.strip("\\"))
            
            # Convertir la ruta al formato de Windows
            ruta_windows = os.path.normpath(ruta)
            
            # Crear el par clave-valor
            subcarpetas_dict[nombre_carpeta] = ruta_windows
        
        # Reemplazar la lista de subcarpetas_base con el nuevo diccionario
        info["subcarpetas_base"] = subcarpetas_dict
    
    return diccionario_proyecto

#**********************************************************************************************************
# Función para actualizar las rutas de los archivos .pos, .obs, .24o, y .24n
def buscar_archivos_en_gps(diccionario_proyecto):

    # Extensiones que buscamos
    extensiones = ["pos", "obs", "24o", "24n"]
    
    # Iterar sobre los días de rastreo
    for dia, info in diccionario_proyecto["dias_rastreos"].items():
        subcarpetas_actualizadas = {}
        
        # Recorrer cada GPS en subcarpetas_base
        for gps_nombre, datos in info["subcarpetas_base"].items():
            
            # Si `datos` ya es un diccionario, extraer la ruta base desde `pos` u otra clave válida
            if isinstance(datos, dict):
                ruta_gps = os.path.dirname(datos["pos"]) if datos["pos"] != 0 else None
            else:
                # Si `datos` es un string, asumir que es la ruta de la carpeta GPS
                ruta_gps = datos

            archivos_encontrados = {ext: 0 for ext in extensiones}  # Inicializar claves con 0
            
            # Verificar que la ruta existe
            if ruta_gps and os.path.exists(ruta_gps) and os.path.isdir(ruta_gps):
                for archivo in os.listdir(ruta_gps):
                    ruta_archivo = os.path.join(ruta_gps, archivo)
                    
                    # Convertir el nombre del archivo a minúsculas para comparar
                    archivo_lower = archivo.lower()
                    
                    # Comprobar si el archivo tiene una de las extensiones buscadas
                    for ext in extensiones:
                        if archivo_lower.endswith(f".{ext}") and archivos_encontrados[ext] == 0:
                            archivos_encontrados[ext] = ruta_archivo
            
            # Guardar los resultados en el nuevo formato
            subcarpetas_actualizadas[gps_nombre] = archivos_encontrados
        
        # Actualizar subcarpetas_base con la nueva estructura
        info["subcarpetas_base"] = subcarpetas_actualizadas
    
    return diccionario_proyecto

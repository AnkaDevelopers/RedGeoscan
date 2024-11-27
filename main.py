from extraer_token_rinex_y_descarga import extraer_token_para_descarga_rinex
from agrupar_rinex_x_antena import crear_lista_antenas_x_rinex
from consumo_servicios import servicio_administrador_antenas
from crear_lista_antenas import insertar_datos_antenas
from seleccion_de_proyecto import selec_proyect
from filtro_antenas_igac import filtro_antenas_igac
from calculos import calcular_antenas_mas_cercanas
from cargar_kml import cargar_base_kml
from cargar_pos import cargar_base_pos
from token_principal import rpa_igac, cerrar_edge
from tkinter import ttk
import tkinter as tk 
import threading
import pandas as pd
import time
import os

#***************************************************************************************************************
# Variables globales y sus valores iniciales
confirmacion_btn_carga_proyecto = None
ruta_carpeta_gps= None
ruta_carpeta_proyecto = None
coordenada_media_base = None
datos_kml = None
datos_kml_order = None
antenas_con_administrador = None
barra_visible = False 
fecha_mas_un_dia = None
fecha = None
dataSet_antenas = None
token_principal = None
progreso_barra = 10
paso_actual = 0  
ruta_descarga = None


#***************************************************************************************************************
# Función para limpiar las variables globales
def limpiar():
    global datos_kml_order, coordenada_media_base, antenas_con_administrador, barra_visible, fecha_mas_un_dia, fecha, dataSet_antenas, token_principal, progreso_barra, paso_actual, ruta_descarga
    
    # Restablecer las variables a sus valores iniciales
    coordenada_media_base = None
    antenas_con_administrador = None
    barra_visible = False 
    fecha_mas_un_dia = None
    fecha = None
    dataSet_antenas = None
    token_principal = None
    progreso_barra = 10
    paso_actual = 0
    ruta_descarga = None
    datos_kml_order = None
    print("Variables globales restablecidas a sus valores iniciales.")
    
#***************************************************************************************************************
# Ejecuta funcion en un segundo hilo
def iniciar_consumir_servicio_token_principal():
    hilo = threading.Thread(target=consumir_servicio_token_principal)
    hilo.start()
    
#***************************************************************************************************************
# Función para imprimir variables y depurar
def imprimir():
    print(dataSet_antenas)

#***************************************************************************************************************
# Barra de progreso: controla el avance basado en parámetros
def barra_de_progreso(valor_maximo, progreso_actual):
    global barra_visible

    # Configurar la barra de progreso solo la primera vez
    if not barra_visible:
        barra_progreso['maximum'] = valor_maximo  # Establecer el valor máximo
        barra_progreso['value'] = 0  # Reiniciar el valor actual
        barra_progreso.pack(pady=10)
        barra_visible = True

    # Actualizar el valor actual de la barra
    barra_progreso['value'] = progreso_actual

    # Ocultar la barra cuando se completa el progreso
    if progreso_actual >= valor_maximo:
        barra_progreso.pack_forget()
        barra_visible = False

    ventana.update_idletasks()  # Actualizar la interfaz


#***************************************************************************************************************
# Función consumir servicio token de descarga según id rinex de manera secuencial
def consumir_token_descarga_rinex():
    global ruta_descarga, ruta_carpeta_gps
    
    ruta = extraer_token_para_descarga_rinex(
        confirmacion_btn_carga_proyecto, 
        ruta_carpeta_proyecto, dataSet_antenas, 
        token_principal, 
        fecha, 
        barra_de_progreso)
    
    print("descarga completa de los archivos rinex",'\n', ruta)
    
    ruta_carpeta_gps = None
    
    insertar_datos_antenas(tabla_antenas, dataSet_antenas, ruta)
    #print("insercion de los datos en la tabla")
    
# ***************************************************************************************************************
# Función consumir servicio filtro de antenas para verificar si contiene rinex según fecha
def consumir_servicio_token_principal():
    
    # Llamamos nuestra variable global donde vamos a almacenar nuestro token principal
    global token_principal
    
    # Llamamos nuestra función para extraer el token principal
    token_principal = rpa_igac() 
    
    # Validamos que token principal exista
    if not token_principal:
        
        # En caso de no haber podido capturar el token principal lo intentamos una segunda vez
        time.sleep(2)
        token_principal = rpa_igac() 
        
        # Si en el segundo intento tampoco lo podemos capturar terminamos el proceso
        if not token_principal:
            
            # Mensaje de depuración
            return print('fallo en extraer el token principal') 
    
    # Llamamos ala funcion para extraer los datos de descarag de los rinex
    consumir_token_descarga_rinex()


#***************************************************************************************************************
# Función para consumir servicio y verificar si las antenas contienen datos RINEX según la fecha
def consumir_servicio_segun_fecha():
    
    # Variable global donde se alamcenan la lista de antenas con rinex
    global dataSet_antenas

    # Crear una base de las antenas con datos RINEX o no
    dataSet_antenas = crear_lista_antenas_x_rinex(fecha, fecha, antenas_con_administrador)

    # Validar si el DataFrame está vacío
    if dataSet_antenas.empty:
        
        # Mensaje en caso de que el DataFrame esté vacío
        mensaje = 'No Ingresaron Datos en dataFrame de antenas con rinex'      
        label_estado_base_kml.config(text=mensaje)
        
        # Finalizamos el proceso y devolvemos un mensaje de depuración
        return print('*' * 150, '\n', 'No Ingresaron Datos en dataFrame de antenas con rinex')

    # Validar si todos los valores de la columna 'has_rinex' son False
    if dataSet_antenas['has_rinex'].any() == False:
        
        # Mensaje en caso de que no se halla encontrado ningun rinex en ninguna antena
        mensaje = 'En el momento no hay rinex de ninguna antena.'
        label_estado_base_kml.config(text=mensaje)
        
        # Finalizamos el proceso y devolvemos un mensaje de depuración
        print('*' * 150, '\n', dataSet_antenas, '\n', '*' * 150)
        return print('\n','*' * 150, '\n', 'En el momento no hay rinex de ninguna antena.','\n','*'*150)

    # Si se encontro almenos un resultado, Contar cuántas antenas tienen RINEX
    count_rinex = dataSet_antenas['has_rinex'].sum()

    # Mensaje en caso de que haya antenas con datos RINEX
    mensaje = f'Se encontraron resultados de RINEX en {count_rinex} antenas.'
    label_estado_base_kml.config(text=mensaje)

    # Imprimir antenas con RINEX
    print('*' * 100, '\n', dataSet_antenas, '\n', '*' * 100)

    # Cerrar procesos de Microsoft Edge y esperar
    time.sleep(0.5)
    cerrar_edge()
    time.sleep(0.5)

    # Llamamos nuestra funcion que trae el modulo que captura el token principal
    iniciar_consumir_servicio_token_principal()

#***************************************************************************************************************
# funcion consumir servicio y crear base de antenas
def consumir_servicio_andimistrador_antenas():
    
    # Llamamos la variable gobal donde podremos almacenar la relación de la antena y su administrador
    global antenas_con_administrador
    
    # este servicio me crea una base con la información de las antenas esta base que da como un archivo json con la fecha 
    servicio_administrador_antenas()
    
     # Mensaje de depuración
    print('*'*200,'\n','Carga Base de antenas con administrador')
    print('*'*200,'\n')
    
    # me devuelve una lista de las antenas que pertenesen al igac y la lista de la que no ordenadas por distancia a mi coordenada base
    antenas_con_administrador = filtro_antenas_igac(datos_kml_order)
    
    # Mensaje de depuración
    print('Administrador antenas:', len(antenas_con_administrador), '\n', antenas_con_administrador,'\n','*'*100)
    
    #servicio para buscar archivos rinex segun fecha
    consumir_servicio_segun_fecha()

#***************************************************************************************************************
# funcion principal calcular las  antenas mas cercanas
def calcular_antenas():
    
    
    # Llamamos la variables globales las cuales se encuentran en NONE
    global coordenada_media_base, datos_kml, datos_kml_order, fecha, fecha_mas_un_dia, ruta_carpeta_gps
       
    # Captura de respuestas por parte de la funcion cargar_base_pos
    coordenada_media_base, mensaje_pos, fecha, fecha_mas_un_dia = cargar_base_pos(tabla_coordenada_media, ruta_carpeta_gps)
    
    # Actualización de mensaje de interfaz
    label_estado_archivo_pos.config(text=mensaje_pos)
    
    # Validación de coordenada_media_base
    if not coordenada_media_base:
        return print('*'*50,'\n','No se pudo calcular la coordenada media base')
    
    # Mensaje de depuración
    print('*'*200,'\n','Se calculo exitosamente la coordenada media')
    print('*'*200,'\n')
    print('-'*200,'\n')
     
    # Funcion para calcular las antenas mas cercanas a mi coordenada media base
    datos_kml_order = calcular_antenas_mas_cercanas((coordenada_media_base['latitud'],coordenada_media_base['longitud']),datos_kml)
    
    # Validacion que kml contenga algo
    if datos_kml_order.empty:
        return print('Data frame de las antenas mas cercanas vacio')
    
    # Mensaje de depuración
    print('\n', 'Antenas mas cercanas:', len(datos_kml_order), '\n', datos_kml_order)

    # Mensaje de depuración
    print('*'*200,'\n','Se calculo exitosamente la lista de antenas mas cercanas')
    print('*'*200,'\n')
    print('-'*200,'\n')
       
    # Llamamos la funcion para consumir un servicio que nos trae una base de informacion de las antenas de la red geodesica
    consumir_servicio_andimistrador_antenas()

#***************************************************************************************************************
# cargar archivo kml antenas base del IGAC
def Seleccionar_proyecto():
    
    # Variable global para almacenar las rutas del proyecto 
    global ruta_carpeta_proyecto, ruta_carpeta_gps, confirmacion_btn_carga_proyecto
    
    # Ejecucion de función para seleccionar el proyecto
    ruta_carpeta_proyecto, ruta_carpeta_gps = selec_proyect()
    
    # Validacion de ruta del archivo .pos
    if not ruta_carpeta_proyecto and not ruta_carpeta_gps:
        return print('*'*50,'\n','No hay rutas')

    # Mensaje de depuración
    print('*'*200,'\n','Archivo .pos creado o ubicado satisfactoriamente')
    print('*'*200,'\n')
    print('-'*200,'\n')
    
    # llamamos la función de calcular antenas
    confirmacion_btn_carga_proyecto = True
    calcular_antenas()
    
#***************************************************************************************************************
# Cargar archivo KML que contiene la lista de las antenas Geodesicas de la red activa
def cargar_archivo_kml():
    
    # Variable para almacenar los datos del kml
    global datos_kml
    
    # Función para cargar archivo kml
    datos_kml,mensaje_kml = cargar_base_kml()
    
    # Validamos que el archivo KML contenga datos
    if datos_kml.empty:
        return print('*'*50,'\n','Archivo kml esta vacio')

    # Mensaje de depuración
    print('*'*200,'\n','Archivo KML cargado exitosamente')
    print('*'*200,'\n')
    print('-'*200,'\n')
    
    # Actualizamos el mensaje de la interfaz
    label_estado_base_kml.config(text=mensaje_kml)
    
# **************************************************************************************************************
# Funcion para cerrar el programa
def cerrar_programa():
    
    # Destruye la ventana principal
    ventana.destroy()  
    
    # Finaliza el proceso completo del programa incluyendo los hilos
    os._exit(0)
    
# *****************************************ESTILOS TKINTER******************************************************
# Configuración de la ventana principal 
ventana = tk.Tk()
ventana.geometry("800x600")
ventana.title("Antenas más cercanas")
ventana.protocol("WM_DELETE_WINDOW", cerrar_programa)

#***************************************************************************************************************
# Tabla de antenas mas cercanas
# Etiqueta para el mensaje de estado de la base KML
label_estado_base_kml = tk.Label(ventana, text="Cargando base de antenas KMZ..", fg="green")
label_estado_base_kml.pack(pady=1)
# LabelFrame para Antenas Más Cercanas
frame_antenas = tk.LabelFrame(ventana, text="Antenas más cercanas", padx=10, pady=10)
frame_antenas.pack(pady=20, padx=20, fill="both")

# Crear tabla para mostrar antenas más cercanas en el frame
tabla_antenas = ttk.Treeview(frame_antenas, columns=("Nombre", "Latitud", "Longitud", "Distancia", "Administrador"), show="headings", height=8)
tabla_antenas.heading("Nombre", text="Nombre")
tabla_antenas.heading("Latitud", text="Latitud (G° M' S\")")
tabla_antenas.heading("Longitud", text="Longitud (G° M' S\")")
tabla_antenas.heading("Distancia", text="Distancia (km)")
tabla_antenas.heading("Administrador", text="Administrador")

# Ajustar el ancho de cada columna
tabla_antenas.column("Nombre", width=100, anchor="center")          # Ajuste para el nombre
tabla_antenas.column("Latitud", width=150, anchor="center")         # Ajuste para latitud
tabla_antenas.column("Longitud", width=150, anchor="center")        # Ajuste para longitud
tabla_antenas.column("Distancia", width=100, anchor="center")       # Ajuste para la distancia
tabla_antenas.column("Administrador", width=100, anchor="center")   # Ajuste para el Administrador de la antena 

tabla_antenas.pack(pady=5, padx=5, fill="both")

#***************************************************************************************************************
# Tabla de coordenada media base
# Etiqueta para el mensaje de estado del archivo .POS
label_estado_archivo_pos = tk.Label(ventana, text="Esperando Archivo pos", fg="green")
label_estado_archivo_pos.pack(pady=1)
# LabelFrame para Coordenada Media Base
frame_coordenada_media = tk.LabelFrame(ventana, text="Coordenada Media Base", padx=10, pady=10)
frame_coordenada_media.pack(pady=20, padx=20, fill="both")

# Tabla para mostrar la coordenada media base
tabla_coordenada_media = ttk.Treeview(frame_coordenada_media, columns=("Latitud", "Longitud", "Altura", "Semana GPS", "Dia del Año"), show="headings", height=1)
tabla_coordenada_media.heading("Latitud", text="Latitud (G° M' S\")")
tabla_coordenada_media.heading("Longitud", text="Longitud (G° M' S\")")
tabla_coordenada_media.heading("Altura", text="Altura (metros)")
tabla_coordenada_media.heading("Semana GPS", text="Semana GPS")
tabla_coordenada_media.heading("Dia del Año", text="Día del Año")

# Ajustar el ancho de cada columna
tabla_coordenada_media.column("Latitud", width=120,anchor="center")       
tabla_coordenada_media.column("Longitud", width=120,anchor="center")      
tabla_coordenada_media.column("Altura", width=120,anchor="center")        
tabla_coordenada_media.column("Semana GPS", width=100,anchor="center")    
tabla_coordenada_media.column("Dia del Año", width=100,anchor="center")    
tabla_coordenada_media.pack(pady=5, padx=5, fill="both")

#***************************************************************************************************************
# Boton para cargar archivos
# Frame para los botones de cargar archivos
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)
# Botón para cargar proyecto
boton_cargar_pos = tk.Button(frame_botones, text="Seleccionar Proyecto 🌍", command=Seleccionar_proyecto)
boton_cargar_pos.pack(side=tk.LEFT, padx=10)
# Botón para cargar archivo POS
boton_cargar_pos = tk.Button(frame_botones, text="Cargar archivo POS 📡", command=calcular_antenas)
boton_cargar_pos.pack(side=tk.LEFT, padx=10)
# Botón para imprimir variables solo para depuración
boton_cargar_pos = tk.Button(frame_botones, text="imprimir variable 🔧", command=imprimir)
boton_cargar_pos.pack(side=tk.LEFT, padx=10)
# Barra de progreso en modo "determinate", inicialmente no visible
barra_progreso = ttk.Progressbar(ventana, orient="horizontal", mode="determinate", length=300)

cargar_archivo_kml()

ventana.mainloop()
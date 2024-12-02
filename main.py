from seleccion_de_proyecto import selec_proyect,transformar_subcarpetas, buscar_archivos_en_gps
from extraer_token_rinex_y_descarga import extraer_token_para_descarga_rinex
from guardar_token_principal import crear_archivo_con_fecha_y_hora
from agrupar_rinex_x_antena import crear_lista_antenas_x_rinex
from consumo_servicios import servicio_administrador_antenas
from crear_lista_antenas import insertar_datos_antenas
from filtro_antenas_igac import filtro_antenas
from calculos import calcular_antenas_mas_cercanas
from token_principal import rpa_igac, cerrar_edge
from rpa_rtklib import ejecutar_rtk_para_gps
from cargar_kml import cargar_base_kml
from cargar_pos import cargar_base_pos
from generar_log import agregar_log
from tkinter import ttk
import tkinter as tk 
import pandas as pd
import threading
import time
import os

#***************************************************************************************************************
# Variables globales y sus valores iniciales
confirmacion_btn_carga_proyecto = None
ruta_carpeta_gps= None
info_proyecto = None
coordenada_media_base = None
datos_kml = None
datos_kml_order = None
antenas_con_administrador = None
barra_visible = False 
fecha_mas_un_dia = None
fecha = None
lista_antenas_con_rinex = None
token_principal = None
progreso_barra = 10
paso_actual = 0  
ruta_descarga = None


#***************************************************************************************************************
# Función para limpiar las variables globales
def limpiar():
    global datos_kml_order, coordenada_media_base, antenas_con_administrador, barra_visible, fecha_mas_un_dia, fecha, lista_antenas_con_rinex, token_principal, progreso_barra, paso_actual, ruta_descarga
    
    # Restablecer las variables a sus valores iniciales
    coordenada_media_base = None
    antenas_con_administrador = None
    barra_visible = False 
    fecha_mas_un_dia = None
    fecha = None
    lista_antenas_con_rinex = None
    token_principal = None
    progreso_barra = 10
    paso_actual = 0
    ruta_descarga = None
    datos_kml_order = None
    print("Variables globales restablecidas a sus valores iniciales.")
    
#***************************************************************************************************************
# Función para imprimir variables y depurar
def imprimir():
    print(token_principal)

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
    
    
    ruta = extraer_token_para_descarga_rinex(lista_antenas_con_rinex)
    
    return
    
    print("descarga completa de los archivos rinex",'\n', ruta)
    
    ruta_carpeta_gps = None
    
    insertar_datos_antenas(tabla_antenas, lista_antenas_con_rinex, ruta)
    #print("insercion de los datos en la tabla")
    
#***************************************************************************************************************
# Función para consumir servicio y verificar si las antenas contienen datos RINEX según la fecha
def consumir_servicio_segun_fecha():
    
    # Variable global donde se alamcenan la lista de antenas con rinex
    global lista_antenas_con_rinex

    # Crear una base de las antenas con datos RINEX o no
    lista_antenas_con_rinex = crear_lista_antenas_x_rinex(fecha, fecha, datos_kml_order)
    
    if not lista_antenas_con_rinex:
        return label_estado_base_kml.config(text='Lista de antenas vacia.')
    

    # Validar si ninguna antena tiene datos RINEX
    if all(antena.get('has_rinex') == "False" for antena in lista_antenas_con_rinex):
        return label_estado_base_kml.config(text='No se encontraron archivos RINEX de ninguna antena.')
        
    # Contar el número de antenas con has_rinex = "True"
    numero_antenas_con_rinex = sum(antena.get('has_rinex') == "True" for antena in lista_antenas_con_rinex)
    
    # Mensaje en caso de que haya antenas con datos RINEX
    mensaje = f'Se encontraron resultados de RINEX en {numero_antenas_con_rinex} antenas.'
    label_estado_base_kml.config(text=mensaje)
    
    print('Administrador antenas:', len(lista_antenas_con_rinex), '\n', lista_antenas_con_rinex,'\n','*'*100)

    consumir_token_descarga_rinex()

#***************************************************************************************************************
# funcion consumir servicio y crear base de antenas
def consumir_servicio_andimistrador_antenas():
    
    # Llamamos la variable gobal donde podremos almacenar la relación de la antena y su administrador
    global datos_kml_order
    
    # este servicio me crea una base con la información de las antenas esta base que da como un archivo json con la fecha 
    servicio_administrador_antenas()
    
    # Mensaje de depuración
    print('*'*200,'\n','Carga Base de antenas con administrador','\n','*'*200)
   
    # me devuelve una lista de las antenas que pertenesen al igac y la lista de la que no ordenadas por distancia a mi coordenada base
    datos_kml_order = filtro_antenas(datos_kml_order)# Mensaje de depuración
    # print('Administrador antenas:', len(datos_kml_order), '\n', datos_kml_order,'\n','*'*100)
    
    #servicio para buscar archivos rinex segun fecha
    consumir_servicio_segun_fecha()
    return

#***************************************************************************************************************
# funcion principal calcular las  antenas mas cercanas
def calcular_antenas(ruta_pos):
    
    # Llamamos la variables globales las cuales se encuentran en NONE
    global coordenada_media_base, datos_kml, datos_kml_order, fecha, fecha_mas_un_dia
       
    # Captura de respuestas por parte de la funcion cargar_base_pos
    coordenada_media_base, mensaje_pos, fecha, fecha_mas_un_dia = cargar_base_pos(tabla_coordenada_media, ruta_pos)
    
    # Actualización de mensaje de interfaz
    label_estado_archivo_pos.config(text=mensaje_pos)
    
    print(coordenada_media_base)
    
    # Validación de coordenada_media_base
    if not coordenada_media_base:
        return print('*'*50,'\n','No se pudo calcular la coordenada media base')

    # Funcion para calcular las antenas mas cercanas a mi coordenada media base
    datos_kml_order = calcular_antenas_mas_cercanas((coordenada_media_base['latitud'],coordenada_media_base['longitud']),datos_kml)
       
    # Mensaje de depuración
    # print('\n', 'Antenas mas cercanas:', len(datos_kml_order), '\n','Lista de antenas cercanas: ','\n', datos_kml_order)
    
    # Convertir DataFrame a diccionario
    datos_kml_order = datos_kml_order.to_dict(orient='records')
    
    # Llamamos la funcion para consumir un servicio que nos trae una base de informacion de las antenas de la red geodesica
    consumir_servicio_andimistrador_antenas()

#***************************************************************************************************************
# función para procesar cada archivo .pos
def imprimir_rutas_pos(diccionario_proyecto):

    # Iterar sobre los días de rastreo
    for dia, info in diccionario_proyecto["dias_rastreos"].items():
        print(f"Día: {dia}")
        
        # Iterar sobre las carpetas GPS en cada día
        for gps_nombre, rutas in info["subcarpetas_base"].items():
            ruta_pos = rutas.get("pos")
            
            # Verificar si existe un archivo .pos para esta carpeta GPS
            if ruta_pos and ruta_pos != 0:  # Asegurarnos de que no sea 0
                calcular_antenas(ruta_pos)
                #print(f"Carpeta GPS: {gps_nombre}, Archivo .pos: {ruta_pos}")


# ***************************************************************************************************************
# Función para ejecutar un RPA que extraerá el token principal
def conseguir_token_y_guardarlo():
    # Llamamos la variables globales
    global token_principal , barra_visible
    # Variable para controlar el estado del hilo
    token_extraido = threading.Event()
    progreso_actual = 0
    valor_maximo = 100
    # Inicializar la barra de progreso
    if not barra_visible:
        barra_progreso['maximum'] = valor_maximo
        barra_progreso['value'] = 0
        barra_progreso.pack(pady=10)
        barra_visible = True
        
    # ***************************************************************************************************************
    # Función para ejecutar el RPA en un hilo separado
    def ejecutar_rpa():
        # Llamamos la variables globales
        global token_principal
        # Llamamos la variables local
        nonlocal token_extraido 
        # Mensaje de depouración
        print("Iniciando extracción del token principal con RPA...")
        # Actualizamos el mensaje de la interfaz
        label_estado_barra_progreso.config(text='Buscando token Principal')
        # Ejecutamos el rpa
        token = rpa_igac()  
        # Validamos al extracción del token 
        if token: 
            # Guardamos el token en nuestar variable global
            token_principal = token
        # Marcar como terminado
        token_extraido.set()  

    # ***************************************************************************************************************
    # Función para actualizar la barra de progreso
    def actualizar_barra():
        # Llamamos la variables local
        nonlocal progreso_actual
        # validamos si ya el rpa_igac termino
        if not token_extraido.is_set():
            # Incrementar el progreso
            progreso_actual += 5  
            if progreso_actual > valor_maximo:
                # Reiniciar la barra para simular progreso continuo
                progreso_actual = 0   
            barra_progreso['value'] = progreso_actual
            ventana.update_idletasks()
            # Reprogramar la función
            ventana.after(200, actualizar_barra)  
        else:
            # Cuando el hilo termina
            time.sleep(0.1)
            if token_principal:
                label_estado_barra_progreso.config(text='Token principal capturado exitosamente.')
                barra_progreso['value'] = valor_maximo
                crear_archivo_con_fecha_y_hora(token_principal)
            else:
                # Actualizamos el mensaje de la interfaz
                label_estado_barra_progreso.config(text='Fallo en extraer el token principal.')
                print('Fallo en extraer el token principal.')
                barra_progreso['value'] = 0
            # Ocultar la barra de progreso
            barra_progreso.pack_forget()
            barra_visible = False
            ventana.update_idletasks()
    # Iniciar el hilo para ejecutar el RPA
    hilo_rpa = threading.Thread(target=ejecutar_rpa)
    hilo_rpa.start()
    # Iniciar la actualización de la barra de progreso
    actualizar_barra()


#***************************************************************************************************************
# cargar archivo kml antenas base del IGAC
def Seleccionar_proyecto():
    # Variable global para almacenar las rutas del proyecto 
    global info_proyecto
    # Ejecucion de función para seleccionar el proyecto
    info_proyecto = selec_proyect()
    # Validacion de ruta del proyecto
    if not info_proyecto:
        return print('*'*50,'\n','fallo1')
    # Ejecucion de funcion para organizar diccionario de rutas
    info_proyecto = transformar_subcarpetas(info_proyecto)
    # Ejecucion de funcion para buscar las rutas de los archivos para el rtklib
    info_proyecto = buscar_archivos_en_gps(info_proyecto)
    # Ejecucion de rpa
    ejecutar_rtk_para_gps(info_proyecto)
    # Ejecucion de funcion para buscar las rutas de los archivos para el rtklib
    info_proyecto = buscar_archivos_en_gps(info_proyecto)
    # Diccionarioa actualizado
    #print(info_proyecto)
    # Conseguir token Principal
    conseguir_token_y_guardarlo()
    imprimir_rutas_pos(info_proyecto)
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
# Etiqueta para el mensaje de estado del archivo .POS
label_estado_barra_progreso = tk.Label(ventana, text="", fg="green")
label_estado_barra_progreso.pack(pady=1)

cargar_archivo_kml()

ventana.mainloop()
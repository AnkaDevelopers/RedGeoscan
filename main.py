from seleccion_de_proyecto import selec_proyect,transformar_subcarpetas, buscar_archivos_en_gps, actualizar_rutas_archivos
from extraer_token_rinex_y_descarga import extraer_token_para_descarga_rinex, descargar_rinex_en_ruta
from guardar_token_principal import crear_archivo_con_fecha_y_hora, buscar_y_leer_archivo_token
from agrupar_rinex_x_antena import crear_lista_antenas_x_rinex
from consumo_servicios import servicio_administrador_antenas
from crear_lista_antenas import insertar_datos_antenas
from calculos import calcular_antenas_mas_cercanas
from filtro_antenas_igac import filtro_antenas
from rpa_rtklib import ejecutar_rtk_para_gps
from cargar_kml import cargar_base_kml
from cargar_pos import cargar_base_pos
from token_principal import rpa_igac
from generar_log import agregar_log
from tkinter import ttk
import tkinter as tk 
import pandas as pd
import threading
import time
import os

#***************************************************************************************************************
# Variables globales y sus valores iniciales
datos_kml = None
info_proyecto = None
token_principal = None
coordenada_media_base = None
datos_kml_order = None
fecha = None
fecha_mas_un_dia = None
barra_visible = False 
lista_antenas_con_rinex = None
ruta_red_activa = None
nombre_gps = None
   
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
# Función para ejecutar la extracción del token en un hilo separado y actualizar la barra de progreso
def informe_rinex():
    insertar_datos_antenas(lista_antenas_con_rinex)
#***************************************************************************************************************
# Función para ejecutar la descarga de los archivos rinex en un hilo aparte
def ejecutar_descarga_rinex_y_actualizar_barra():
    global  lista_antenas_con_rinex, ruta_red_activa

    valor_maximo = 100
    progreso_actual = 0

    # Inicializar la barra de progreso
    barra_de_progreso(valor_maximo, progreso_actual)

    # Llamar a la función que está en otro módulo para extraer tokens
    token_extraido = threading.Event()  # Evento para controlar el estado del hilo

    def extraer_token():
        global lista_antenas_con_rinex
        nonlocal token_extraido
        
        label_estado_barra_progreso.config(text='Descargando Rinex de las antenas')
        # Ejecutar la extracción de tokens
        lista_antenas_con_rinex = descargar_rinex_en_ruta(lista_antenas_con_rinex, ruta_red_activa, nombre_gps)

        # Marcar la extracción del token como completada
        token_extraido.set()

    # Iniciar el hilo para extraer el token
    hilo_extraccion = threading.Thread(target=extraer_token)
    hilo_extraccion.start()

    # Actualizar la barra de progreso mientras el hilo está en ejecución
    def actualizar_barra():
        nonlocal progreso_actual

        if not token_extraido.is_set():
            # Incrementar el progreso para simular la actualización de la barra
            progreso_actual += 5
            if progreso_actual > valor_maximo:
                # Reiniciar la barra para simular progreso continuo
                progreso_actual = 0

            barra_de_progreso(valor_maximo, progreso_actual)

            # Reprogramar la función para actualizar la barra después de 200 ms
            ventana.after(200, actualizar_barra)
        else:
            # Cuando el hilo de extracción del token termine
            progreso_actual = valor_maximo
            barra_de_progreso(valor_maximo, progreso_actual)
            label_estado_barra_progreso.config(text='Rinex Descargados con exito')

            # Ejecutar la función para imprimir la lista de antenas con RINEX en el hilo principal
            ventana.after(0, informe_rinex)

    # Iniciar la actualización de la barra de progreso
    actualizar_barra()


#***************************************************************************************************************
# Función para imprimir la lista de antenas con RINEX después de la descarga del token
def descargar_rinex_antenas():
    print('Iniciando descarga... de los rinex')
    
    # Crear e iniciar un hilo para ejecutar la extracción del token y la barra de progreso
    hilo_descarga = threading.Thread(target=ejecutar_descarga_rinex_y_actualizar_barra)
    hilo_descarga.start()

#***************************************************************************************************************
# Función para ejecutar la extracción del token en un hilo separado y actualizar la barra de progreso
def ejecutar_descarga_y_actualizar_barra():
    global token_principal, lista_antenas_con_rinex

    valor_maximo = 100
    progreso_actual = 0

    # Inicializar la barra de progreso
    barra_de_progreso(valor_maximo, progreso_actual)

    # Llamar a la función que está en otro módulo para extraer tokens
    token_extraido = threading.Event()  # Evento para controlar el estado del hilo

    def extraer_token():
        global lista_antenas_con_rinex
        nonlocal token_extraido
        
        label_estado_barra_progreso.config(text='Capturando Tokens de descarga de las antenas.')
        # Ejecutar la extracción de tokens
        lista_antenas_con_rinex = extraer_token_para_descarga_rinex(lista_antenas_con_rinex, token_principal)

        # Marcar la extracción del token como completada
        token_extraido.set()

    # Iniciar el hilo para extraer el token
    hilo_extraccion = threading.Thread(target=extraer_token)
    hilo_extraccion.start()

    # Actualizar la barra de progreso mientras el hilo está en ejecución
    def actualizar_barra():
        nonlocal progreso_actual

        if not token_extraido.is_set():
            # Incrementar el progreso para simular la actualización de la barra
            progreso_actual += 5
            if progreso_actual > valor_maximo:
                # Reiniciar la barra para simular progreso continuo
                progreso_actual = 0

            barra_de_progreso(valor_maximo, progreso_actual)

            # Reprogramar la función para actualizar la barra después de 200 ms
            ventana.after(200, actualizar_barra)
        else:
            # Cuando el hilo de extracción del token termine
            progreso_actual = valor_maximo
            barra_de_progreso(valor_maximo, progreso_actual)
            print('Token de descarga extraído con éxito.')
            label_estado_barra_progreso.config(text='Tokens de descarga de las antenas extraídos con éxito.')

            # Ejecutar la función para imprimir la lista de antenas con RINEX en el hilo principal
            ventana.after(0, descargar_rinex_antenas)

    # Iniciar la actualización de la barra de progreso
    actualizar_barra()


#***************************************************************************************************************
# Función consumir servicio token de descarga según id RINEX de manera secuencial
def consumir_token_descarga_rinex():
    print('Iniciando consumo del token de descarga...')
    
    # Crear e iniciar un hilo para ejecutar la extracción del token y la barra de progreso
    hilo_descarga = threading.Thread(target=ejecutar_descarga_y_actualizar_barra)
    hilo_descarga.start()
    
#***************************************************************************************************************
# Función para consumir servicio y verificar si las antenas contienen datos RINEX según la fecha
def consumir_servicio_segun_fecha():
    # Variable global donde se alamcenan la lista de antenas con rinex
    global lista_antenas_con_rinex

    # Crear una base de las antenas con datos RINEX o no
    lista_antenas_con_rinex = crear_lista_antenas_x_rinex(fecha, fecha, datos_kml_order)
    
    if not lista_antenas_con_rinex:
        return label_estado_base_kml.config(text='Lista de antenas vacía.')
    
    # Validar si ninguna antena tiene datos RINEX
    if all(antena.get('has_rinex') == "False" for antena in lista_antenas_con_rinex):
        return label_estado_base_kml.config(text='No se encontraron archivos RINEX de ninguna antena.')
    
    # Contar el número de antenas con has_rinex = "True"
    numero_antenas_con_rinex = sum(antena.get('has_rinex') == True for antena in lista_antenas_con_rinex)
    
    # Mensaje en caso de que haya antenas con datos RINEX
    mensaje = f'Se encontraron resultados de RINEX en {numero_antenas_con_rinex} antenas.'
    label_estado_base_kml.config(text=mensaje)
    
    # Iniciar la extracción del token y actualizar la barra de progreso
    consumir_token_descarga_rinex()


#***************************************************************************************************************
# funcion consumir servicio y crear base de antenas
def consumir_servicio_andimistrador_antenas():
    
    # Llamamos la variable gobal donde podremos almacenar la relación de la antena y su administrador
    global datos_kml_order
    
    # este servicio me crea una base con la información de las antenas esta base que da como un archivo json con la fecha 
    servicio_administrador_antenas()
    
    # Mensaje de depuración
    print('*'*50,'\n','Carga Base de antenas con administrador','\n','*'*50)
   
    # me devuelve una lista de las antenas que pertenesen al igac y la lista de la que no ordenadas por distancia a mi coordenada base
    datos_kml_order = filtro_antenas(datos_kml_order)# Mensaje de depuración
    #print('Administrador antenas por distancia:', len(datos_kml_order), '\n', datos_kml_order,'\n','*'*100)
    
    #servicio para buscar archivos rinex segun fecha
    consumir_servicio_segun_fecha()
    

#***************************************************************************************************************
# funcion principal calcular las  antenas mas cercanas
def calcular_antenas(ruta_pos, red_activa, gps_nombre):
    
    # Llamamos la variables globales las cuales se encuentran en NONE
    global coordenada_media_base, datos_kml, datos_kml_order, fecha, fecha_mas_un_dia, ruta_red_activa, nombre_gps
    
    # Capoturamos globalmente la ruta de descarga
    ruta_red_activa = red_activa
    nombre_gps = gps_nombre
         
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
    #print('\n', 'Antenas mas cercanas 1:', len(datos_kml_order), '\n','Lista de antenas cercanas: ','\n', datos_kml_order)
    
    # Convertir DataFrame a diccionario
    datos_kml_order = datos_kml_order.to_dict(orient='records')
    
    # Llamamos la funcion para consumir un servicio que nos trae una base de informacion de las antenas de la red geodesica
    consumir_servicio_andimistrador_antenas()

#***************************************************************************************************************
# función para procesar cada archivo .pos
def imprimir_rutas_pos(info_proyecto): 
    
    # Iterar sobre los días de rastreo
    for dia, info in info_proyecto["dias_rastreos"].items():
        print(f"Día: {dia}")
        
        # Obtener la red activa del día actual
        red_activa = info.get("redActiva")
        
        # Iterar sobre las carpetas GPS en cada día
        for gps_nombre, rutas in info["subcarpetas_base"].items():
            ruta_pos = rutas.get("pos")
            
            # Verificar si existe un archivo .pos para esta carpeta GPS
            if ruta_pos and ruta_pos != 0:  # Asegurarnos de que no sea 0
                print(f"Carpeta GPS: {gps_nombre}, Archivo .pos: {ruta_pos}")
                calcular_antenas(ruta_pos, red_activa, gps_nombre)

# ***************************************************************************************************************
# Función que espera a que el token sea extraído y luego llama a imprimir_rutas_pos
def esperar_token_y_continuar():
    global token_principal, info_proyecto

    # Llamamos la función para conseguir el token
    conseguir_token_y_guardarlo()

    # Esperar hasta que se obtenga el token principal antes de continuar
    while not token_principal:
        time.sleep(1)  # Espera breve para no sobrecargar la CPU

    # Ejecutar la siguiente función en el hilo principal para interactuar con la interfaz
    ventana.after(0, lambda: imprimir_rutas_pos(info_proyecto))
    
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
        
    # *************************************************************************
    # Función para ejecutar el RPA en un hilo separado
    def ejecutar_rpa():
        
        # Llamamos la variables globales
        global token_principal, info_proyecto
        
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
    # ************************************************************************
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
    global info_proyecto, token_principal
    
    # Ejecucion de función para seleccionar el proyecto
    info_proyecto = selec_proyect()
    
    # Validacion de ruta del proyecto
    if not info_proyecto:
        return print('*'*50, '\n', 'fallo1')
    
    # Ejecucion de funcion para organizar diccionario de rutas
    info_proyecto= transformar_subcarpetas(info_proyecto)
    
    # Ejecucion de funcion para buscar las rutas de los archivos para el rtklib
    info_proyecto = buscar_archivos_en_gps(info_proyecto)

    # Ejecucion de rpa
    ejecutar_rtk_para_gps(info_proyecto)
    
    time.sleep(0.5)
    
    # Actualizamos nuevamente las rutas
    info_proyecto = actualizar_rutas_archivos(info_proyecto)
    
    # Buscamos el token principal
    token_principal = buscar_y_leer_archivo_token()
    
    # Validar si el token ya esta vencido
    if not token_principal:
        # Ejecutar el proceso de conseguir el token en un hilo separado
        hilo_token = threading.Thread(target=esperar_token_y_continuar)
        hilo_token.start()
    else:
        # Si el token a un sirve continuar con el proceso
        label_estado_barra_progreso.config(text='Token principal capturado exitosamente.')
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
    print('*'*200,'\n','Archivo KML cargado exitosamente','\n','*'*200)

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
from extraer_token_rinex_y_descarga import extraer_token_para_descarga_rinex
from agrupar_rinex_x_antena import crear_lista_antenas_x_rinex
from consumo_servicios import servicio_administrador_antenas
from crear_lista_antenas import insertar_datos_antenas
from seleccion_de_proyecto import seleccionar_carpeta
from filtro_antenas_igac import filtro_antenas_igac
from calculos import calcular_antenas_mas_cercanas
from cargar_kml import cargar_base_kml
from cargar_pos import cargar_base_pos
from token_principal import rpa_igac
from rpa_rtklib import ejecutar_rtk
from tkinter import ttk
import tkinter as tk 
import threading

#***************************************************************************************************************
# Variables globales y sus valores iniciales
rutas_proyecto = None
coordenada_media_base = None
datos_kml = None
antenas_con_administrador = None
barra_visible = False 
fecha_mas_un_dia = None
fecha = None
antenas_con_rinex = None
token_principal = None
progreso_barra = 10
paso_actual = 0  
ruta_descarga = None


#***************************************************************************************************************
# Función para limpiar las variables globales
def limpiar():
    global coordenada_media_base, datos_kml, antenas_con_administrador, barra_visible, fecha_mas_un_dia, fecha, antenas_con_rinex, token_principal, progreso_barra, paso_actual, ruta_descarga
    
    # Restablecer las variables a sus valores iniciales
    coordenada_media_base = None
    datos_kml = None
    antenas_con_administrador = None
    barra_visible = False 
    fecha_mas_un_dia = None
    fecha = None
    antenas_con_rinex = None
    token_principal = None
    progreso_barra = 10
    paso_actual = 0
    ruta_descarga = None


    print("Variables globales restablecidas a sus valores iniciales.")
#***************************************************************************************************************

# Ejecuta funcion en un segundo hilo
def iniciar_consumir_servicio_token_principal():
    hilo = threading.Thread(target=consumir_servicio_token_principal)
    hilo.start()

#***************************************************************************************************************
# funcion para imprimir variables y debugear
def imprimir():
    for antenas in antenas_con_rinex:
        print(antenas)

#***************************************************************************************************************
# Barra de progreso: incrementa cada vez que se llama
def barra_de_progreso():
    global barra_visible
    if not barra_visible:
        barra_progreso.pack(pady=10)  
        barra_visible = True
        
    # Aumenta el valor actual de la barra
    if barra_progreso['value'] < 100:  
        barra_progreso['value'] += progreso_barra
    if barra_progreso['value'] == 100:
        barra_progreso.pack_forget()
        barra_visible = False

    ventana.update_idletasks()  # Actualiza la interfaz

#***************************************************************************************************************
# Función consumir servicio token de descarga según id rinex de manera secuencial
def consumir_token_descarga_rinex():
    global ruta_descarga
    if not token_principal:
        print("segundo intento de descarga del token  principal")
        consumir_servicio_token_principal()
    else:    
        ruta = extraer_token_para_descarga_rinex(antenas_con_rinex, token_principal, fecha, barra_de_progreso)
        print("descarga completa de los archivos rinex")
        insertar_datos_antenas(tabla_antenas, antenas_con_rinex, ruta)
        print("insercion de los datos en la tabla")
# ***************************************************************************************************************
# Función consumir servicio filtro de antenas para verificar si contiene rinex según fecha
def consumir_servicio_token_principal():
    global paso_actual, token_principal
    token_principal = rpa_igac()  # Ejecuta rpa_igac en este paso
    consumir_token_descarga_rinex()   # Actualiza la barra nuevamente
    print("Descarga del token principal")
    paso_actual += 1

#***************************************************************************************************************
# funcion consumir servicio filtro de antenas para verificar si contiene rinex segun fecha
def consumir_servicio_segun_fecha():
    global antenas_con_rinex
    nombre_antenas = antenas_con_administrador
    antenas_con_rinex = crear_lista_antenas_x_rinex(fecha,fecha,nombre_antenas)
    print("validadacion de las atenas para saber cuales cuentan con rinex")
    iniciar_consumir_servicio_token_principal()

#***************************************************************************************************************
# funcion consumir servicio y crear base de antenas
def consumir_servicio_andimistrador_antenas():
    global antenas_con_administrador
    # este servicio me crea una base con la informnacion de las antenas esta base que da como un archivo json con la fecha 
    servicio_administrador_antenas()
    # me devuelve una lista de las antenas que pertenesen al igac y la lista de la que no ordenadas por distancia a mi coordenada base
    antenas_con_administrador = filtro_antenas_igac(datos_kml)
    #servicio para buscar archivos rinex segun fecha
    print("descargar base de antenas para conocer el administrador de la antena")
    consumir_servicio_segun_fecha()

#***************************************************************************************************************
# funcion principal calcular las  antenas mas cercanas
def calcular_antenas():
    global coordenada_media_base, datos_kml, fecha, fecha_mas_un_dia
    coordenada_media_base, mensaje_pos, fecha, fecha_mas_un_dia = cargar_base_pos(tabla_coordenada_media)
    label_estado_archivo_pos.config(text=mensaje_pos)
    if not coordenada_media_base:
        return
    datos_kml = calcular_antenas_mas_cercanas((coordenada_media_base['latitud'],coordenada_media_base['longitud']),datos_kml)
    print("organizacion de las antenas desde la mas cercana")
    consumir_servicio_andimistrador_antenas()

#***************************************************************************************************************
# cargar archivo kml antenas base del IGAC
def selec_proyecto():
    global rutas_proyecto
    rutas_proyecto = seleccionar_carpeta()
    ejecutar_rtk(rutas_proyecto)
#***************************************************************************************************************
# cargar archivo kml antenas base del IGAC
def cargar_archivo_kml():
    print("carga kml exito")
    global datos_kml
    datos_kml,mensaje_kml = cargar_base_kml()
    label_estado_base_kml.config(text=mensaje_kml)
    
# *****************************************ESTILOS TKINTER******************************************************
# Configuración de la ventana principal 
ventana = tk.Tk()
ventana.title("Antenas más cercanas")
ventana.geometry("800x600")

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
tabla_antenas.column("Administrador", width=100, anchor="center")   # Ajuste para el Administgrador de la antena 

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
boton_cargar_pos = tk.Button(frame_botones, text="Seleccionar Proyecto 🌍", command=selec_proyecto)
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
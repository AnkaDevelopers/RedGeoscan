from extraer_token_rinex import extraer_token_para_descarga_rinex
from agrupar_rinex_x_antena import crear_lista_antenas_x_rinex
from crear_lista_antenas import insertar_datos_antenas
from consumo_servicios import servicio_administrador_antenas
from filtro_antenas_igac import filtro_antenas_igac
from calculos import calcular_antenas_mas_cercanas
from token_principal import rpa_igac
from cargar_kml import cargar_base_kml
from cargar_pos import cargar_base_pos
from tkinter import ttk
import tkinter as tk 


#***************************************************************************************************************
# Variables globales
coordenada_media_base = None
datos_kml = None
antenas_con_administrador = None
barra_visible = False 
fecha_mas_un_dia= None
fecha = None
antenas_con_rinex = None
token_principal = None
progreso_barra = 10
paso_actual = 0  

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
        # Muestra la barra solo la primera vez
        barra_progreso.pack(pady=10)  
        barra_visible = True
    # Aumenta el valor actual de la barra
    if barra_progreso['value'] < 100:  # Limita el progreso a 100%
        barra_progreso['value'] += progreso_barra
    ventana.update_idletasks()  # Actualiza la interfaz

#***************************************************************************************************************
# Función consumir servicio token de descarga según id rinex de manera secuencial
def consumir_token_descarga_rinex():
    global barra_visible
    barra_de_progreso()
    if not token_principal:
        consumir_servicio_token_principal()
    else:    
        extraer_token_para_descarga_rinex(antenas_con_rinex, token_principal, fecha)
        barra_de_progreso()
        print('descargas finalizadas')
        insertar_datos_antenas(tabla_antenas, antenas_con_rinex)
        barra_de_progreso()
        barra_progreso.pack_forget()
        barra_visible = False
        ventana.update_idletasks()  # Actualiza la interfaz
        
# ***************************************************************************************************************
# Función consumir servicio filtro de antenas para verificar si contiene rinex según fecha
def consumir_servicio_token_principal():
    global paso_actual, token_principal

    if paso_actual == 0:
        # Paso 1: Actualizar la barra y configurar para siguiente paso
        barra_de_progreso()
        ventana.after(100, consumir_servicio_token_principal)  # Espera 100ms y continúa
        paso_actual += 1

    elif paso_actual == 1:
        # Paso 2: Ejecutar el servicio principal y configurar para siguiente paso
        token_principal = rpa_igac()  # Ejecuta rpa_igac en este paso
        barra_de_progreso()
        consumir_token_descarga_rinex()   # Actualiza la barra nuevamente
        paso_actual += 1

#***************************************************************************************************************
# funcion consumir servicio filtro de antenas para verificar si contiene rinex segun fecha
def consumir_servicio_segun_fecha():
    barra_de_progreso()
    global antenas_con_rinex
    nombre_antenas = antenas_con_administrador
    antenas_con_rinex = crear_lista_antenas_x_rinex(fecha,fecha,nombre_antenas)
    barra_de_progreso()
    consumir_servicio_token_principal()

#***************************************************************************************************************
# funcion consumir servicio y crear base de antenas
def consumir_servicio_andimistrador_antenas():
    global antenas_con_administrador
    # este servicio me crea una base con la informnacion de las antenas esta base que da como un archivo json con la fecha 
    servicio_administrador_antenas()
    # me devuelve una lista de las antenas que pertenesen al igac y la lista de la que no ordenadas por distancia a mi coordenada base
    antenas_con_administrador = filtro_antenas_igac(datos_kml)
    barra_de_progreso()
    #servicio para buscar archivos rinex segun fecha
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
    consumir_servicio_andimistrador_antenas()

#***************************************************************************************************************
# cargar archivo kml antenas base del IGAC
def cargar_archivo_kml():
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
tabla_antenas = ttk.Treeview(frame_antenas, columns=("Nombre", "Latitud", "Longitud", "Distancia"), show="headings", height=8)
tabla_antenas.heading("Nombre", text="Nombre")
tabla_antenas.heading("Latitud", text="Latitud (G° M' S\")")
tabla_antenas.heading("Longitud", text="Longitud (G° M' S\")")
tabla_antenas.heading("Distancia", text="Distancia (km)")

# Ajustar el ancho de cada columna
tabla_antenas.column("Nombre", width=100)       # Ajuste para el nombre
tabla_antenas.column("Latitud", width=150)      # Ajuste para latitud
tabla_antenas.column("Longitud", width=150)     # Ajuste para longitud
tabla_antenas.column("Distancia", width=100)  

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
# Botón para cargar archivo POS
boton_cargar_pos = tk.Button(frame_botones, text="Cargar archivo POS", command=calcular_antenas)
boton_cargar_pos.pack(side=tk.LEFT, padx=10)
# Botón para cargar archivo POS
boton_cargar_pos = tk.Button(frame_botones, text="imprimir variable", command=imprimir)
boton_cargar_pos.pack(side=tk.LEFT, padx=10)
# Barra de progreso en modo "determinate", inicialmente no visible
barra_progreso = ttk.Progressbar(ventana, orient="horizontal", mode="determinate", length=300)

cargar_archivo_kml()

ventana.mainloop()

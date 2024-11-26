from calculos import decimales_a_gms, fecha_a_semana_gps
from datetime import datetime, timedelta
import tkinter.messagebox as messagebox
from tkinter import filedialog
import numpy as np
import config  
import time

# Variables globales
msj_estado = config.msj_pos
fecha = None

#********************************************************************************************
# Función para organizar el archivo .pos
def organizar_pos(datos_pos, tabla_coordenada_media):
    
    # Verificar si los parámetros están vacíos
    if not datos_pos or not tabla_coordenada_media:
        messagebox.showinfo("Advertencia", msj_estado[4])
        return None  
    
    # Separar las coordenadas
    latitudes, longitudes, alturas = zip(*[(d[0], d[1], d[2]) for d in datos_pos])

    # Buscar la media de los datos y convertir a float estándar
    media_latitud = float(np.mean(latitudes))
    media_longitud = float(np.mean(longitudes))
    media_altura = float(np.mean(alturas))

    # Calcular la fecha media
    fechas = [datetime.strptime(d[3], "%Y/%m/%d %H:%M:%S.%f") for d in datos_pos]
    fecha_media = fechas[len(fechas) // 2]  # Fecha central (puede usarse promedio si necesario)
    
    # Calcular semana GPS y día del año solo una vez
    semana, dia = fecha_a_semana_gps(fecha_media.strftime("%Y/%m/%d %H:%M:%S.%f"))

    # Actualizar tabla con coordenada media
    lat_g, lat_m, lat_s = decimales_a_gms(media_latitud)
    lon_g, lon_m, lon_s = decimales_a_gms(media_longitud)

    for item in tabla_coordenada_media.get_children():
        tabla_coordenada_media.delete(item)
    
    # Insertar la coordenada media y la semana GPS en la tabla_coordenada_media
    tabla_coordenada_media.insert("", "end", values=(
        f"{lat_g}° {lat_m}' {lat_s:.2f}\"",
        f"{lon_g}° {lon_m}' {lon_s:.2f}\"",
        f"{media_altura:.2f} m",
        semana,
        dia 
    ))

    # Devolver resultado en un diccionario
    media_pos = {
        "latitud": media_latitud,
        "longitud": media_longitud,
        "altura": media_altura,
        "semana": semana,
        "dia": dia
    }
    
    print('*'*50,'\n','coordenada media:', media_pos)    
    return media_pos

#********************************************************************************************
# Función para procesar el archivo .pos
def procesar_pos(archivo_pos, insertar_datos):
    global fecha
    
    # Inicialización de una lista para los datos del archivo pos
    datos_pos = []
    
    with open(archivo_pos, 'r') as file:
        for line in file:
            if not line.startswith('%'):
                valores = line.split()
                try:
                    # Capturar fecha y hora
                    fecha = valores[0] + ' ' + valores[1]
                    latitud = float(valores[2])
                    longitud = float(valores[3])
                    altura = float(valores[4])

                    # Agregar coordenadas y fecha/hora al dataset
                    datos_pos.append((latitud, longitud, altura, fecha))
        
                except ValueError:
                    print(f"{msj_estado[0]}: {line.strip()}")
                    continue
    
    # Calcular coordenada media    
    media_pos = organizar_pos(datos_pos, insertar_datos)
     
    return media_pos

#********************************************************************************************
# Función para cargar el archivo .POS
def cargar_base_pos(insertar_datos, ruta_pos):
    media_pos = None
    fecha_formateada = None
    fecha_mas_24_formateada = None
    estado = msj_estado[3]
    
    # En caso de que exista una ruta en el argumento  
    if ruta_pos:
        archivo_pos = ruta_pos
    else:
        # Abrir ventana para seleccionar archivo .pos
        archivo_pos = filedialog.askopenfilename(filetypes=[("Archivos POS", "*.pos")], title="Selecciona un archivo .POS")  
        if not archivo_pos:
            estado = msj_estado[1]
            return media_pos, estado, fecha_formateada, fecha_mas_24_formateada
    
    # Procesar los datos del archivo.pos
    media_pos = procesar_pos(archivo_pos, insertar_datos)
    if not media_pos:
        estado = msj_estado[1]
        return media_pos, estado, fecha_formateada, fecha_mas_24_formateada
    
    # Calcular fechas formateadas
    fecha_nueva = datetime.strptime(fecha, "%Y/%m/%d %H:%M:%S.%f")
    fecha_formateada = fecha_nueva.strftime("%d/%m/%Y")
    fecha_mas_24 = fecha_nueva + timedelta(days=1)
    fecha_mas_24_formateada = fecha_mas_24.strftime("%d/%m/%Y")
    
    return media_pos, estado, fecha_formateada, fecha_mas_24_formateada

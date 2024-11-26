from calculos import decimales_a_gms, fecha_a_semana_gps
from datetime import datetime, timedelta
import tkinter.messagebox as messagebox
from tkinter import filedialog
import numpy as np
import config  


msj_estado = config.msj_pos
fecha = None

#********************************************************************************************
#Funcion para organizar el archivo .pos
def organizar_pos(datos_pos, tabla_coordenada_media):
    
    # Verificar si los parámetros están vacíos
    if not datos_pos or not tabla_coordenada_media:
        messagebox.showinfo("Advertencia", "El archivo .pos seleccionado no cumple con los requisitos.")
        return None  
    
        # Separar las semanas y las coordenadas
    dias, semanas, latitudes, longitudes, alturas = zip(*datos_pos)
    dia = int(np.mean(dias))
    semana = int(np.mean(semanas))
    media_latitud = np.mean(latitudes)  # Asignar a la variable global
    media_longitud = np.mean(longitudes)  # Asignar a la variable global
    media_altura = np.mean(alturas)  # Asignar a la variable global

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
    media_pos = {
        "dia": dia,
        "semana": semana,
        "latitud": float(media_latitud) ,
        "longitud": float(media_longitud ),
        "altura": float(media_altura)
    }
    return media_pos

#********************************************************************************************
#Funcion para procesar el archivo .pos
def procesar_pos(archivo_pos, insertar_datos):
    global fecha
    datos_pos = []
    with open(archivo_pos, 'r') as file:
        for line in file:
            if not line.startswith('%'):
                valores = line.split()
                try:
                    # Capturar fecha y hora
                    fecha = valores[0] + ' ' + valores[1]
                    # Calcular la semana GPS usando la nueva función
                    semana_gps, dia_del_anio = fecha_a_semana_gps(fecha)
                    latitud = float(valores[2])
                    longitud = float(valores[3])
                    altura = float(valores[4])
                    # Incluir epoca y dia del año en los datos
                    datos_pos.append((dia_del_anio, semana_gps, latitud, longitud, altura)) 
                except ValueError:
                    print(f"{msj_estado[0]}: {line.strip()}")
                    continue
    #calculamos coordenada media base
    media_pos = organizar_pos(datos_pos, insertar_datos) 
    return media_pos

#********************************************************************************************
# Función para cargar el archivo .POS
def cargar_base_pos(insertar_datos, ruta_pos):
    media_pos = None
    fecha_formateada = None
    fecha_mas_24_formateada = None
    estado = msj_estado[3]
    
    if not ruta_pos: 
        # Abre una ventana para seleccionar un archivo .pos
        archivo_pos = filedialog.askopenfilename(
          filetypes=[("Archivos POS", "*.pos")], title="Selecciona un archivo .POS"
     )
    else:
        archivo_pos = ruta_pos
    
    # Si se cierra  la ventana sin seleccionar archivo, se muestra un mensaje de salida de la funcion
    if not archivo_pos:
        estado = msj_estado[1]
        return media_pos, estado ,fecha_formateada, fecha_mas_24_formateada
    
    # Se procesan los satos del archivo.pos
    media_pos = procesar_pos(archivo_pos, insertar_datos)
    if not media_pos:
        estado = msj_estado[1]
        return media_pos, estado ,fecha_formateada, fecha_mas_24_formateada
    
    # los datos estan cargados
    # Convertir la cadena a un objeto datetime, solo con la fecha
    fecha_nueva = datetime.strptime(fecha, "%Y/%m/%d %H:%M:%S.%f")
    fecha_formateada = fecha_nueva.strftime("%d/%m/%Y")
    # Crear una nueva fecha con un día más
    fecha_mas_24 = fecha_nueva + timedelta(days=1)
    fecha_mas_24_formateada = fecha_mas_24.strftime("%d/%m/%Y")
    return media_pos, estado ,fecha_formateada, fecha_mas_24_formateada
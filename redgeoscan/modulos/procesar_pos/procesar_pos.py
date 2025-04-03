# Importar modulos redgeoscan
from redgeoscan.utils.fecha_sem_gps import fecha_a_semana_gps
from redgeoscan.utils.decimales_a_gps import decimales_a_gms

# Importaciones adicionales
from datetime import datetime, timedelta
import numpy as np

#********************************************************************************************
# Función para procesar el archivo .pos
def procesar_pos(archivo_pos):
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

                    # Agregar coordenadas y fecha/hora al dataset
                    datos_pos.append((latitud, longitud,fecha))
        
                except ValueError:
                    print(f"error")
                    continue
    
    # Calcular coordenada media    
    media_pos = organizar_pos(datos_pos)
     
    return media_pos

#********************************************************************************************
# Función para organizar el archivo .pos
def organizar_pos(datos_pos):
    

    # Separar las coordenadas
    latitudes, longitudes = zip(*[(d[0], d[1]) for d in datos_pos])

    # Buscar la media de los datos y convertir a float estándar
    media_latitud = float(np.mean(latitudes))
    media_longitud = float(np.mean(longitudes))

    # Calcular la fecha media
    fechas = [datetime.strptime(d[2], "%Y/%m/%d %H:%M:%S.%f") for d in datos_pos]
    fecha_media = fechas[len(fechas) // 2]  # Fecha central (puede usarse promedio si necesario)
    fecha_ensayo = fecha_media.strftime("%Y/%m/%d %H:%M:%S.%f")


    # Calcular semana GPS y día del año solo una vez
    semana, dia = fecha_a_semana_gps(fecha_media.strftime("%Y/%m/%d %H:%M:%S.%f"))

    # Actualizar tabla con coordenada media
    lat_g, lat_m, lat_s = decimales_a_gms(media_latitud)
    lon_g, lon_m, lon_s = decimales_a_gms(media_longitud)

    # Devolver resultado en un diccionario
    media_pos = {
        "latitud": f"{lat_g} {lat_m} {lat_s}",
        "longitud": f"{lon_g} {lon_m} {lon_s}",
        "fecha": fecha_ensayo,
        "semana": semana,
        "dia": dia
    }
       
    return media_pos
import numpy as np
import pandas as pd  
from datetime import datetime

#********************************************************************************************
# Función para calcular la distancia en kilómetros entre dos puntos en la superficie de la Tierra usando la fórmula del coseno
def calcular_distancia(lat1, lon1, lat2, lon2):
    # Convertir las coordenadas de grados a radianes
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    # Usar la fórmula del coseno
    distancia = np.arccos(np.sin(lat1_rad) * np.sin(lat2_rad) +
                          np.cos(lat1_rad) * np.cos(lat2_rad) * 
                          np.cos(lon2_rad - lon1_rad)) * 6371  # Radio de la Tierra en km
    return distancia

#********************************************************************************************
# Convertir a grados, minutos y segundos con redondeo en segundos
def decimales_a_gms(decimal):
    grados = int(decimal)
    minutos_decimales = abs((decimal - grados) * 60)
    minutos = int(minutos_decimales)
    segundos = round((minutos_decimales - minutos) * 60, 2)  # Redondear a 4 decimales
    return grados, minutos, segundos


#********************************************************************************************
# funcion para convertir una fecha en semana gps y en dia del año
def fecha_a_semana_gps(fecha_str):
    # Definir la fecha de inicio de la época GPS
    epoca_gps = datetime(1980, 1, 6)

    # Convertir la fecha de entrada a un objeto datetime
    fecha = datetime.strptime(fecha_str, "%Y/%m/%d %H:%M:%S.%f")
    # Calcular la diferencia en días
    diferencia = fecha - epoca_gps
    dias_gps = diferencia.days  # Obtener días completos
    semanas_gps = dias_gps // 7  # Obtener semanas completas

    # Obtener el día del año
    dia_del_año = fecha.timetuple().tm_yday  # Día del año

    return semanas_gps, dia_del_año


#********************************************************************************************
# Función para calcular las antenas más cercanas que cumplen con los criterios
def calcular_antenas_mas_cercanas(punto_central, datos_kml):
    # Calcular la distancia de cada antena al punto central
    datos_kml['Distancia'] = datos_kml.apply(
        lambda row: calcular_distancia(
            punto_central[0], punto_central[1], row['Latitud (Decimal)'], row['Longitud (Decimal)']
        ),
        axis=1
    )
    # Ordenar las antenas por distancia
    datos_ordenados = datos_kml.sort_values(by='Distancia')
    return datos_ordenados

#********************************************************************************************
#Convierte una fecha en formato 'dd/mm/yyyy' a 'ddmmyy'.
def formatear_fecha(fecha):
    fecha_obj = datetime.strptime(fecha, '%d/%m/%Y')
    return fecha_obj.strftime('%d%m%y')
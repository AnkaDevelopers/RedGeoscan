import numpy as np

#********************************************************************************************
# Función para convertir coordenadas de DMS (grados, minutos, segundos) a decimal
def dms_a_decimal(dms):
    try:
        # Separar los componentes de grados, minutos y segundos
        partes = dms.split()
        grados = float(partes[0])
        minutos = float(partes[1]) / 60
        segundos = float(partes[2]) / 3600
        
        # Si los grados son negativos, toda la coordenada debe ser negativa
        if grados < 0:
            return grados - minutos - segundos
        else:
            return grados + minutos + segundos
    except Exception as e:
        print(f"Error al convertir DMS a decimal: {e}")
        return None  # Retorna None si hay un error en la conversión

#********************************************************************************************
# Función para calcular la distancia en kilómetros entre dos puntos en la superficie de la Tierra usando la fórmula del coseno
def calcular_distancia(lat1, lon1, lat2, lon2):
    try:
        # Convertir las coordenadas de DMS a decimal si es necesario
        lat1 = dms_a_decimal(lat1) if isinstance(lat1, str) else float(lat1)
        lon1 = dms_a_decimal(lon1) if isinstance(lon1, str) else float(lon1)
        lat2 = dms_a_decimal(lat2) if isinstance(lat2, str) else float(lat2)
        lon2 = dms_a_decimal(lon2) if isinstance(lon2, str) else float(lon2)
        
        # Validar que las coordenadas sean numéricas
        if None in [lat1, lon1, lat2, lon2]:
            raise ValueError("Las coordenadas no son válidas después de la conversión a decimal.")

        # Convertir las coordenadas de grados a radianes
        lat1_rad = np.radians(lat1)
        lon1_rad = np.radians(lon1)
        lat2_rad = np.radians(lat2)
        lon2_rad = np.radians(lon2)
        
        # Usar la fórmula del coseno para calcular la distancia
        distancia = np.arccos(
            np.sin(lat1_rad) * np.sin(lat2_rad) +
            np.cos(lat1_rad) * np.cos(lat2_rad) *
            np.cos(lon2_rad - lon1_rad)
        ) * 6371  # Radio de la Tierra en km
        
        return distancia
    except Exception as e:
        print(f"Error al calcular la distancia: {e}")
        return float('inf')  # Devuelve infinito si hay un error para que se descarte el punto

#********************************************************************************************
# Función para calcular las antenas más cercanas que cumplen con los criterios
def calcular_antenas_mas_cercanas(punto_central, datos_kml, radio):
    
    try:
        # Validar que el punto central tenga valores válidos
        if not punto_central or len(punto_central) != 2:
            raise ValueError("El punto central debe contener latitud y longitud en formato decimal o DMS.")

        # Validar que los datos KML contengan las columnas necesarias
        if 'Latitud (Decimal)' not in datos_kml.columns or 'Longitud (Decimal)' not in datos_kml.columns:
            raise ValueError("El archivo KML no contiene las columnas requeridas: 'Latitud (Decimal)' y 'Longitud (Decimal)'.")

        # Calcular la distancia de cada antena al punto central
        datos_kml['Distancia'] = datos_kml.apply(
            lambda row: calcular_distancia(
                punto_central[0], punto_central[1], row['Latitud (Decimal)'], row['Longitud (Decimal)']
            ),
            axis=1
        )
        
        # Filtrar antenas con distancia <= 150 km
        datos_filtrados = datos_kml[datos_kml['Distancia'] <= radio]
        
        # Ordenar las antenas filtradas por distancia
        datos_ordenados = datos_filtrados.sort_values(by='Distancia')
        
        # Eliminar la columna 'KML_STYLE' si existe
        if 'KML_STYLE' in datos_ordenados.columns:
            datos_ordenados = datos_ordenados.drop(columns=['KML_STYLE'])
        
        # Agregar una nueva columna 'Tiempo de Rastreo' con la fórmula proporcionada
        datos_ordenados['Tiempo de Rastreo (h)'] = datos_ordenados['Distancia'].apply(
            lambda distancia: round((65 + (3 * (int(distancia) - 10))) / 60,1)
        )

        datos_ordenados = datos_ordenados.to_dict(orient='records') 
        return datos_ordenados

    except Exception as e:
        print(f"Error al calcular antenas más cercanas: {e}")
        return None  # Retorna None si ocurre un error


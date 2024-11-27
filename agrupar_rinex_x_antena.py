from consumo_servicios import servicio_comprobar_rinex_por_fecha
import time
import pandas as pd

def crear_lista_antenas_x_rinex(fecha_inicial, fecha_final, datos_antenas):
    # Crear nuevas columnas en el DataFrame para indicar si tiene datos RINEX
    datos_antenas['has_rinex'] = False
    datos_antenas['rinex_data'] = None

    # Contador para las antenas con datos RINEX
    contador_rinex = 0

    # Iterar sobre cada fila del DataFrame
    for index, fila in datos_antenas.iterrows():
        
        # Detener el proceso si ya se alcanzaron 8 antenas con datos RINEX
        if contador_rinex >= 2:
            print('*' * 100, '\n', "Se alcanzó el límite de 8 antenas con datos RINEX.")
            break
        
        # Extraer el nombre de la antena
        nombre_antena = fila['NAME']

        # Intentar llamar al servicio
        try:
            rinex_data = servicio_comprobar_rinex_por_fecha(fecha_inicial, fecha_final, nombre_antena)
            
        except Exception as e:
            print(f"Error al procesar antena {nombre_antena}: {e}")
            rinex_data = None

        # Actualizar el DataFrame con los resultados
        if rinex_data:
            # Marcar como True y agregar los datos RINEX
            datos_antenas.at[index, 'has_rinex'] = True
            datos_antenas.at[index, 'rinex_data'] = rinex_data
            contador_rinex += 1  # Incrementar el contador para las antenas con datos RINEX

        # Pausa para evitar saturar el servicio
        time.sleep(0.1)

    # Retornar el DataFrame completo
    return datos_antenas

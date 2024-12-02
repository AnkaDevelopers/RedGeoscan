from consumo_servicios import servicio_comprobar_rinex_por_fecha
import time


def crear_lista_antenas_x_rinex(fecha_inicial, fecha_final, datos_antenas):
    
    
    if not datos_antenas:
        return print('vacio')

    # Agregar claves nuevas para almacenar información RINEX
    for antena in datos_antenas:
        antena['has_rinex'] = False
        antena['rinex_data'] = None

    # Contador para las antenas con datos RINEX
    contador_rinex = 0

    # Iterar sobre cada antena
    for antena in datos_antenas:
        # Detener el proceso si ya se alcanzaron 8 antenas con datos RINEX
        if contador_rinex >= 8:
            print('*' * 100, '\n', "Se alcanzó el límite de 8 antenas con datos RINEX.")
            break

        # Extraer el nombre de la antena
        nombre_antena = antena.get('NAME', '')

        # Intentar llamar al servicio
        try:
            rinex_data = servicio_comprobar_rinex_por_fecha(fecha_inicial, fecha_final, nombre_antena)
        except Exception as e:
            print(f"Error al procesar antena {nombre_antena}: {e}")
            rinex_data = None

        # Actualizar la antena con los resultados
        if rinex_data:
            antena['has_rinex'] = True
            antena['rinex_data'] = rinex_data
            contador_rinex += 1  # Incrementar el contador para las antenas con datos RINEX

        # Pausa para evitar saturar el servicio
        time.sleep(0.1)

    # Retornar la lista actualizada
    return datos_antenas


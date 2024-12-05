from consumo_servicios import servicio_comprobar_rinex_por_fecha, descargar_archivo_sirgas
import time


def crear_lista_antenas_x_rinex(fecha_inicial, fecha_final, datos_antenas):

    # Agregar claves nuevas para almacenar información RINEX
    for antena in datos_antenas:
        antena['has_rinex'] = False
        antena['rinex_data'] = None
        antena['estado_coordenada'] = 'ORDEN 1'
        antena['coordenada'] = None

    # Contador para las antenas con datos RINEX
    contador_rinex = 0
    limite_antenas = 8  # Límite de antenas con datos RINEX
    
    # Iterar sobre cada antena
    for antena in datos_antenas:

        # Verificar si ya se alcanzó el límite de antenas con datos RINEX
        if contador_rinex >= limite_antenas:
            print('*' * 100, '\n', "Se alcanzó el límite de 8 antenas con datos RINEX.")
            break

        # Ejecutar la función que consume un servicio y recibe el nombre de cada antena
        coordenada = descargar_archivo_sirgas(antena['NAME'])
        
        if coordenada == False:
            antena['estado_coordenada'] = 'ORDEN 1'
            antena['coordenada'] = 'None'
        else:
            antena['estado_coordenada'] = 'ORDEN 0'
            antena['coordenada'] = coordenada

        # Mostrar información sobre la antena
        print('Antena:', antena['NAME'], '\n', 'Coordenada:', antena['coordenada'])
        
        # Intentar llamar al servicio para comprobar datos RINEX
        nombre_antena = antena.get('NAME', '')
        
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

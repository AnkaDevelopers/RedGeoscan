from consumo_servicios import servicio_comprobar_rinex_por_fecha
import time

def crear_lista_antenas_x_rinex(fecha_inicial, fecha_final, datos_antenas):
    # Lista para almacenar antenas con datos RINEX y sin datos RINEX
    antenas_con_rinex = []
    antenas_sin_rinex = []

    # Iterar sobre cada antena en la lista de datos
    for datos in datos_antenas:
        # Extraer el nombre de la antena
        nombre_antena = datos['NAME']

        # Llamar al servicio para obtener los datos RINEX asociados
        rinex_data = servicio_comprobar_rinex_por_fecha(fecha_inicial, fecha_final, nombre_antena)
        time.sleep(0.1)
        # Verificar si se encontraron datos RINEX
        if rinex_data:
            # Vincular los datos RINEX obtenidos con el diccionario de la antena actual
            datos['rinex_data'] = rinex_data
            # Agregar la antena con datos RINEX a la lista final
            antenas_con_rinex.append(datos)
            if len(antenas_con_rinex) == 2:
                print('Procesamiento completado.')
                return antenas_con_rinex
        else:
            # Si no hay datos RINEX, agregar a la lista de antenas sin datos
            antenas_sin_rinex.append(datos)

    return antenas_con_rinex


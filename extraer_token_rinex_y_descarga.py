from consumo_servicios import consumir_servicio_descarga
import time

def extraer_token_para_descarga_rinex(dataSet_antenas, token_principal, callback_progreso=None):
    
    # Convertir el DataFrame a un diccionario
    dataSet_dict = dataSet_antenas.to_dict(orient='records')

    # Recorrer cada antena en el dataset
    for antena in dataSet_dict:
        
        # Recorrer cada archivo RINEX y consumir el servicio
        for archivo_rinex in antena['rinex_data']:
            id_rinex = archivo_rinex['ID_RINEX']

            # Consumir el servicio para obtener el token
            respuesta = consumir_servicio_descarga(id_rinex, token_principal)

            # Si hay una respuesta válida, agregar el token al archivo RINEX
            if respuesta:
                archivo_rinex['TOKEN'] = respuesta
            else:
                print(f"No se pudo obtener token para {archivo_rinex['NOMBRE_ARCHIVO']} (ID: {id_rinex})")

            # Llamar al callback de progreso si está definido
            if callback_progreso:
                callback_progreso()

            # Pausa para evitar saturar el servicio
            time.sleep(0.5)

    return dataSet_dict

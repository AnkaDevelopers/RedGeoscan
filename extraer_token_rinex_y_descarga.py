from consumo_servicios import consumir_servicio_descarga, descargar_archivo
import time
import os

ruta_carpeta = None

def extraer_token_para_descarga_rinex(cargo_proyecto, ruta_carpeta_proyecto, antenas, token_principal, fecha, callback_progreso=None):
    global ruta_carpeta
    
    # Validamos si la interaccion fue cargando proyecto o directamente el archivo .pos
    if cargo_proyecto == True:
        ruta_carpeta = ruta_carpeta_proyecto # C:\Users\camil-code\Desktop\AGRADO-RPA-RTKLIB
    
    # Filtrar solo las antenas con has_rinex == True
    antenas_filtradas = antenas[antenas['has_rinex'] == True]

    # Longitud total de las antenas filtradas para la barra de progreso
    longitud_total = len(antenas_filtradas)
    progreso_actual = 0  # Inicializar el progreso actual

    print("Comenzando la descarga de tokens RINEX...")

    for index, fila in antenas_filtradas.iterrows():
        
        # Extraemos el nombre de la antena
        nombre_antena = fila['NAME']
        
        # Extraemos la distancia de la antena
        distancia = round(fila['Distancia'], 1)
        
        # Extraemos el nombre del administrador de la antena
        administrador = fila['ADMINISTRADOR']
        
        # Extraemos la información de rinex_data
        rinex_data = fila['rinex_data']
        
        # Validar que rinex_data sea una lista válida
        if not isinstance(rinex_data, list):
            print(f"Advertencia: rinex_data no es una lista válida para la antena {nombre_antena}.")
            continue

        # Creamos el nombre de la subcarpeta
        subcarpeta = f"{index + 1}-{nombre_antena}-{distancia}-km"

        for archivo_rinex in rinex_data:
            
            # Validar que el archivo RINEX tenga un ID válido
            id_rinex = archivo_rinex.get('ID_RINEX')
            if not id_rinex:
                print(f"Advertencia: No se encontró ID_RINEX en el archivo {archivo_rinex.get('NOMBRE_ARCHIVO', 'desconocido')}.")
                continue
            
            # Extraer el nombre del archivo RINEX
            nombre_archivo = archivo_rinex.get('NOMBRE_ARCHIVO', 'desconocido')

            # Consumir servicio para obtener el token
            respuesta = consumir_servicio_descarga(id_rinex, token_principal)
            time.sleep(0.5)

            # Validar la respuesta del servicio
            if respuesta:
                # Agregar el token al archivo RINEX
                archivo_rinex['TOKEN'] = respuesta
                
                # Descargar el archivo usando el token
                ruta_carpeta = descargar_archivo(
                    token=respuesta,
                    subcarpeta=subcarpeta,
                    nombre_archivo=nombre_archivo,
                    fecha=fecha,
                    administrador=administrador,
                    ruta_carpeta_inicial=ruta_carpeta,
                    validacion = cargo_proyecto
                )
                print(f"Descarga exitosa para {nombre_antena} - Archivo: {nombre_archivo}")
            else:
                print(f"No se pudo descargar el token para {nombre_antena} - Archivo: {nombre_archivo}")

        # Actualizar el progreso
        progreso_actual += 1
        if callback_progreso:
            callback_progreso(longitud_total, progreso_actual)

    print("Proceso de descarga completado.")
    return ruta_carpeta

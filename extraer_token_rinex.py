from consumo_servicios import consumir_servicio_descarga, descargar_archivo
import time

ruta_carpeta = None

def extraer_token_para_descarga_rinex(antenas, token_principal,fecha,callback_progreso=None):
    global ruta_carpeta
    # Lista para almacenar las asociaciones de descarga para cada antena y archivo RINEX
    longitud = len(antenas)
    
    if token_principal:
        print('si hay token')
    
    for i in range(longitud):
        
        
        # numeracion antenas mas cercanas    
        orden = i + 1
        
        # datos de la antena extraidos del diccioanrio
        nombre_antena = antenas[i]['NAME'] #Extraemos el nombre de la antena
        distancia = round(antenas[i]['Distancia'],1) #Extraemos la distancia de la antena
        administrador = antenas[i]['ADMINISTRADOR']
        nombre_distancia = f"{orden}-{nombre_antena}-{distancia}" # Crea la variable en el formato "NOMBRE-DISTANCIA"  
        longitud_rinex_data_antena = 0      
        longitud_rinex_data_antena = len(antenas[i]['rinex_data'])
        
        for s in range(longitud_rinex_data_antena):
            
            # Extrae el nombre del archivo Rinex y el ID del archivo RINEX
            nombre_archivo = antenas[i]['rinex_data'][s]['NOMBRE_ARCHIVO']
            id_rinex = antenas[i]['rinex_data'][s]['ID_RINEX']
            
            # Llama al servicio para descargar usando el id_rinex
            respuesta = consumir_servicio_descarga(id_rinex, token_principal)
            time.sleep(0.5)
            if respuesta:
                ruta = descargar_archivo(respuesta, nombre_distancia, nombre_archivo, fecha, administrador, ruta_carpeta)
                time.sleep(0.5)               
                print('descarga exitosa:', nombre_antena )
                ruta_carpeta = ruta
            if not respuesta:
                print('no hubo respuesta')
                print('nombre: ', nombre_archivo ,'id:',id_rinex)
                continue
        # Llama al callback de progreso si está definido
        if callback_progreso:
            callback_progreso()
    return ruta_carpeta
from consumo_servicios import consumir_servicio_descarga, descargar_archivo
import time
import os


def extraer_token_para_descarga_rinex(lista_antenas_con_rinex, token_principal):
    
    global token_pinci
    
    token_pinci = token_principal
    
    # Iterar sobre cada antena en la lista
    for antena in lista_antenas_con_rinex:
        if antena['has_rinex'] == True and antena['rinex_data'] is not None:
            
            # Iterar sobre los datos RINEX de la antena
            for info_rinex in antena['rinex_data']:

                # Consumir servicio para obtener el token de descarga
                time.sleep(0.5)
                token_descarga = consumir_servicio_descarga(info_rinex['ID_RINEX'], token_principal)
                
                if not token_descarga:
                    print('No se encontró el token para el archivo:', info_rinex['NOMBRE_ARCHIVO'], 'con ID:', info_rinex['ID_RINEX'])
                    continue  

                # Agregar el token de descarga al archivo RINEX
                info_rinex['TOKEN_DESCARGA'] = token_descarga

    return lista_antenas_con_rinex


def descargar_rinex_en_ruta(lista_antenas_con_rinex, ruta_red_activa, nombre_gps):
    
    ruta_red_activa_gps = os.path.join(ruta_red_activa,nombre_gps)
    
    # Iterar sobre cada antena en la lista
    for antena in lista_antenas_con_rinex:
        
        administrador = antena["ADMINISTRADOR"]
        sub_carpeta = antena["NAME"]
        
        if antena['has_rinex'] == True and antena['rinex_data'] is not None:
        
            # Iterar sobre los datos RINEX de la antena
            for info_rinex in antena['rinex_data']:

                token = info_rinex['TOKEN_DESCARGA']
                nombre_archivo = info_rinex["NOMBRE_ARCHIVO"]
                
                # Consumir servicio para obtener el token de descarga
                time.sleep(0.5)
                # Retorna True o False segun el status
                respuesta = descargar_archivo(token,ruta_red_activa_gps,administrador,sub_carpeta,nombre_archivo)
                
                if respuesta == False:
                    print('No se descargo el archivo:', info_rinex['NOMBRE_ARCHIVO'], 'con ID:', info_rinex['ID_RINEX'])
                    info_rinex['DESCARGO'] = respuesta
                    continue 
                if respuesta == True:
                    info_rinex['DESCARGO'] = respuesta
                    continue
    
    return lista_antenas_con_rinex
    
    

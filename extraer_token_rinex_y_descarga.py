from consumo_servicios import consumir_servicio_descarga, descargar_archivo
import time
import os



def extraer_token_para_descarga_rinex(lista_antenas_con_rinex):
    
    for antenas in lista_antenas_con_rinex:
        
        if antenas['has_rinex'] == True and antenas['rinex_data'] != None:
            
            for info_rinex in antenas['rinex_data']:
                print(info_rinex['NOMBRE_ARCHIVO'])
                print(info_rinex['ID_RINEX'])
                token_descarga = consumir_servicio_descarga(info_rinex['ID_RINEX'])
                
                if not token_descarga:
                    print('no se encontro el token del archivo: ', info_rinex['NOMBRE_ARCHIVO'], ' con id: ',info_rinex['ID_RINEX'] )
                    break
                info_rinex = ['TOKEN_DESCARGA'] = token_descarga
        
    return 


def token_principal():
        token_principal_txt = [archivo for archivo in os.listdir() if archivo.startswith("*token_principal") and archivo.endswith(".txt")]
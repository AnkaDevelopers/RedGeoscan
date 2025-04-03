# Importar modulos redgeoscan
from redgeoscan.modulos.procesar_pos.procesar_pos import procesar_pos

# Importar modulos de monitor
from monitor.log.log import agregar_log

def procesar_rutas_pos(diccionario):

    try:
        # Iterar sobre los días de rastreos
        for dia, info_dia in diccionario.get("dias_rastreos", {}).items():
            
            # Verificar la existencia de subcarpetas en el día
            base_subcarpetas = info_dia.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})
            for gps_nombre, gps_info in base_subcarpetas.items():
                # Verificar si hay una ruta 'pos' en los archivos
                ruta_pos = gps_info.get("archivos", {}).get("pos")
                if ruta_pos:
                    agregar_log(f"Procesando archivo POS para {gps_nombre} en el día {dia}: {ruta_pos}")
                    
                    # Usar procesar_pos para procesar la ruta del archivo .pos
                    informacion_pos = procesar_pos(ruta_pos)
                    agregar_log(f"coordenada media: {informacion_pos}" ) 
                    
                    if informacion_pos:
                        # Agregar la información media al diccionario
                        gps_info["informacion_pos"] = informacion_pos
                        agregar_log(f"Información media POS agregada para {gps_nombre} en el día {dia}.")
                    else:
                        agregar_log(f"Error al procesar archivo POS para {gps_nombre} en el día {dia}.")
                        
        return None, diccionario
    
    except Exception as e:
        
        msj_depuracion = f"Error al procesar rutas POS: {e}"
        return msj_depuracion, None  

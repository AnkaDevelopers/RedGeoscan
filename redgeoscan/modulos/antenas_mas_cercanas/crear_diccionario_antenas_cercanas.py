# Importar modulos redgeoscan
from redgeoscan.utils.calcular_antenas_cercanas import calcular_antenas_mas_cercanas

# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import time

#**************************************************************************************************
def crear_diccionario_con_antenas_mas_cercanas(diccionario, kml, radio):
 
    try:
        # Registrar inicio del procesamiento
        agregar_log("Iniciando el procesamiento del diccionario para antenas más cercanas......")
        
        # Iterar sobre los días de rastreo en el diccionario
        for dia, info_dia in diccionario.get("dias_rastreos", {}).items():
            # Registrar el día en el log
            agregar_log(f"Procesando día de rastreo: {dia}")
            
            # Acceder a las subcarpetas de Base
            base_subcarpetas = info_dia.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})
            
            # Iterar sobre cada subcarpeta GPS
            for gps_nombre, gps_info in base_subcarpetas.items():
                # Obtener la información POS
                informacion_pos = gps_info.get("informacion_pos", {})
                
                # Extraer latitud y longitud si existen
                latitud = informacion_pos.get("latitud")
                longitud = informacion_pos.get("longitud")
                
                if latitud and longitud:
                    
                    # Calcular las antenas más cercanas
                    antenas_cercanas = calcular_antenas_mas_cercanas((latitud, longitud), kml, radio)
                    
                    # Agregar las antenas cercanas al diccionario bajo el GPS actual
                    gps_info["antenas_cercanas"] = antenas_cercanas
                    
                    # Registrar las antenas cercanas en el log
                    agregar_log(f"Antenas cercanas para {gps_nombre}:\n \t\t      {antenas_cercanas}")
                else:
                    mensaje = f"GPS: {gps_nombre} - No se encontró información de latitud o longitud."
                    agregar_log(mensaje)
        
        # Registrar fin del procesamiento
        agregar_log("Procesamiento del diccionario completado con éxito.")
        
        # Retorna el diccionario actualizado con las antenas cercanas
        return None, diccionario  

    except Exception as e:
        
        msj_depuracion = f"Error al procesar el diccionario: {e}"
        return msj_depuracion, None 

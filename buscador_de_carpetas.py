from calculos import formatear_fecha
import config
import os

msj_buscardor = config.msj_buscador_carpetas

#**************************************************************************************************************************************************
# Verifica si una ruta existe
def validar_ruta(ruta):
    return os.path.exists(ruta)

#**************************************************************************************************************************************************
# Función principal que busca la carpeta 'RED ACTIVA' basada en la estructura de carpetas y la fecha proporcionada.
def buscar_y_crear_carpeta(origen, fecha):
    
    # Verificar si el directorio de origen existe
    if not validar_ruta(origen):
        return print('*'*50,'\n',msj_buscardor[0],'\n', origen)
        
    # Buscar carpeta '6. TOPOGRAFIA'
    topografia_path = buscar_carpeta_en_estructura(origen, "6. topografia")
    
    # Validacion de directorio '6. TOPOGRAFIA' en ruta actual
    if not topografia_path:
        return print('*'*50,'\n',msj_buscardor[1],'\n',origen)

    # Buscar carpeta 'RASTREOS' dentro de '6. TOPOGRAFIA'
    rastreos_path = buscar_carpeta_en_estructura(topografia_path, "rastreos")
    
    # Validacion de directirio 'RASTREOS' en ruta actual 
    if not rastreos_path:
        return print('*'*50,'\n',msj_buscardor[2],'\n',topografia_path)

    # Salida del componente Seleccion_de_proyecto.py
    if  not fecha:
        print('*'*50,'\n',msj_buscardor[4],'\n',rastreos_path)
        return rastreos_path
        
    # Convertir la fecha al formato 'ddmmyy' desde 'dd/mm/yyyy'
    fecha_formateada = formatear_fecha(fecha)
    
    # Buscar carpeta con nombre de fecha en Directorio 'RASTREOS'
    fecha_path = buscar_carpeta_en_estructura(rastreos_path, fecha_formateada)
    
    # Validación de carpeta con nombre en formato fecha(ddmmyyyy) en la ruta actual
    if not fecha_path:
        return print('*'*50,'\n',msj_buscardor[5],'\n',rastreos_path)

    # Buscar 'RED ACTIVA' dentro de la carpeta de la fecha
    red_activa_path = buscar_carpeta_en_estructura(fecha_path, "red activa")
    
    # Validación de carpeteta'RED ACTIVA' en la ruta actual
    if not red_activa_path:
        return print('*'*50,'\n',msj_buscardor[6],'\n',fecha_path)
    
    # Mensaje de depuración ruta final
    print('*'*50,'\n',msj_buscardor[7],'\n',red_activa_path,'\n','*'*50)
    return red_activa_path

#**************************************************************************************************************************************************
# Busca una carpeta específica dentro de una estructura de carpetas de forma recursiva.
def buscar_carpeta_en_estructura(origen, nombre_carpeta):

    for root, dirs, _ in os.walk(origen):
        
        # Información de depuración
        print('*'*50,'\n',msj_buscardor[8],'\n',root) 
        
        # Normalizar nombres de carpetas
        dirs_normalized = [d.lower() for d in dirs]

        # Verificar si alguna carpeta coincide con el nombre buscado
        if any(nombre_carpeta in d for d in dirs_normalized):
            for d in dirs:
                if nombre_carpeta in d.lower():
                    return os.path.join(root, d)
                
    return None

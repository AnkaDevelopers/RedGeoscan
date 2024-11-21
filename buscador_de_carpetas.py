from calculos import formatear_fecha
import os

#**************************************************************************************************************************************************
# Verifica si una ruta existe
def validar_ruta(ruta):
    return os.path.exists(ruta)

#**************************************************************************************************************************************************
# Función principal que busca la carpeta 'RED ACTIVA' basada en la estructura de carpetas y la fecha proporcionada.
def buscar_y_crear_carpeta(origen, fecha):

    # Verificar si el directorio de origen existe
    if not validar_ruta(origen):
        print(f"El origen {origen} no existe.")
        return

    # Buscar '6. TOPOGRAFIA'
    topografia_path = buscar_carpeta_en_estructura(origen, "6. topografia")
    if not topografia_path:
        print("Carpeta '6. TOPOGRAFIA' no encontrada.")
        return 

    # Buscar 'RASTREOS' dentro de '6. TOPOGRAFIA'
    rastreos_path = buscar_carpeta_en_estructura(topografia_path, "rastreos")
    if not rastreos_path:
        print("Carpeta 'RASTREOS' no encontrada.")
        return 

    if  not fecha:
        print('ruta hasta rastreos',rastreos_path)
        return rastreos_path
        
    # Convertir la fecha al formato 'ddmmyy' desde 'dd/mm/yyyy'
    fecha_formateada = formatear_fecha(fecha)
    
    # Buscar carpeta con la fecha en 'RASTREOS'
    fecha_path = buscar_carpeta_en_estructura(rastreos_path, fecha_formateada)
    if not fecha_path:
        print(f"Carpeta con la fecha {fecha_formateada} no encontrada.")
        return

    # Buscar 'RED ACTIVA' dentro de la carpeta de la fecha
    red_activa_path = buscar_carpeta_en_estructura(fecha_path, "red activa")
    if not red_activa_path:
        print("Carpeta 'RED ACTIVA' no encontrada.")
        return

    print(f"Ruta final encontrada: {red_activa_path}")
    return red_activa_path

#**************************************************************************************************************************************************
# Busca una carpeta específica dentro de una estructura de carpetas de forma recursiva.
def buscar_carpeta_en_estructura(origen, nombre_carpeta):

    for root, dirs, _ in os.walk(origen):
        print(f"Explorando: {root}")  # Información de depuración

        # Normalizar nombres de carpetas
        dirs_normalized = [d.lower() for d in dirs]

        # Verificar si alguna carpeta coincide con el nombre buscado
        if any(nombre_carpeta in d for d in dirs_normalized):
            for d in dirs:
                if nombre_carpeta in d.lower():
                    print('ACA')
                    return os.path.join(root, d)
                
    return None

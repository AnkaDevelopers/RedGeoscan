from calculos import formatear_fecha
from datetime import datetime
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

#**************************************************************************************************************************************************
# Busca una carpeta específica dentro de una estructura de carpetas de forma recursiva.
def buscar_crear_carpeta(origen, fecha):
    # Convertir la fecha al formato 'ddmmyy' desde 'dd/mm/yyyy'
    fecha_obj = datetime.strptime(fecha, '%d/%m/%Y')  # Ajuste para aceptar '/' en el formato
    fecha_formateada = fecha_obj.strftime('%d%m%y')

    # Verificar si la ruta de origen existe
    if not os.path.exists(origen):
        print(f"El origen {origen} no existe.")
        return

    # Buscar la estructura de carpetas
    for root, dirs, files in os.walk(origen):
        print(f"Explorando: {root}")  # Información de depuración
        
        # Normalizar los nombres de las carpetas a minúsculas para la comparación
        dirs_normalized = [d.lower() for d in dirs]

        # Verificar si existe una carpeta con un nombre similar a '6. TOPOGRAFIA'
        if any("6. topografia" in d for d in dirs_normalized):
            print("INGRESANDO A TOPOGRAFIA")
            
            # Obtener el nombre real de la carpeta coincidente
            for d in dirs:
                if "6. topografia" in d.lower():
                    topografia_path = os.path.join(root, d)
                    print(f"Ruta hasta este punto: {topografia_path}")
                    
                    # Normalizar los nombres de las subcarpetas dentro de '6. TOPOGRAFIA'
                    rastreos_normalized = [f.lower() for f in os.listdir(topografia_path)]

                    # Verificar si existe una carpeta con un nombre similar a 'RASTREOS'
                    if any("rastreos" in f for f in rastreos_normalized):
                        print("CARPETA RASTREOS ENCONTRADA")
                        
                        # Obtener la ruta real de la carpeta 'RASTREOS'
                        for f in os.listdir(topografia_path):
                            if "rastreos" in f.lower():
                                rastreos_path = os.path.join(topografia_path, f)
                                print(f"Ruta hasta este punto: {rastreos_path}")
                                
                                # Verificar si la carpeta con la fecha coincidente existe dentro de 'RASTREOS'
                                fecha_normalized = [sub.lower() for sub in os.listdir(rastreos_path)]
                                if fecha_formateada in fecha_normalized:
                                    print(f"CARPETA {fecha_formateada} ENCONTRADA")
                                    
                                    # Obtener la ruta real de la carpeta con la fecha
                                    for sub in os.listdir(rastreos_path):
                                        if fecha_formateada == sub.lower():
                                            fecha_path = os.path.join(rastreos_path, sub)
                                            print(f"Ruta hasta este punto: {fecha_path}")
                                            
                                            # Buscar la carpeta 'RED ACTIVA' dentro de la carpeta con la fecha
                                            red_activa_normalized = [s.lower() for s in os.listdir(fecha_path)]
                                            if any("red activa" in s for s in red_activa_normalized):
                                                print("CARPETA RED ACTIVA ENCONTRADA")
                                                
                                                # Obtener la ruta real de la carpeta 'RED ACTIVA'
                                                for s in os.listdir(fecha_path):
                                                    if "red activa" in s.lower():
                                                        red_activa_path = os.path.join(fecha_path, s)
                                                        print(f"Ruta hasta RED ACTIVA: {red_activa_path}")
                                                        
                                                        # Retornar la ruta final de la carpeta 'RED ACTIVA'
                                                        return red_activa_path
                                else:
                                    print(f"La carpeta con la fecha {fecha_formateada} no coincide, saltando esta ruta...")
                                    continue  # Saltar esta carpeta si no coincide la fecha
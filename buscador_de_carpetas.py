from datetime import datetime
import difflib
import config
import os

msj_buscardor = config.msj_buscador_carpetas
umbral_similitud = 0.8

#**************************************************************************************************************************************************
# Funcion que tiene como finalidad encontrar y listar las carpetas dentro de una ruta origen
def listar_carpetas_en_ruta(ruta):

    # Obtenemos todos los elementos en la ruta y filtramos las carpetas
    carpetas = [d for d in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, d))]
    return carpetas


#**************************************************************************************************************************************************
# Funcion que tiene como finalidad encontrar carpetas dentro de una ruta origen
def buscar_carpeta_en_estructura(origen, nombre_carpeta):
    try:
        # Lista los elementos del nivel actual en la ruta origen
        elementos = os.listdir(origen)
        
        # Información de depuración
        #print('*' * 50, '\n', msj_buscardor[8], '\n', origen)

        # Filtrar solo las carpetas
        carpetas = [d for d in elementos if os.path.isdir(os.path.join(origen, d))]

        for d in carpetas:
            # Normalizamos el nombre de la carpeta actual
            nombre_actual = d.lower().strip()

            # Verificamos similitud usando difflib
            similitud = difflib.SequenceMatcher(None, nombre_carpeta, nombre_actual).ratio()

            # Si la similitud es mayor o igual al umbral, consideramos que es la carpeta buscada
            if similitud >= umbral_similitud:
                return os.path.join(origen, d)

    except Exception as e:
        print(f"Error al acceder a la ruta {origen}: {e}")
    
    # Si no se encuentra la carpeta, devolver cadena vacía
    return ""


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
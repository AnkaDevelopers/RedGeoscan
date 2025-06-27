# Importar modulos Geoepoca
from geoepoca.utils.revisar_alteraciones import buscar_archivo_navegado, buscar_archivo_fix
from geoepoca.utils.comparar_excels import comparar_archivos_excel
from geoepoca.utils.calcular_fehca_ref import calculo_fehca_ref
from geoepoca.utils.calcular_epoca import calcular_dia_gps_y_epoca
from geoepoca.utils.seleccion_datos_rpa import seleccion_datos_para_rpa
from geoepoca.utils.guardar_datos_rpa import guardar_datos_para_rpa
from geoepoca.modulos.rpa_magnasirgas import rpa_magnasirgas
from geoepoca.modulos.generar_archivo_final import procesar_y_calcular

# Importar modulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import time
import os

# ***************************************************************************************************************
# Funcion de control geoEpoca
def geoEpoca(ruta_proyecto):
    
    #******************************************************************************
    # Si la ruta empieza con cualquier letra seguida de ":", se reemplaza por la ruta UNC
    if len(ruta_proyecto) > 2 and ruta_proyecto[1] == ":":
        # Se reemplaza la letra de unidad por la ruta UNC correspondiente
        ruta_proyecto = r"F:" + ruta_proyecto[2:]
        
        # Validar si la unidad F: realmente existe
        unidad = ruta_proyecto[:3]  # Ejemplo: 'F:\'
        if not os.path.exists(unidad):
            return "Error en ajuste de ruta.", 0
        
    # En caso de un error:
    else:
        return "La unidad especificada no existe en el sistema.", 0 
    
    #******************************************************************************
    # Funcion para verificar la existencia de un archivo navegado
    ruta_nav= buscar_archivo_navegado(ruta_proyecto)

    # Validación en caso de que la ruta no exista
    if ruta_nav is None:
        return "La carpeta 'navegado' no existe en la ruta especificada.", 1
    
    # Validación encaso de que el archivo aun no se allá cargado en la ruta
    elif ruta_nav is False:
        agregar_log("Aun no existe archivo navegado")
        return "sin navegado", None 
        
    #******************************************************************************
    # Función para verficiar la existencia de un archivo Fix
    ruta_fix = buscar_archivo_fix(ruta_proyecto)
    
    # Validación en caso de que la ruta no exista
    if ruta_fix is None:
        return "La carpéta 'FIX' no existe en la ruta especificada.", 2
    
    # valicaion en caso de que el archivo aun no se allá cargado en la ruta    
    elif ruta_fix is False:
        return "sin fix", None
    
    
    #******************************************************************************
    # Funcion para validar distancia entre puntos:
    resultados_comparacion = comparar_archivos_excel(ruta_nav, ruta_fix)
    
    # Validación de la funcion
    if resultados_comparacion is None:
        return "Fallo en validacion carteras", 3
    
    # depuracion
    # print(resultados_comparacion)
    #******************************************************************************
    # Funcion para determinar la fehca de referencia:
    fecha_refer = calculo_fehca_ref(ruta_nav)
    
    # Validación de la funcion
    if fecha_refer is None:
        return " fallo calculo fecha de referencia", 4
    
    # depuración
    # print(fecha_refer)
    #******************************************************************************
    # Función para calcular el valor de cambio de epoca a 2018 y el dia GPS segun la fecha de referencia
    dia_gps, epoca_2018 = calcular_dia_gps_y_epoca(fecha_refer)
    
    # Validación de la función
    if dia_gps is None:
        return "fallo en calculo de dia GPS y calculo de epoca2018", 5
    
    #******************************************************************************
    # Funcion para Prealistar los datos para el RPA al Magna Sirgas
    datos_rpa = seleccion_datos_para_rpa(ruta_fix, fecha_refer)
    
    # Validacion de la función
    if datos_rpa is None:
        return "fallo en prealistamiento de datos", 6
    
    # depuración
    # print(datos_rpa)
    #******************************************************************************
    # Funcion para guardar los datos ajustados para el inicio del RPA
    resultado_carpetacion = guardar_datos_para_rpa(datos_rpa)
    
    if resultado_carpetacion is None:
        return "fallo proceso de guardar csv para RPA", 7
    
    #******************************************************************************
    # Funcion encargada de correr el RPA
    resultado_rpa = rpa_magnasirgas()
    
    # Validacion de la función
    if resultado_rpa is None:
        return "fallo en RPA", 8
    
    #******************************************************************************
    # Funcion encargada de guardar el archivo final
    resultado_final = procesar_y_calcular(ruta_proyecto)
    
    # Validacion de la función
    if resultado_final is None:
        return "fallo en guardar archivo final", 9
    
    #******************************************************************************
    time.sleep(5000)
    return True, None

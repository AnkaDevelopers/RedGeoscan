# Importar modulos Geoepoca
from geoepoca.utils.revisar_alteraciones import consolidado_nav_fix_unico
from geoepoca.utils.guardar_datos_rpa import guardar_excel_para_rpa
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
    # Funcion para verificar la existencia de un archivo navegado
    ruta_consolidado= consolidado_nav_fix_unico(ruta_proyecto)

    # Validación en caso de que la ruta no exista
    if ruta_consolidado is None:
        return "La carpeta 'navegado' no existe en la ruta especificada.", 1, None
    
    # Validación encaso de que el archivo aun no se allá cargado en la ruta
    elif ruta_consolidado is False:
        agregar_log("Aun no existe archivo navegado")
        return "sin navegado", None, None 

    #******************************************************************************
    # Funcion para guardar los datos ajustados para el inicio del RPA
    resultado_carpetacion = guardar_excel_para_rpa(ruta_consolidado)
    
    if resultado_carpetacion is None:
        return "fallo proceso de guardar csv para RPA", 7, None
    
    
    #******************************************************************************
    # Funcion encargada de correr el RPA
    resultado_rpa = rpa_magnasirgas()
    
    # Validacion de la función
    if resultado_rpa is None:
        return "fallo en RPA", 8, None
    
    #******************************************************************************
    # Funcion encargada de guardar el archivo final
    resultado_final = procesar_y_calcular(ruta_proyecto)
    
    # Validacion de la función
    if resultado_final is None:
        return "fallo en guardar archivo final", 9, None
    
    #******************************************************************************

    return resultado_final, None

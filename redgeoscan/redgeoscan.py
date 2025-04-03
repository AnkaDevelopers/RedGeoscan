# Importar modulos redgeoscan
from redgeoscan.modulos.carga_kml.cargar_kml import cargar_kml
from redgeoscan.modulos.validacion_estructura_proyecto.carpetacion_proyecto import validar_carpetacion
from redgeoscan.modulos.validacion_estructura_proyecto.obtener_lista_subcarpetas import obtener_lista_sub_carpetas
from redgeoscan.modulos.crear_diccionario.proyecto_info import proyecto_info
from redgeoscan.modulos.crear_diccionario.sub_carpeta_info import sub_carpeta_info
from redgeoscan.modulos.crear_diccionario.sub_carpetas_gps import sub_carpetas_gps
from redgeoscan.modulos.crear_diccionario.prosesar_archivos_gps import procesar_archivos_gps
from redgeoscan.modulos.rpa.rpa_rtklib import ejecutar_rtk_para_gps
from redgeoscan.modulos.crear_diccionario.actualizar_pos import actualizar_diccionario_con_pos
from redgeoscan.modulos.gestion_token_principal.buscar_y_leer_txt_con_token import buscar_y_leer_archivo_token
from redgeoscan.modulos.rpa.token_principal import rpa_igac 
from redgeoscan.modulos.gestion_token_principal.actualizar_token_principal import actualizar_token_principal
from redgeoscan.modulos.procesar_pos.procesar_rutas_pos import procesar_rutas_pos
from redgeoscan.modulos.antenas_mas_cercanas.crear_diccionario_antenas_cercanas import crear_diccionario_con_antenas_mas_cercanas
from redgeoscan.modulos.servicios.obtener_data_antenas_materializadas import servicio_administrador_antenas
from redgeoscan.modulos.antenas_mas_cercanas.actualizar_diccionario_administrador_antenas import actualizar_diccionario_con_administradores_antenas
from redgeoscan.modulos.antenas_mas_cercanas.actualizar_diccionario_coordenada import actualizar_diccionario_con_coordenada
from redgeoscan.modulos.antenas_mas_cercanas.actualizar_diccionario_con_id_rinex import actualizar_diccionario_con_rinex_antenas
from redgeoscan.modulos.antenas_mas_cercanas.actualizar_diccionario_con_token_descarga import actualizar_diccionario_con_el_token_rinex
from redgeoscan.modulos.antenas_mas_cercanas.actualizar_diccionario_antenas_descargadas import actualizar_diccionario_antenas_descargadas
from redgeoscan.modulos.antenas_mas_cercanas.guardar_diccionario import guardar_diccionario_oculto
from redgeoscan.modulos.antenas_mas_cercanas.reporte import generar_informe_pdf_por_gps
from redgeoscan.modulos.antenas_mas_cercanas.respuesta_final import generar_resumen_proyecto
from redgeoscan.modulos.efemerides.efmerides import descargar_efemeride_para_semana

# Importar modulos de monitor
from monitor.log.log import agregar_log
from config import config

# Importaciones adicionales
import pandas as pd
import time

nombre_archivo_kml = config.nombre_archivo_excel[1]

# ***************************************************************************************************************
# Funcion de control RedGEoScan
def redGeoscan(ruta_archivos_excel, ruta_proyecto, nombre_proyecto):
    
    print(f"ruta archivo excel ingresada como parametro {ruta_archivos_excel}")
    print(f"ruta proyecto ingresada como parametro {ruta_proyecto}")
    print(f"nombre_proyecto ingresada como parametro {ruta_proyecto}")
    
    
    # Si la ruta empieza con cualquier letra seguida de ":", se reemplaza por la ruta UNC
    if len(ruta_proyecto) > 2 and ruta_proyecto[1] == ":":
        # Se reemplaza la letra de unidad por la ruta UNC correspondiente
        ruta_proyecto = r"Z:" + ruta_proyecto[2:]
    

    # Modulo que carga el archivo excel de las antenas
    respuesta_kml = cargar_kml(ruta_archivos_excel, nombre_archivo_kml)
    # Validación de la carga del archivo KML
    if respuesta_kml is None or respuesta_kml.empty:
        return None, 0
    
    # Modulo que se encarga de validar la estructura del proyecto
    msj_depuracion, respuesta_estructura = validar_carpetacion(ruta_proyecto)
        
    # Validacion estructura del proyecto
    if not respuesta_estructura:
        return msj_depuracion, 1
    
    # Modulo que se encarga de listar los dias de rastreos
    msj_depuracion, respuesta_dias_rastreos = obtener_lista_sub_carpetas(respuesta_estructura, "Rastreos" )
    
    # Validación de subcarpetas dias-rastreos
    if not respuesta_dias_rastreos:
        return msj_depuracion, 2
    
    # Modulo que se encarga de crear el diccionario conlos dias rastreos
    msj_depuracion, diccionario_proyecto_uno = proyecto_info(ruta_proyecto,respuesta_estructura, respuesta_dias_rastreos, nombre_proyecto)
    
    # Validación de diccionario uno proyecto
    if not diccionario_proyecto_uno:
        return msj_depuracion, 3
    
    # Modulo que se encarga de extraer la información de las subcarpetas de las carpetas dias rastreos
    msj_depuracion, diccionario_subcarpetas_dias_rastreos = sub_carpeta_info(diccionario_proyecto_uno)
    
    # Validación de diccionario de subcarpetas dias rastreos
    if not diccionario_subcarpetas_dias_rastreos:
        return msj_depuracion, 4
    
    msj_depuracion, diccionario_sub_carpeta_gps = sub_carpetas_gps(diccionario_subcarpetas_dias_rastreos)
    
    # Validación de diccionario de subcarpetas dias rastreos
    if not diccionario_sub_carpeta_gps:
        return msj_depuracion, 5
            
    # Modulo que se encarga de capturar las extenciones le los archivos para el rpa en rtklib
    msj_depuracion, diccionario_archivos_carpetas_gps = procesar_archivos_gps(diccionario_sub_carpeta_gps)
    

    # Validación de diccionario de subcarpetas dias rastreos
    if not diccionario_archivos_carpetas_gps:
        return msj_depuracion, 6        

    # Modulo que se encarga de la automatizacion con el progrma RTKLIB
    msj_depuracion, resultado_rpa_rtklib = ejecutar_rtk_para_gps(diccionario_archivos_carpetas_gps)
    
    # Validar funcionamiento de rtklib
    if resultado_rpa_rtklib == False:
        return msj_depuracion, 7
    
    # Modulo que se encarga de capturar las extenciones le los archivos para el rpa en rtklib
    msj_depuracion ,diccionario_archivos_carpetas_gps_V2 = actualizar_diccionario_con_pos(diccionario_sub_carpeta_gps)
    
    # Validación de diccionario de subcarpetas dias rastreos
    if not diccionario_archivos_carpetas_gps_V2:
        return msj_depuracion ,8
    
    
    # Modulo que se encarga de buscar y reutilizar el token principal en un archivo .txt en casioq ue siga siendo valido
    msj_depuracion, token_principal = buscar_y_leer_archivo_token()

    # validacion en caso de no encontrar el token principalo que ya se halla vencido
    if token_principal == 0:
        return msj_depuracion, 9
    
    # Validacion enc aso de que el token principla ya se halla vencido
    if token_principal == 1:
        
        # Modulo que se encarga de descargar el token principal
        msj_depuracion, token_principal = rpa_igac()
        
        # Validación de captura de token principal mediante rpa
        if not token_principal:
            return msj_depuracion, 10

    # Modulo que se encaraga de actualizar el token en el archivo .txt
    msj_depuracion, token_capturado = actualizar_token_principal(token_principal)
    
    # Validacion de actualizacion del token principal
    if not token_capturado:
        return msj_depuracion, 11
    
    # Modulo que se encarga de capturar la coordenada media de cada archivo .pos del diccionario
    msj_depuracion, diccionario_con_coordenada_media = procesar_rutas_pos(diccionario_archivos_carpetas_gps_V2)
    
    # Validación de extracción de la coordenada media del archivo .pos
    if not diccionario_con_coordenada_media:
        return msj_depuracion, 12
    
    # Modulo para calcular las antenas mas cercanas
    msj_depuracion, diccionario_con_antenas_mas_cercanas = crear_diccionario_con_antenas_mas_cercanas(diccionario_con_coordenada_media, respuesta_kml)
    
    # Validación de la actualización del diccionario donde podemos encontrar las antenas mas cercanas a cada archivo .pos en un radio de max 150 km
    if not diccionario_con_antenas_mas_cercanas:
        return msj_depuracion, 13
    
    # Modulo que se encarga de bajar la información de las antenas del serviciogeovisor del IGAC  y lo almacena en un JSON en esta ruta C:\bot-auto\docs
    msj_depuracion,consulta_base_administradores_antenas = servicio_administrador_antenas()
    
    # Mensaje de validación consumo serviciogeovisor
    if consulta_base_administradores_antenas == False:
        agregar_log(msj_depuracion)
    
    # Modulo que se encarga de actualizar el diccioanrio con los administradores de cada antena
    msj_depuracion, diccionario_antenas_con_administrador = actualizar_diccionario_con_administradores_antenas(diccionario_con_antenas_mas_cercanas, msj_depuracion)
    
    # Mensaje de validacion actualizacion del diccioanrio con los adminsitradores de las antenas
    if not diccionario_antenas_con_administrador:
        return msj_depuracion, 14
    
    # Modulo que se encarga de validar si una antena pertenece al orden 0 y tambien captura la coordenada SIRGAS
    msj_depuracion, diccionario_antenas_con_coordenada = actualizar_diccionario_con_coordenada(diccionario_antenas_con_administrador)
    
    # Validacion de actualizacion de antenas con la coordenada
    if not diccionario_antenas_con_coordenada:
        return msj_depuracion, 15
    

    # Modulo que se encarga de capturar el nombre y el id de los rinex de cada antena y los agrega al diccionario
    msj_depuracion, diccionario_antenas_con_rinex = actualizar_diccionario_con_rinex_antenas(diccionario_antenas_con_coordenada)
    
    # Validación de actualización de antenas con info de los rinex
    if not diccionario_antenas_con_rinex:
        return msj_depuracion, 16
    
    # Modulo que se encarga de capturar el token de descarga de los archivos rinex de las antenas y lo agrega al diccioanrio
    msj_depuracion, diccionario_antenas_con_token = actualizar_diccionario_con_el_token_rinex(diccionario_antenas_con_rinex)
    
    # Validación de actualizacion de diccionario con el token de descarga de los archivos rinex
    if not diccionario_antenas_con_token:
        return msj_depuracion, 17
    
    # Modulo que se encarga de descargar los archivos rinex
    msj_depuracion, diccionario_con_informacion_final_proyecto = actualizar_diccionario_antenas_descargadas(diccionario_antenas_con_token)

    # Validación de actualizacion de diccionario con el estado de los archivos descaragdos
    if not diccionario_con_informacion_final_proyecto:
        return msj_depuracion, 18
    
    # Modulo que se encarga de guardar la informacion del diccioanrio en un archivo json
    msj_depuracion, guardar_diccionario = guardar_diccionario_oculto(diccionario_con_informacion_final_proyecto)

    # Validación de actualizacion de diccionario con el estado de los archivos descaragdos
    if not guardar_diccionario:
        return msj_depuracion, 19
        
    msj_depuracion, resultado_informes = generar_informe_pdf_por_gps(diccionario_con_informacion_final_proyecto)    

    # Validación de informe
    if not resultado_informes:
        return msj_depuracion, 20

    # Modulo que se encarga de crear una respuesta del informe que se enviara al correo 
    msj_depuracion, respuesta_final, estado = generar_resumen_proyecto(diccionario_con_informacion_final_proyecto)
    
    # Validación de proyecto
    if not respuesta_final:
        return msj_depuracion, 21
    
    #semana = diccionario_con_informacion_final_proyecto["dias_rastreos"]["091024"]["subcarpetas"]["Base"]["sub_carpetas"]["GPS_n"]["informacion_pos"]["semana"]
    #print(semana)

    '''
    resultado = descargar_efemeride_para_semana("2250", "/ruta/destino")
    if resultado:
        print("✅ Descarga y descompresión exitosa.")
    else:
        print("⚠️ Ocurrió un problema.")
    '''
    return respuesta_final, estado
    print(resultado_rpa_rtklib)
    print(msj_depuracion)
    print(respuesta_final)
    print(estado)
    print("*"*500)
    time.sleep(100)
#***************************************************************************************************************************************
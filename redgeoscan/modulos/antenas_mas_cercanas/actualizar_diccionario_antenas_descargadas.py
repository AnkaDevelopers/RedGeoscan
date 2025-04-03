# Importar modulos redgeoscan
from redgeoscan.modulos.servicios.descargar_archivos_rinex import descargar_archivo

# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import os

#********************************************************************************************************************
# Funcion que se encarga de iterar sobre el diccioanrio y descargar las antenas
def actualizar_diccionario_antenas_descargadas(diccionario):

    try:
        # Recorremos los días en "dias_rastreos"
        for dia, contenido in diccionario.get("dias_rastreos", {}).items():
            agregar_log(f"Procesando día: {dia}")
            
            # Verificar la existencia de "subcarpetas"
            subcarpetas = contenido.get("subcarpetas", {})

            # capturamos la clave "Red activa"
            red_activa = subcarpetas.get("Red activa")

            # Obtener "Base" dentro de "subcarpetas"
            base = subcarpetas.get("Base", {})

            # Obtener "sub_carpetas" dentro de "Base"
            sub_carpetas_gps = base.get("sub_carpetas", {})

            # Iteramos sobre las claves GPS (como GPS_n, GPS_o, etc.)
            for gps_carpeta, gps_contenido in sub_carpetas_gps.items():
                agregar_log(f"Procesando carpeta GPS: {gps_carpeta}")

                # Obtenemos las antenas cercanas dentro de la clave "antenas_cercanas"
                antenas_cercanas = gps_contenido.get("antenas_cercanas", [])
                
                if not antenas_cercanas:
                    agregar_log(f"No se encontraron antenas cercanas en {gps_carpeta}.")
                    continue

                for antena in antenas_cercanas:
                    # Obtenemos el nombre y el estado "MATERIALIZADA" de cada antena
                    nombre_antena = antena.get("NAME")
                    materializada = antena.get("MATERIALIZADA")
                    orden = antena.get("ORDEN")
                    agregar_log(f"Procesando antena: {nombre_antena}, Materializada: {materializada}, Orden: {orden}")

                    # Revisamos los archivos en "RINEX_ARCHIVOS"
                    rinex_archivos = antena.get("RINEX_ARCHIVOS", [])
                    if rinex_archivos:

                        for archivo in rinex_archivos:
                            nombre_archivo = archivo.get("NOMBRE_ARCHIVO")
                            token_rinex = archivo.get("TOKEN_RINEX")
                            
                            # Ruta para alamcenar los archivos
                            ruta_red_activa_gps = os.path.join(red_activa,gps_carpeta)
                            agregar_log(f"Intentando descargar archivo: {nombre_archivo} en ruta: {ruta_red_activa_gps}")
                        
                            # Funcion descargar archivo
                            resultado_descarga = descargar_archivo(token_rinex,ruta_red_activa_gps,materializada,nombre_antena,nombre_archivo)
                        
                            if resultado_descarga == True:
                                antena["DESCARGA"] = "COMPLETA"
                            else:
                                antena["DESCARGA"] = "INCOMPLETA"
                                agregar_log(f"Descarga incompleta del archivo: {nombre_archivo}")
                    
                    else:
                        agregar_log(f"No se encontraron archivos RINEX para la antena: {nombre_antena}")
                        if orden == "1":
                            antena["DESCARGA"] = "SIN RINEX"
                        else:
                            antena["DESCARGA"] = "SIN RINEX"
        
        agregar_log("Actualización del diccionario completada.")

        return None, diccionario
        
    except Exception as e:
        msj_depúracion = f"Error procesando el diccionario: {e}"
        return msj_depúracion, None

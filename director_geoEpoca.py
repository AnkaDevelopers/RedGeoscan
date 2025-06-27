# Importar modulos GeoEpoca           
from geoepoca.geoEpoca import geoEpoca                                            

# Importar modulos monitor
from monitor.log.log import agregar_log, guardar_log_en_archivo, enviar_log_por_correo

# Importar modulos Adicionales
import pandas as pd
import datetime
import time
import os

# ***********************************************************************************************************
# Enviar errores solo al equipo de soporte

def enviar_respuesta_equipo_de_soporte(msj_depuracion, rpta):
    if rpta:
        agregar_log(rpta)
        agregar_log(msj_depuracion)
    else:
        agregar_log(msj_depuracion)

    guardar_log_en_archivo("Proceso_Geoepoca")
    enviar_log_por_correo(msj_depuracion)

# ***********************************************************************************************************
# Función principal de verificación

def control_verificacion_proyectos(ruta_archivos_excel, nombre_archivo_excel):
    agregar_log("Inicio verificación complementaria de proyectos\n")

    # Construcción de ruta completa del archivo Excel
    ruta_excel = os.path.join(ruta_archivos_excel[0], nombre_archivo_excel[0])

    try:
        # Carga el Excel en un DataFrame
        df = pd.read_excel(ruta_excel)
        cambios_realizados = False  # <== Agregado

        # Recorre cada proyecto listado en el Excel
        for indice_fila, datos_proyecto in df.iterrows():
            
            # Tiempod e refresco
            time.sleep(2)
            
            # Obtiene la ruta completa donde está el proyecto
            ruta_completa_proyecto = datos_proyecto.get("ruta", "").strip()
            
            # Lee el estado actual del proyecto (por ejemplo: "Completo", "En Proceso", etc.)
            estado_proyecto = str(datos_proyecto.get("estado", "")).strip().lower()
            
            # Verifica si ya se hizo el cambio de época
            estado_cambio_epoca = str(datos_proyecto.get("cambio epoca", "")).strip().lower()
            
            # Extrae el nombre del proyecto desde la ruta (última parte del camino)
            nombre_carpeta_proyecto = os.path.basename(ruta_completa_proyecto)
            
            agregar_log(f"Analizando proyecto: {nombre_carpeta_proyecto}")
                        
            if estado_proyecto == "en proceso":
                agregar_log("Proceso RedGeoscan en Proceso saltar...")
                continue
            
            # Si ya está completo el cambio de época, no se necesita procesar
            if estado_cambio_epoca == "completo":
                agregar_log("Cambio de epoca completo saltar...")
                continue

            # *************************Inicio de programa GeoEpoca***********************************
            respuesta_geoepoca, codigo_estado = geoEpoca(ruta_completa_proyecto)
            
            mensajes_error = {
                0: "FALLA EN ASIGNACION DE INDICE",
                1: "FALLA EN RUTA DE ARCHIVO NAVEGADO",
                2: "FALLA EN RUTA DE ARCHIVO FIX",
                3: "FALLA EN COMPARACION ARCHIVOS",
                4: "FALLA EN EXTRACCIÓN FEHCA DE REFERENCIA",
                5: "FALLA EN CALCULO DE DIA GPS",
                6: "FALLA EN ALISTAMIENTO DE DATOS PARA EL RPA",
                7: "FALLA EN GUARDADO DE DATOS PARA EL RPA",
                8: "FALLA EN RPA",
                9: "FALLA EN GUARDAR ARCHIVO FINAL",
            }

            if codigo_estado in mensajes_error:
                enviar_respuesta_equipo_de_soporte(mensajes_error[codigo_estado], respuesta_geoepoca)
                continue
            if codigo_estado is None:
                
                # Actualizar columna navegado cuando aun no se ha cargado un archivo navegado
                if respuesta_geoepoca == "sin navegado":
                    agregar_log(f"Aun no se ha cargado el archivo navegado en el proyecto {nombre_carpeta_proyecto}.")
                    df.at[indice_fila, "navegado"] = "Sin Archivo"
                    cambios_realizados = True 
                
                # Actualizar columna fix cuando aun no se ha cargado un archivo fix
                if respuesta_geoepoca == "sin fix":
                    agregar_log(f"Aun no se ha cargado el archivo navegado en el proyecto {nombre_carpeta_proyecto}.")
                    df.at[indice_fila, "fix"] = "Sin Archivo"
                    cambios_realizados = True 
                    
        # *************************
        if cambios_realizados:  # <== Agregado
            df.to_excel(ruta_excel, index=False)
            agregar_log("Excel actualizado con los nuevos estados.")
        else:  # <== Agregado
            agregar_log("No se realizaron cambios en el Excel. No se actualizó el archivo.")  
            
    except Exception as e:
        agregar_log(f"⚠ Error en: {e}")
        # enviar_log_por_correo(f"Error crítico al verificar proyectos: {e}")  # Se puede activar si se desea

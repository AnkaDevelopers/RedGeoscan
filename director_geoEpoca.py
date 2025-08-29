# Importar modulos GeoEpoca           
from geoepoca.geoEpoca import geoEpoca                                            

# Importar modulos monitor
from monitor.log.log import agregar_log, guardar_log_en_archivo, enviar_log_por_correo, enviar_correo_personalizado

# Importar modulo de consumo y actualizacion de proyecto
from services.actualizarProyecto import actualizarProyecto

# Importar eliminar Proyecto
from eliminarProyecto import eliminar_proyecto

# Importar configuraciones globales
from config import config

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

def control_verificacion_proyectos():

    try:
        # Carga el Excel en un DataFrame
        df = pd.read_excel(config.ruta_excel)
        cambios_realizados = False
        indices_a_eliminar = []  # <== agregado: aquí guardamos las filas a borrar del Excel

        # Recorre cada proyecto listado en el Excel
        for idex, row in df.iterrows():
            
            # Extraer el ID del proyecto
            id_proyecto = row.get("ID_PROYECTO")
            
            # Extraer la ruta del proyecto
            ruta_proyecto = row.get("RUTA_PROYECTO")
            
            # Extraer el estado del proyecto en redgeoscan
            estado = row.get("ESTADO_GEO")

            # Extraer nombre del proyecto desde la ruta
            nombre_proyecto = os.path.basename(ruta_proyecto.strip() if isinstance(ruta_proyecto, str) else "")

            agregar_log(f"Analizando proyecto: {nombre_proyecto}")
                        
            if estado == "Finalizado":

                # Eliminar carpeta/proyecto del disco
                try:
                    eliminar_proyecto(ruta_proyecto)
                    agregar_log(f"Proyecto eliminado del disco: {ruta_proyecto}")
                except Exception as e:
                    agregar_log(f"No se pudo eliminar la carpeta del proyecto: {e}")
                
                # Marcar fila para eliminar del Excel
                indices_a_eliminar.append(idex)  # <== agregado
                cambios_realizados = True        # <== agregado
                continue

            if estado == "Completo":
                continue
            
            if estado == "Sin Dias Rastreos":
                continue
            
            if estado == "Sin Carteras":
                continue

            # *************************Inicio de programa GeoEpoca***********************************
            respuesta_geoepoca, codigo_estado = geoEpoca(ruta_proyecto)
            
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
                enviar_correo_personalizado(
                    destinatario=config.correoDesarrollo,
                    asunto=f"Proyecto {nombre_proyecto} Finalizado", 
                    cuerpo_html=f"<p> Corrdenadas Finales creadas en:{respuesta_geoepoca}</p>"
                )
                actualizarProyecto(id_proyecto, ESTADO_GEO="Completo")
                
        # ***********************************************************************************************
        # Eliminar del DataFrame todas las filas marcadas y guardar Excel
        if indices_a_eliminar:
            df = df.drop(index=indices_a_eliminar).reset_index(drop=True)  # <== agregado
            agregar_log(f"Se eliminaron {len(indices_a_eliminar)} fila(s) del Excel (estado Finalizado).")
            cambios_realizados = True

        if cambios_realizados:
            df.to_excel(config.ruta_excel, index=False)
            agregar_log("Excel actualizado con los cambios.")
        else:
            agregar_log("No se realizaron cambios en el Excel. No se actualizó el archivo.")  
            
    except Exception as e:
        agregar_log(f"⚠ Error en: {e}")
        enviar_respuesta_equipo_de_soporte(f"Error crítico: {e}", None)

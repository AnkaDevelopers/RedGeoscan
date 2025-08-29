# Importar módulos redgeoscan
from redgeoscan.redgeoscan import redGeoscan

# Importar módulos monitor
from monitor.log.log import agregar_log, guardar_log_en_archivo, enviar_log_por_correo, enviar_correo_personalizado

# Importar configuraciones globales
from config import config

# Importar eliminar Proyecto
from eliminarProyecto import eliminar_proyecto, eliminar_proyecto_db, obtener_numero_gps

# Importar modulo de consumo y actualizacion de proyecto
from services.actualizarProyecto import actualizarProyecto

# Importar módulos adicionales
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

    guardar_log_en_archivo("Proceso_redgeoscan")
    enviar_log_por_correo(msj_depuracion)

# ***********************************************************************************************************
# Programa principal

def control_redgeoscan():
    try:
        df = pd.read_excel(config.ruta_excel)
        fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
        cambios_realizados = False
        indices_a_eliminar = []  # <- filas a eliminar del Excel cuando el estado sea "Finalizado"

        for index, row in df.iterrows():
            
            # Extraer el ID del proyecto
            id_proyecto = row.get("ID_PROYECTO")
            
            # Extraer la ruta del proyecto
            ruta_proyecto = row.get("RUTA_PROYECTO")
            
            # Extraer el estado del proyecto en redgeoscan
            estado = row.get("ESTADO_RED")
            
            # Extraer RADIO
            radio = row.get("RADIO_BUSQUEDA")

            # Nombre desde ruta (seguro ante None)
            nombre_proyecto = os.path.basename(ruta_proyecto.strip() if isinstance(ruta_proyecto, str) else "")

            # Si ya está Finalizado -> eliminar carpeta y fila del Excel
            if estado == "Finalizado":
                                                
                try:
                    eliminar_proyecto_db(id_proyecto)
                    agregar_log(f"Proyecto eliminado de la DB")
                except:
                    agregar_log(f"No se pudo eliminar el proyecto de la DB")
                try:
                    eliminar_proyecto(ruta_proyecto)
                    agregar_log(f"Proyecto eliminado del disco: {ruta_proyecto}")
                except Exception as e:
                    agregar_log(f"No se pudo eliminar la carpeta del proyecto: {e}")
                indices_a_eliminar.append(index)
                cambios_realizados = True
                continue

            # Saltos de estados que no requieren proceso
            if estado == "Completo":
                continue
            if estado == "Sin Dias Rastreos":
                continue
            if estado == "Sin GPS":
                continue

            # Evitar reprocesar el mismo día
            if estado == fecha_actual:
                agregar_log(f"Proyecto {nombre_proyecto} ya fue procesado hoy ({fecha_actual}).")
                continue

            agregar_log(f"Procesando proyecto: {nombre_proyecto}")
            agregar_log("RedGeoScan iniciado...")

            # ******* Obtener el número de GPS antes de procesar el proyecto ******
            gps_inicial = obtener_numero_gps(id_proyecto)
            agregar_log(f"Inicialmente, el proyecto tiene {gps_inicial} GPS asociados.")

            respuesta_red_geoscan, codigo_estado = redGeoscan(id_proyecto, ruta_proyecto, nombre_proyecto, radio)

            # Manejo de errores por código de estado
            mensajes_error = {
                0: "FALLA EN CARGA KML!",
                1: f"FALLA EN CARPETACIÓN !!!: {respuesta_red_geoscan}",
                2: f"ERROR EN CARPETAS DIAS RASTREOS !!!: {respuesta_red_geoscan}",
                3: "FALLA EN CREACIÓN DICCIONARIO !!!",
                4: "FALLA EN OBTENCIÓN DE RUTAS SUB-CARPETAS DÍAS RASTREOS !!!",
                5: "FALLA EN OBTENCIÓN DE RUTAS CARPETAS GPS !!!",
                6: "FALLA EN OBTENCIÓN DE RUTAS ARCHIVOS GPS obs, pos, etc !!!",
                7: "FALLA RPA RTKLIB !!!",
                8: "FALLA EN ACTUALIZACIÓN DE RUTAS ARCHIVOS .POS !!!",
                9: "FALLA NO DEFINIDA (código 9)",
                10: "FALLA, NO FUE POSIBLE CAPTURAR EL TOKEN PRINCIPAL !!!",
                11: "FALLA, NO FUE POSIBLE ACTUALIZAR EL TOKEN PRINCIPAL !!!",
                12: "FALLA, ERROR AL GENERAR COORDENADA MEDIA .POS !!!",
                13: "FALLA, NO SE AGREGARON ANTENAS MÁS CERCANAS !!!",
                14: "FALLA, NO SE AGREGARON ADMINISTRADORES DE ANTENAS !!!",
                15: "FALLA, NO SE AGREGARON COORDENADAS DE ANTENAS !!!",
                16: "FALLA, NO SE AGREGÓ INFO RINEX DE ANTENAS !!!",
                17: "FALLA, NO SE AGREGARON TOKENS DE DESCARGA RINEX !!!",
                18: "FALLA, EN DESCARGA DE ARCHIVOS RINEX !!!",
                19: "FALLA, EN GUARDAR DICCIONARIO !!!",
                20: "FALLA, EN REPORTES !!!",
                21: "FALLA, EN RESPUESTA FINAL !!!",
            }
            # ******* Obtener el número de GPS después del proceso ******
            gps_final = obtener_numero_gps(id_proyecto)
            agregar_log(f"Después de RedGeoScan, el proyecto tiene {gps_final} GPS asociados.")

            if codigo_estado in mensajes_error:
                enviar_respuesta_equipo_de_soporte(mensajes_error[codigo_estado], respuesta_red_geoscan)
                continue
            # ******* Verificar si el número de GPS ha cambiado ******
            if gps_final > gps_inicial:
                agregar_log(f"¡Sorpresa! El número de GPS ha aumentado. Actualizando estado a 'En Proceso'.")
                df.at[index, "ESTADO_RED"] = "En Proceso"
                cambios_realizados = True
                actualizarProyecto(id_proyecto, ESTADO_RED="En Proceso")
                time.sleep(1)
                enviar_correo_personalizado(destinatario=config.correoDesarrollo, asunto=f"Proyecto {nombre_proyecto} en Proceso", cuerpo_html=f"<p>{respuesta_red_geoscan}</p>")
                continue                                                                                                                                   
                
            if str(codigo_estado).lower() == "completo":
                agregar_log(f"Proyecto {nombre_proyecto} completado con éxito.")
                df.at[index, "ESTADO_RED"] = "Completo"
                cambios_realizados = True
                actualizarProyecto(id_proyecto, ESTADO_RED="Completo")
                time.sleep(1)
                enviar_correo_personalizado( destinatario=config.correoDesarrollo, asunto=f"Proyecto {nombre_proyecto} Finalizado", cuerpo_html=f"<p> {respuesta_red_geoscan}</p>" )
            else:
                agregar_log(f"Proyecto {nombre_proyecto} incompleto. Registrando revisión de hoy.")
                df.at[index, "ESTADO_RED"] = fecha_actual  # reflejar en Excel también
                cambios_realizados = True
                actualizarProyecto(id_proyecto, ESTADO_RED=fecha_actual)
                time.sleep(1)
                enviar_correo_personalizado( destinatario=config.correoDesarrollo, asunto=f"Proyecto {nombre_proyecto} Revisado", cuerpo_html=f"<p> {respuesta_red_geoscan}</p>" )



        # --- aplicar eliminaciones y guardar Excel ---
        if indices_a_eliminar:
            df = df.drop(index=indices_a_eliminar).reset_index(drop=True)
            agregar_log(f"Se eliminaron {len(indices_a_eliminar)} fila(s) del Excel (estado Finalizado).")
            cambios_realizados = True

        if cambios_realizados:
            df.to_excel(config.ruta_excel, index=False)
            agregar_log("Excel actualizado con los nuevos estados.")
        else:
            agregar_log("No se realizaron cambios en el Excel. No se actualizó el archivo.")

    except Exception as e:
        agregar_log(f"Error al procesar el archivo Excel: {e}")
        enviar_respuesta_equipo_de_soporte(f"Error crítico: {e}", None)

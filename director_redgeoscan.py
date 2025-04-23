# Importar módulos redgeoscan
from redgeoscan.redgeoscan import redGeoscan

# Importar módulos monitor
from monitor.log.log import agregar_log, guardar_log_en_archivo, enviar_log_por_correo

# Importar módulos adicionales
import pandas as pd
import time
import datetime
import os

# Importar módulos adicionales
import pandas as pd
import datetime
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

def control_redgeoscan(ruta_archivos_excel, nombre_archivo_excel):
    agregar_log("Inicio Programa director\n")

    ruta_completa_cola_rutas_proyectos = os.path.join(ruta_archivos_excel[0], nombre_archivo_excel[0])

    try:
        df = pd.read_excel(ruta_completa_cola_rutas_proyectos)
        fecha_actual = datetime.date.today().strftime("%d-%m-%Y")
        cambios_realizados = False  # <== Agregado

        for index, row in df.iterrows():
            ruta_proyecto = row.get("ruta")
            estado = str(row.get("estado", "")).strip().lower()

            # Extraer nombre del proyecto desde la ruta
            nombre_proyecto = os.path.basename(ruta_proyecto.strip())
            
            # Extraer el radio de busqueda
            radio = row.get("radio", None)


            if estado == "completo":
                continue

            if estado == fecha_actual:
                agregar_log(f"Proyecto {nombre_proyecto} ya fue procesado hoy ({fecha_actual}).")
                continue

            agregar_log(f"Procesando proyecto: {nombre_proyecto}")
            agregar_log("RedGeoScan iniciado...")

            respuesta_red_geoscan, codigo_estado = redGeoscan(ruta_archivos_excel[1], ruta_proyecto, nombre_proyecto, radio)

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

            if codigo_estado in mensajes_error:
                enviar_respuesta_equipo_de_soporte(mensajes_error[codigo_estado], respuesta_red_geoscan)
                continue

            if str(codigo_estado).lower() == "completo":
                agregar_log(f"Proyecto {nombre_proyecto} completado con éxito.")
                df.at[index, "estado"] = "Completo"
                cambios_realizados = True  # <== Agregado
                enviar_respuesta_equipo_de_soporte(f"Proyecto: {nombre_proyecto} completo", respuesta_red_geoscan)

            else:
                agregar_log(f"Proyecto {nombre_proyecto} incompleto. Registrando revisión de hoy.")
                df.at[index, "estado"] = fecha_actual
                cambios_realizados = True  # <== Agregado

        if cambios_realizados:  # <== Agregado
            df.to_excel(ruta_completa_cola_rutas_proyectos, index=False)
            agregar_log("Excel actualizado con los nuevos estados.")
        else:  # <== Agregado
            agregar_log("No se realizaron cambios en el Excel. No se actualizó el archivo.")

    except Exception as e:
        agregar_log(f"Error al procesar el archivo Excel: {e}")
        enviar_respuesta_equipo_de_soporte(f"Error crítico: {e}", None)

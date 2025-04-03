# Importar modulos redgeoscan
from redgeoscan.modulos.servicios.obtener_id_rinex_antenas import servicio_comprobar_rinex_por_fecha

# Importar modulos de monitor
from monitor.log.log import agregar_log

#********************************************************************************************************************************
# Función para actualizar el diccionario con la información de los RINEX de las antenas donde ORDEN es "0"
def actualizar_diccionario_con_rinex_antenas(diccionario):
    try:
        agregar_log("Inicio actualización del diccionario con nombres e IDs de archivos RINEX.")

        # Iterar sobre los días de rastreo en el diccionario
        for dia, info_dia in diccionario.get("dias_rastreos", {}).items():
            base_subcarpetas = info_dia.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})

            for gps_nombre, gps_info in base_subcarpetas.items():
                informacion_pos = gps_info.get("informacion_pos", {})
                fecha = informacion_pos.get("fecha", "").split(" ")[0]  # Extraer fecha en formato yyyy/mm/dd
                if not fecha:
                    agregar_log(f"No se encontró una fecha válida para el GPS: {gps_nombre}.")
                    continue

                # Convertir la fecha al formato requerido dd-mm-yyyy
                fecha_formateada = "-".join(reversed(fecha.split("/")))

                antenas_cercanas = gps_info.get("antenas_cercanas", [])

                for antena in antenas_cercanas:
                    nombre_antena = antena.get("NAME")

                    if not nombre_antena:
                        agregar_log(f"Antena sin nombre encontrada en el GPS: {gps_nombre}.")
                        continue

                    # Consumir el servicio para obtener los datos RINEX
                    datos_rinex = servicio_comprobar_rinex_por_fecha(fecha_formateada, nombre_antena)

                    if datos_rinex:
                        # Almacenar todos los archivos RINEX relacionados
                        antena["RINEX_ARCHIVOS"] = datos_rinex
                        agregar_log(f"Actualizados datos RINEX para la antena {nombre_antena}.")
                    else:
                        # Dejar vacío si no hay datos RINEX
                        antena["RINEX_ARCHIVOS"] = []
                        agregar_log(f"No se encontraron datos RINEX para la antena {nombre_antena}.")

        agregar_log("Finalizada la actualización del diccionario con datos RINEX.")
        return None, diccionario

    except Exception as e:
        msj_depuracion = f"!!!Error durante la actualización del diccionario con datos RINEX!!!: {e}"

        return msj_depuracion, None

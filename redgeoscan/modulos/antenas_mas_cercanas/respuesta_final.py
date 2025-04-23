# Importaciones de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
import time

def generar_resumen_proyecto(diccionario):
    print(diccionario)
    time.sleep(1)  # Pequeña pausa para visualización

    try:
        # Obtener el nombre del proyecto
        nombre_proyecto = diccionario.get("nombre", "Desconocido")

        # Log inicial
        agregar_log(f"Procesando proyecto: {nombre_proyecto}")

        # Inicializar mensaje de resumen
        mensaje_resumen = f"Proyecto {nombre_proyecto}\n"
        estado_proyecto = "COMPLETO"

        # Obtener los días de rastreo
        dias_rastreos = diccionario.get("dias_rastreos", {})

        for dia, detalles_dia in dias_rastreos.items():
            agregar_log(f"Procesando día de rastreo: {dia}")
            mensaje_resumen += f"Días rastreos: {dia}\n"

            base_info = detalles_dia.get("subcarpetas", {}).get("Base", {})
            subcarpetas = base_info.get("sub_carpetas", {})
            ruta_base = base_info.get("ruta", "")

            gps_completos = []

            for gps_nombre, gps_detalles in subcarpetas.items():
                agregar_log(f"Procesando carpeta GPS: {gps_nombre}")

                antenas = gps_detalles.get("antenas_cercanas", [])
                total_antenas = len(antenas)

                # --- NUEVA LÓGICA ---
                # Antenas con descarga completa
                descargas_completas = [antena for antena in antenas if antena.get("DESCARGA", "") == "COMPLETA"]
                total_descargas = len(descargas_completas)

                # Cuántas son de orden 0
                orden_0_completas = sum(1 for antena in descargas_completas if antena.get("ORDEN", "") == "0")

                # Condición de completitud
                estado_gps = "COMPLETO" if total_descargas >= 4 and orden_0_completas >= 2 else "INCOMPLETO"
                if estado_gps == "INCOMPLETO":
                    estado_proyecto = "INCOMPLETO"

                agregar_log(f"Total antenas procesadas: {total_antenas}, Descargas completas: {total_descargas}, Orden 0 completas: {orden_0_completas}, Estado: {estado_gps}")

                mensaje_resumen += (f"{gps_nombre}: se procesaron {total_antenas} antenas, "
                                    f"{total_descargas} completas, {orden_0_completas} de orden 0 "
                                    f"({estado_gps})\n")

                # Renombrar carpeta GPS si está completa
                gps_ruta = gps_detalles.get("ruta", "")
                if estado_gps == "COMPLETO" and not gps_ruta.endswith("-completo"):
                    nueva_ruta_gps = gps_ruta + "-completo"
                    if os.path.exists(gps_ruta):
                        os.rename(gps_ruta, nueva_ruta_gps)
                        agregar_log(f"Carpeta GPS renombrada: {gps_ruta} → {nueva_ruta_gps}")
                        gps_completos.append(True)
                    else:
                        agregar_log(f"Ruta de GPS no encontrada: {gps_ruta}")
                else:
                    gps_completos.append(False)

            # Renombrar la carpeta del día si TODOS los GPS fueron completados
            if all(gps_completos) and ruta_base:
                ruta_dia = detalles_dia.get("ruta-dia")
                if ruta_dia and not ruta_dia.endswith("-completo"):
                    nueva_ruta_dia = ruta_dia + "-completo"
                    if os.path.exists(ruta_dia):
                        os.rename(ruta_dia, nueva_ruta_dia)
                        agregar_log(f"Carpeta del día renombrada: {ruta_dia} → {nueva_ruta_dia}")
                    else:
                        agregar_log(f"Ruta del día no encontrada: {ruta_dia}")

        agregar_log("Resumen del proyecto generado correctamente.")
        return None, mensaje_resumen, estado_proyecto

    except Exception as e:
        msj_depuracion = f"Error al generar el resumen del proyecto: {e}"
        return msj_depuracion, None, None

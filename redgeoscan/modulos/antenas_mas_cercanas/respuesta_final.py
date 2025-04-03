from monitor.log.log import agregar_log

def generar_resumen_proyecto(diccionario):
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
            # Log del día
            agregar_log(f"Procesando día de rastreo: {dia}")

            # Agregar día al mensaje
            mensaje_resumen += f"Días rastreos: {dia}\n"

            # Obtener las carpetas GPS dentro de las subcarpetas del día
            subcarpetas = detalles_dia.get("subcarpetas", {}).get("Base", {}).get("sub_carpetas", {})

            for gps_nombre, gps_detalles in subcarpetas.items():
                # Log de la carpeta GPS
                agregar_log(f"Procesando carpeta GPS: {gps_nombre}")

                # Contar antenas procesadas y con descarga completa
                antenas = gps_detalles.get("antenas_cercanas", [])
                total_antenas = len(antenas)
                descargas_completas = sum(1 for antena in antenas if antena.get("DESCARGA", "") == "COMPLETA")

                # Determinar estado de la carpeta GPS
                estado_gps = "COMPLETO" if descargas_completas >= 4 else "INCOMPLETO"
                if estado_gps == "INCOMPLETO":
                    estado_proyecto = "INCOMPLETO"

                # Log de antenas
                agregar_log(f"Total antenas procesadas: {total_antenas}, Descargas completas: {descargas_completas}, Estado: {estado_gps}")

                # Agregar información de GPS al mensaje
                mensaje_resumen += (f"{gps_nombre}: se procesaron {total_antenas} antenas "
                                    f"de las cuales {descargas_completas} con descarga completa ({estado_gps})\n")

        # Log final
        agregar_log("Resumen del proyecto generado correctamente.")

        # Retornar el mensaje y el estado del proyecto
        return None, mensaje_resumen, estado_proyecto
    
    except Exception as e:
        
        msj_depuracion = f"Error al generar el resumen del proyecto: {e}"
        return msj_depuracion, None, None


from redgeoscan.modulos.validacion_estructura_proyecto.obtener_lista_subcarpetas import obtener_lista_sub_carpetas
from monitor.log.log import agregar_log
from os.path import join, exists
from os import rename, makedirs
import os


def sub_carpeta_info(diccionario_proyecto_uno):
    try:
        agregar_log("Inicio de procesamiento de días de rastreos...")

        resultado = {
            "nombre": diccionario_proyecto_uno["nombre"],
            "ruta_principal": diccionario_proyecto_uno["ruta_principal"],
            "dias_rastreos": {}
        }

        for dia, info in diccionario_proyecto_uno["dias_rastreos"].items():
            ruta_dia = info["ruta"]
            es_carpeta_vacia = ruta_dia.endswith("-CarpetaVacia")
            dia_corregido = dia  # nombre corregido si cambia

            res, subcarpetas = obtener_lista_sub_carpetas(ruta_dia, dia)

            if not subcarpetas:
                agregar_log(f"{res} - Día {dia} sin subcarpetas.")

                if not es_carpeta_vacia and exists(ruta_dia):
                    nueva_ruta = ruta_dia + "-CarpetaVacia"
                    rename(ruta_dia, nueva_ruta)
                    agregar_log(f"Carpeta {ruta_dia} renombrada a {nueva_ruta}.")
                continue

            # Corrección de nombres mal escritos
            nombres_esperados = {
                "base": "Base",
                "vase": "Base",
                "bsae": "Base",
                "redactiva": "Red activa",
                "redactiva_": "Red activa",
                "redactiva2": "Red activa",
                "redactiva3": "Red activa",
                "redactiva4": "Red activa",
                "redactiva5": "Red activa",
                "redactiva6": "Red activa",
                "redactiva7": "Red activa",
                "redactiva8": "Red activa",
                "redactiva9": "Red activa",
                "redactiva0": "Red activa",
                "redactiva ": "Red activa",
                "redactiva.": "Red activa"
            }

            cambios_realizados = False
            for nombre in subcarpetas:
                nombre_limpio = nombre.lower().replace(" ", "")
                if nombre_limpio in nombres_esperados:
                    nombre_correcto = nombres_esperados[nombre_limpio]
                    if nombre != nombre_correcto:
                        ruta_errada = os.path.join(ruta_dia, nombre)
                        ruta_corregida = os.path.join(ruta_dia, nombre_correcto)
                        if exists(ruta_errada):
                            rename(ruta_errada, ruta_corregida)
                            agregar_log(f"Renombrada subcarpeta '{nombre}' a '{nombre_correcto}' en {ruta_dia}")
                            cambios_realizados = True

            if cambios_realizados:
                _, subcarpetas = obtener_lista_sub_carpetas(ruta_dia, dia)

            # Verificación final de carpetas
            subcarpetas_dict = {nombre.lower().replace(" ", ""): nombre for nombre in subcarpetas}

            if "base" not in subcarpetas_dict:
                agregar_log(f"La carpeta 'Base' no existe en {ruta_dia}. Día {dia} marcado como vacío.")
                if not es_carpeta_vacia and exists(ruta_dia):
                    nueva_ruta = ruta_dia + "-CarpetaVacia"
                    rename(ruta_dia, nueva_ruta)
                    agregar_log(f"Carpeta {ruta_dia} renombrada a {nueva_ruta}.")
                continue

            if es_carpeta_vacia:
                nueva_ruta = ruta_dia.replace("-CarpetaVacia", "")
                if exists(ruta_dia):
                    rename(ruta_dia, nueva_ruta)
                    agregar_log(f"Carpeta {ruta_dia} renombrada a {nueva_ruta} (ya no está vacía).")
                ruta_dia = nueva_ruta
                dia_corregido = dia.replace("-CarpetaVacia", "")

            if "redactiva" not in subcarpetas_dict and "redactiva" not in [n.lower().replace(" ", "") for n in subcarpetas]:
                ruta_redactiva = join(ruta_dia, "Red activa")
                makedirs(ruta_redactiva, exist_ok=True)
                agregar_log(f"Subcarpeta 'Red activa' creada automáticamente en {ruta_dia}")
                _, subcarpetas = obtener_lista_sub_carpetas(ruta_dia, dia)

            subcarpetas_completas = {nombre: join(ruta_dia, nombre) for nombre in subcarpetas}
            resultado["dias_rastreos"][dia_corregido] = {
                "subcarpetas": subcarpetas_completas
            }

        if not resultado["dias_rastreos"]:
            msj = "Ningún día tiene subcarpetas válidas."
            agregar_log(msj)
            return msj, "dias_Rastreos_vacios"

        agregar_log("Procesamiento completado exitosamente.")
        return None, resultado

    except Exception as e:
        msj = f"Error al procesar días de rastreos: {e}"
        return msj, None

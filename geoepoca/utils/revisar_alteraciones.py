# ===========================
# Consolidado único NAV+FIX (join por DÍA + NOMBRE)
# Salida (con encabezados): PUNTO | X | Y | Z | F_RASTREO | F_REFERENCIA
# Reglas:
#   - Recorrer Reportes/ddmmaa
#   - Exigir subcarpetas NAVEGADO y FIX con NAV.xlsx y FIX.xlsx (nombres exactos)
#   - Emparejar por (ddmmaa, NOMBRE)  -> inner join
#   - Columnas de salida y orden:
#       1) PUNTO         -> "ddmmaa-NOMBRE" (usar NOMBRE de NAV)
#       2) X, 3) Y, 4) Z -> últimas 3 columnas de FIX (en ese orden)
#       5) F_RASTREO     -> segunda columna de NAV (col 1)
#       6) F_REFERENCIA  -> "01/01/2018" (constante)
#   - Logs cortos
#   - Si falta ruta/archivo o no hay filas finales -> False
# ===========================

from monitor.log.log import agregar_log
import os
import pandas as pd


def consolidado_nav_fix_unico(ruta_proyecto: str):
    # ----- Rutas base -----
    carpeta_reportes = os.path.join(ruta_proyecto, "Procesamiento", "1. Topografia", "Reportes")
    carpeta_salida   = os.path.join(ruta_proyecto, "Procesamiento", "1. Topografia", "Cambio de Epoca")

    # ----- Validaciones iniciales -----
    if not os.path.isdir(carpeta_reportes):
        agregar_log("No 'Reportes'")
        return False
    try:
        os.makedirs(carpeta_salida, exist_ok=True)
    except Exception as e:
        agregar_log(f"No 'Cambio de Epoca': {e}")
        return False

    filas_total = []
    agregar_log("Scan ddmmaa...")

    # ----- Helper: archivo exacto (case-insensitive) -----
    def _buscar_archivo_exact(carpeta, nombre_objetivo):
        try:
            for f in os.listdir(carpeta):
                if f.lower() == nombre_objetivo.lower():
                    return os.path.join(carpeta, f)
        except Exception as e:
            agregar_log(f"List err: {e}")
        return None

    # ----- Recorrer días (carpetas ddmmaa) -----
    for nombre_carpeta in sorted(os.listdir(carpeta_reportes)):
        ruta_dia = os.path.join(carpeta_reportes, nombre_carpeta)
        # Solo carpetas con 6 dígitos (ddmmaa)
        if not (os.path.isdir(ruta_dia) and nombre_carpeta.isdigit() and len(nombre_carpeta) == 6):
            continue

        agregar_log(f"Día {nombre_carpeta}")

        # Subcarpetas requeridas
        ruta_nav = os.path.join(ruta_dia, "NAVEGADO")
        ruta_fix = os.path.join(ruta_dia, "FIX")
        if not os.path.isdir(ruta_nav):
            agregar_log(f"Sin NAVEGADO {nombre_carpeta}")
            return False
        if not os.path.isdir(ruta_fix):
            agregar_log(f"Sin FIX {nombre_carpeta}")
            return False

        # Archivos requeridos
        nav_xlsx = _buscar_archivo_exact(ruta_nav, "NAV.xlsx")
        fix_xlsx = _buscar_archivo_exact(ruta_fix, "FIX.xlsx")
        if not (nav_xlsx and os.path.isfile(nav_xlsx)):
            agregar_log(f"Sin NAV.xlsx {nombre_carpeta}")
            return False
        if not (fix_xlsx and os.path.isfile(fix_xlsx)):
            agregar_log(f"Sin FIX.xlsx {nombre_carpeta}")
            return False

        # ----- Leer NAV.xlsx -----
        try:
            df_nav_raw = pd.read_excel(nav_xlsx, header=None)
            if df_nav_raw.empty:
                agregar_log(f"NAV vacío {nombre_carpeta}")
                return False
            if df_nav_raw.shape[1] < 2:
                agregar_log(f"NAV < 2 cols {nombre_carpeta}")
                return False

            # Claves para emparejar
            nombre_nav = df_nav_raw.iloc[:, 0].astype(str).fillna("").str.strip()
            # Para salida (F_RASTREO)
            nav_segunda = df_nav_raw.iloc[:, 1]

            # Data mínima para merge
            nav_merge = pd.DataFrame({
                "__DIA__": nombre_carpeta,
                "__NOMBRE__": nombre_nav,
                "__NAV2__": nav_segunda
            })

            agregar_log(f"NAV ok {df_nav_raw.shape[0]}")
        except Exception as e:
            agregar_log(f"NAV err {nombre_carpeta}: {e}")
            return False

        # ----- Leer FIX.xlsx -----
        try:
            df_fix_raw = pd.read_excel(fix_xlsx, header=None)
            if df_fix_raw.empty:
                agregar_log(f"FIX vacío {nombre_carpeta}")
                return False
            if df_fix_raw.shape[1] < 3:
                agregar_log(f"FIX < 3 cols {nombre_carpeta}")
                return False

            # Claves para emparejar
            nombre_fix = df_fix_raw.iloc[:, 0].astype(str).fillna("").str.strip()

            # Tomar las últimas 3 columnas como X,Y,Z
            fix_last3 = df_fix_raw.iloc[:, -3:].copy()
            if fix_last3.shape[1] != 3:
                agregar_log("FIX != 3 cols fin")
                return False
            fix_last3.columns = ["__X__", "__Y__", "__Z__"]

            # Data mínima para merge
            fix_merge = fix_last3.copy()
            fix_merge.insert(0, "__NOMBRE__", nombre_fix)
            fix_merge.insert(0, "__DIA__", nombre_carpeta)

            agregar_log(f"FIX ok {df_fix_raw.shape[0]}")
        except Exception as e:
            agregar_log(f"FIX err {nombre_carpeta}: {e}")
            return False

        # ----- Emparejar por (DÍA, NOMBRE) -> inner -----
        try:
            joined = pd.merge(nav_merge, fix_merge, on=["__DIA__", "__NOMBRE__"], how="inner")
            if joined.empty:
                agregar_log(f"Sin match {nombre_carpeta}")
                # No es error: se omite este día
                continue

            # PUNTO debe ser "ddmmaa-NOMBRE"
            punto = (joined["__DIA__"] + "-" + joined["__NOMBRE__"]).astype(str)

            # Orden de salida:
            # PUNTO, X, Y, Z, F_RASTREO, F_REFERENCIA
            out_day = pd.DataFrame({
                "PUNTO": punto,
                "X": joined["__X__"],
                "Y": joined["__Y__"],
                "Z": joined["__Z__"],
                "F_RASTREO": joined["__NAV2__"],
                "F_REFERENCIA": "01/01/2018"
            })

            filas_total.append(out_day)
            agregar_log(f"Join ok {out_day.shape[0]}")
        except Exception as e:
            agregar_log(f"Join err {nombre_carpeta}: {e}")
            return False

    # ----- Guardar único consolidado -----
    if not filas_total:
        agregar_log("Sin filas finales")
        return False

    try:
        df_out = pd.concat(filas_total, ignore_index=True)
        ruta_out = os.path.join(carpeta_salida, "consolidado.xlsx")
        df_out.to_excel(ruta_out, index=False, header=True)  # con encabezados
        agregar_log("Consolidado guardado")
    except Exception as e:
        agregar_log(f"Save err: {e}")
        return False

    return ruta_out

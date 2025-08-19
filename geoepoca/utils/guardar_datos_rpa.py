# ===========================
# Guardar Excel como CSV para RPA
# - Recibe la ruta a un Excel (.xlsx/.xls/.xlsm)
# - Crea la carpetación en C:\0 - GEOEPOCA\
# - En "0 - {AÑO}" guarda el contenido del Excel como CSV: "{AÑO}.csv"
# - Logs cortos, retorna True si todo ok, None en error
# ===========================

from monitor.log.log import agregar_log
import os
from datetime import datetime
import pandas as pd


def guardar_excel_para_rpa(ruta_excel: str):
    try:
        agregar_log("🟡 Inicio RPA")

        # 1) Validaciones de entrada
        if not isinstance(ruta_excel, str) or not ruta_excel.strip():
            agregar_log("❌ Ruta inválida")
            return None

        ruta_excel = ruta_excel.strip()

        if not os.path.isfile(ruta_excel):
            agregar_log("❌ No existe archivo")
            return None

        ext = os.path.splitext(ruta_excel)[1].lower()
        if ext not in (".xlsx", ".xls", ".xlsm"):
            agregar_log("❌ No es Excel")
            return None

        # 2) Leer Excel
        try:
            # Lee primera hoja por defecto, usa primera fila como encabezado
            df = pd.read_excel(ruta_excel, header=0)
        except Exception as e:
            agregar_log(f"❌ Error lectura: {e}")
            return None

        if df is None or df.empty:
            agregar_log("❌ Excel vacío")
            return None

        agregar_log(f"✅ Leído {df.shape[0]}x{df.shape[1]}")

        # 3) Crear carpetación destino
        anio_actual = datetime.now().year
        ruta_base = r"C:\0 - GEOEPOCA"

        carpetas = [
            f"0 - {anio_actual}",
            "1 - 2018",
            "2 - ELIPSOIDAL-2018",
            "3 - CTM-2018",
            "4 - OND -2018",
            "5 - VELOCI-2018",
            "6 - COORD-FINALES-2018"
        ]

        for nombre in carpetas:
            ruta = os.path.join(ruta_base, nombre)
            try:
                os.makedirs(ruta, exist_ok=True)
            except Exception as e:
                agregar_log(f"❌ Carpeta err: {e}")
                return None
            agregar_log(f"📁 OK {ruta}")

        # 4) Guardar CSV en la primera carpeta ("0 - {AÑO}")
        carpeta_csv = os.path.join(ruta_base, f"0 - {anio_actual}")
        archivo_csv = os.path.join(carpeta_csv, f"{anio_actual}.csv")

        try:
            # Guarda con encabezados y sin índice
            df.to_csv(archivo_csv, index=False, encoding="utf-8-sig")
        except Exception as e:
            agregar_log(f"❌ Guardar err: {e}")
            return None

        agregar_log(f"✅ CSV: {archivo_csv}")
        return True

    except Exception as e:
        agregar_log(f"❌ Error inesperado: {e}")
        return None

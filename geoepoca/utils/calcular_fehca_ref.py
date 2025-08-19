from monitor.log.log import agregar_log
import pandas as pd
from datetime import datetime
import time

def calculo_fehca_ref(ruta_navegado):
    try:
        agregar_log("📄 Iniciando lectura del archivo Excel...")

        df = pd.read_excel(ruta_navegado, header=None)
        agregar_log(f"✅ Excel cargado correctamente con {len(df)} filas y {len(df.columns)} columnas.")

        fechas_raw = df.iloc[:, -2]  # Antepenúltima columna
        agregar_log(f"📦 Se leerán {len(fechas_raw)} valores desde la antepenúltima columna.")

        fechas_final = []

        for i, f in enumerate(fechas_raw):
            try:
                valor_original = repr(f)
                agregar_log(f"🔍 Fila {i}: valor crudo = {valor_original}")

                fecha = pd.to_datetime(str(f).strip(), dayfirst=True)
                fecha_formateada = fecha.strftime("%d/%m/%Y")
                fechas_final.append(fecha_formateada)

                agregar_log(f"✅ Fila {i}: fecha válida → {fecha_formateada}")
            except Exception as e:
                agregar_log(f"⚠️ Fila {i}: error al convertir '{f}' → {e}")

        agregar_log(f"📋 Total fechas válidas extraídas: {len(fechas_final)}")
        #time.sleep(500)
        return fechas_final

    except Exception as e:
        agregar_log(f"❌ Error general al extraer fechas del Excel: {e}")
        return None

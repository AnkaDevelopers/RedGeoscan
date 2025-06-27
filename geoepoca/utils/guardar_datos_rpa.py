# Importar módulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
from datetime import datetime
import pandas as pd

def guardar_datos_para_rpa(datos_rpa):

    try:
        agregar_log("🟡 Iniciando proceso de guardado de datos para RPA...")

        # Verificación mínima
        if not isinstance(datos_rpa, list) or len(datos_rpa) < 2:
            agregar_log("❌ Error: Los datos no tienen suficiente información o no son una lista válida.")
            return None

        # Convertir a DataFrame
        encabezados = datos_rpa[0]
        datos = datos_rpa[1:]
        df = pd.DataFrame(datos, columns=encabezados)
        agregar_log("✅ Datos convertidos correctamente a DataFrame.")

        # Año actual
        anio_actual = datetime.now().year

        # Ruta base
        ruta_base = r"C:\0 - GEOEPOCA"

        # Crear carpetas requeridas
        carpetas = [
            f"0 - {anio_actual}",
            "1 - 2018",
            "2 - ELIPSOIDAL-2018",
            "3 - CTM-2018",
            "4 - OND -2018",
            "5 - VELOCI-2018",
            "6 - COORD-FINALES-2018"
        ]

        for carpeta in carpetas:
            ruta = os.path.join(ruta_base, carpeta)
            os.makedirs(ruta, exist_ok=True)
            agregar_log(f"📁 Carpeta verificada/creada: {ruta}")

        # Ruta final del archivo CSV
        archivo_csv = os.path.join(ruta_base, f"0 - {anio_actual}", f"{anio_actual}.csv")

        # Guardar el CSV
        df.to_csv(archivo_csv, index=False, encoding='utf-8-sig')
        agregar_log(f"✅ Archivo CSV guardado correctamente en: {archivo_csv}")

        return True

    except Exception as e:
        agregar_log(f"❌ Error inesperado al guardar el archivo: {e}")
        return None

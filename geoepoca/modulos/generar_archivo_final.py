# Importar módulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
import pandas as pd
from datetime import datetime
import shutil

def procesar_y_calcular(ruta_base_proyecto):
    try:
        agregar_log("🔄 Iniciando procesamiento de archivos GEOEPOCA...\n")

        # Carpeta fija de donde se leen los datos
        ruta_origen = r"C:\0 - GEOEPOCA"
        agregar_log(f"📂 Carpeta origen definida: {ruta_origen}")

        # Definición de carpetas y nombres de hojas
        anio_actual = datetime.now().year
        carpetas = [
            f"0 - {anio_actual}",
            "1 - 2018",
            "2 - ELIPSOIDAL-2018",
            "3 - CTM-2018",
            "4 - OND -2018",
            "5 - VELOCI-2018",
        ]
        nombres_hojas = [
            f"EPOCA - {anio_actual}",
            "EPOCA - 2018",
            "ELIPSOIDAL-2018",
            "CTM-2018",
            "OND -2018",
            "VELOCI-2018",
        ]

        data_frames = {}

        for idx, carpeta in enumerate(carpetas):
            ruta_carpeta = os.path.join(ruta_origen, carpeta)
            agregar_log(f"📁 Leyendo carpeta: {ruta_carpeta}")

            if not os.path.isdir(ruta_carpeta):
                raise FileNotFoundError(f"No se encontró la carpeta: {ruta_carpeta}")

            archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith('.csv')]
            if not archivos:
                raise FileNotFoundError(f"No se encontró ningún archivo .csv en: {ruta_carpeta}")

            ruta_archivo = os.path.join(ruta_carpeta, archivos[0])
            agregar_log(f"📄 Archivo CSV detectado: {ruta_archivo}")

            df = None
            for encoding in (None, 'latin1', 'cp1252'):
                try:
                    if idx in (0, 5):
                        df = pd.read_csv(ruta_archivo, encoding=encoding) if encoding else pd.read_csv(ruta_archivo)
                    else:
                        df = pd.read_csv(ruta_archivo, usecols=range(4), encoding=encoding) if encoding else pd.read_csv(ruta_archivo, usecols=range(4))
                    agregar_log(f"✅ Archivo leído correctamente con codificación: {encoding}")
                    break
                except (UnicodeDecodeError, TypeError):
                    continue
            if df is None:
                raise UnicodeDecodeError("No se pudo decodificar el archivo CSV en ninguna codificación.", ruta_archivo, 0, 1, "encoding")

            data_frames[nombres_hojas[idx]] = df

        # Cálculo de ALTURA-ORTOMETRICA
        agregar_log("🧮 Calculando ALTURA-ORTOMETRICA...")
        df_ctm = data_frames['CTM-2018']
        df_ond = data_frames['OND -2018']
        df_alt = df_ctm.copy()
        ond_col = df_ond.iloc[:, 3].reset_index(drop=True)
        df_alt['Ondulacion'] = ond_col
        df_alt['ALTURA-ORTOMETRICA'] = df_alt['Altura'] - df_alt['Ondulacion']
        data_frames['ALTURA-ORTOMETRICA'] = df_alt
        agregar_log("✅ Cálculo completado.\n")

        # Ruta de salida
        ruta_destino = os.path.join(ruta_base_proyecto, r"Procesamiento\1. Topografia\Cambio de epoca")
        os.makedirs(ruta_destino, exist_ok=True)
        resultado_path = os.path.join(ruta_destino, 'COORD-FINALES-2018.xlsx')
        agregar_log(f"💾 Guardando archivo Excel en: {resultado_path}")

        with pd.ExcelWriter(resultado_path, engine='openpyxl') as writer:
            for hoja, df in data_frames.items():
                df.to_excel(writer, sheet_name=hoja, index=False)

        agregar_log("✅ Archivo Excel generado exitosamente.\n")

        # Eliminar carpeta original
        agregar_log(f"🗑️ Eliminando carpeta original: {ruta_origen}")
        shutil.rmtree(ruta_origen)
        agregar_log("✅ Carpeta eliminada correctamente.\n")

        agregar_log("🎉 Proceso finalizado sin errores.\n")
        return resultado_path

    except Exception as e:
        agregar_log(f"❌ Error al procesar y calcular: {e}")
        return None

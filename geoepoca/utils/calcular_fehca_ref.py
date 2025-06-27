# Importar módulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import pandas as pd
from datetime import datetime

def calculo_fehca_ref(ruta_navegado):
    try:
        agregar_log("Iniciando lectura del archivo Excel.")

        # Leer el archivo Excel, solo hasta la columna N (índice 13)
        df = pd.read_excel(ruta_navegado, usecols="A:N")
        agregar_log(f"Archivo leído correctamente con {len(df)} filas.")

        # Extraer la columna N (última columna)
        fechas_con_hora = df.iloc[:, -1].dropna()
        agregar_log(f"Se extrajeron {len(fechas_con_hora)} fechas con hora.")

        # Convertir a datetime (manejo de errores con 'coerce')
        fechas = pd.to_datetime(fechas_con_hora, errors='coerce', dayfirst=True).dropna()
        agregar_log(f"{len(fechas)} fechas convertidas exitosamente a formato datetime.")

        # Eliminar la hora, dejando solo la fecha
        fechas_sin_hora = fechas.dt.normalize().drop_duplicates()
        agregar_log(f"{len(fechas_sin_hora)} fechas únicas sin hora obtenidas.")

        # Ordenar las fechas
        fechas_ordenadas = sorted(fechas_sin_hora)
        agregar_log(f"Fechas ordenadas: {[f.strftime('%d/%m/%Y') for f in fechas_ordenadas]}")

        # Calcular el índice central
        medio_idx = len(fechas_ordenadas) // 2
        fecha_ref = fechas_ordenadas[medio_idx - 1 if len(fechas_ordenadas) % 2 == 0 else medio_idx]

        resultado = fecha_ref.strftime("%d/%m/%Y")
        agregar_log(f"Fecha de referencia calculada: {resultado}")

        return resultado

    except Exception as e:
        agregar_log(f"Error al calcular la fecha de referencia: {str(e)}")
        return None

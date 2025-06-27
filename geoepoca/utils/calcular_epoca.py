# Importar módulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
from datetime import datetime

def calcular_dia_gps_y_epoca(fecha_str):
    """
    Recibe una fecha en formato DD/MM/AAAA, calcula el día GPS y la época 2018.
    Retorna una tupla (dia_gps, epoca) o (None, None) si hay error.
    """
    try:
        agregar_log(f"📥 Fecha recibida como parámetro: {fecha_str}")

        # Convertir la fecha a objeto datetime usando formato con año de 4 dígitos
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        agregar_log(f"📅 Fecha convertida correctamente: {fecha.strftime('%Y-%m-%d')}")

        anio = fecha.year

        # Calcular día GPS
        dia_gps = fecha.timetuple().tm_yday
        agregar_log(f"🛰 Día GPS calculado: {dia_gps}")

        # Verificar si el año es bisiesto
        es_bisiesto = (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
        dias_en_anio = 366 if es_bisiesto else 365
        agregar_log(f"📆 Año {anio} {'es' if es_bisiesto else 'no es'} bisiesto. Días en el año: {dias_en_anio}")

        # Calcular época respecto al año base 2018
        epoca = round((anio + (dia_gps / dias_en_anio)) - 2018, 6)
        agregar_log(f"📐 Época calculada respecto a 2018: {epoca}")

        return dia_gps, epoca

    except ValueError:
        msg = f"❌ Fecha inválida: '{fecha_str}'. Usa el formato DD/MM/AAAA"
        print(msg)
        agregar_log(msg)
        return None, None

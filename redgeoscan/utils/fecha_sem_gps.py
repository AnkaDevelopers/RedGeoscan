# Importaciones adicionales
from datetime import datetime

# funcion para convertir una fecha en semana gps y en dia del año
def fecha_a_semana_gps(fecha_str):
    # Definir la fecha de inicio de la época GPS
    epoca_gps = datetime(1980, 1, 6)

    # Convertir la fecha de entrada a un objeto datetime
    fecha = datetime.strptime(fecha_str, "%Y/%m/%d %H:%M:%S.%f")
    # Calcular la diferencia en días
    diferencia = fecha - epoca_gps
    dias_gps = diferencia.days  # Obtener días completos
    semanas_gps = dias_gps // 7  # Obtener semanas completas

    # Obtener el día del año
    dia_del_año = fecha.timetuple().tm_yday  # Día del año

    return semanas_gps, dia_del_año
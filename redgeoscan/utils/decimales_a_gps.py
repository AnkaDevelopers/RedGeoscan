# Convertir a grados, minutos y segundos con redondeo en segundos
def decimales_a_gms(decimal):
    grados = int(decimal)
    minutos_decimales = abs((decimal - grados) * 60)
    minutos = int(minutos_decimales)
    segundos = round((minutos_decimales - minutos) * 60, 2)  # Redondear a 4 decimales
    return grados, minutos, segundos
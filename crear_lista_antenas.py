from calculos import decimales_a_gms

def insertar_datos_antenas(tabla_antenas, antenas_con_rinex):

    #limpioar la tabla
    for item in tabla_antenas.get_children():
        tabla_antenas.delete(item)
    longitud_datos = len(antenas_con_rinex)
    for i in range(longitud_datos):
        nombre = antenas_con_rinex[i] ['NAME']
        lat_g, lat_m, lat_s = decimales_a_gms(antenas_con_rinex[i] ['Latitud (Decimal)'])
        lon_g, lon_m, lon_s = decimales_a_gms(antenas_con_rinex[i] ['Longitud (Decimal)'])
        distancia = f"{round(antenas_con_rinex[i] ['Distancia'])} 'km'"
    
        # Insertar los datos de las antenas en la tabla de antenas mas cercanas
        tabla_antenas.insert("", "end", values=(
            nombre,
         f"{lat_g}° {lat_m}' {lat_s:.2f}\"",
            f"{lon_g}° {lon_m}' {lon_s:.2f}\"",
         distancia
        ))        

    return
from calculos import decimales_a_gms
import openpyxl
import os

ruta_principal = None

def insertar_datos_antenas(tabla_antenas, antenas_con_rinex, ruta):
    global ruta_principal
    ruta_principal = ruta

    # Limpiar la tabla
    for item in tabla_antenas.get_children():
        tabla_antenas.delete(item)

    # Crear una lista para almacenar los datos que se exportarán
    datos_para_exportar = []

    # Insertar datos en la tabla y prepararlos para exportar
    longitud_datos = len(antenas_con_rinex)
    for i in range(longitud_datos):
        nombre = antenas_con_rinex[i]['NAME']
        lat_g, lat_m, lat_s = decimales_a_gms(antenas_con_rinex[i]['Latitud (Decimal)'])
        lon_g, lon_m, lon_s = decimales_a_gms(antenas_con_rinex[i]['Longitud (Decimal)'])
        distancia = f"{round(antenas_con_rinex[i]['Distancia'], 2)} km"
        administrador = antenas_con_rinex[i]['ADMINISTRADOR']

        # Insertar los datos de las antenas en la tabla de antenas más cercanas
        tabla_antenas.insert("", "end", values=(
            nombre,
            f"{lat_g}° {lat_m}' {lat_s:.2f}\"",
            f"{lon_g}° {lon_m}' {lon_s:.2f}\"",
            distancia,
            administrador
        ))

        # Preparar datos para exportar
        datos_para_exportar.append([
            nombre,
            f"{lat_g}° {lat_m}' {lat_s:.2f}\"",
            f"{lon_g}° {lon_m}' {lon_s:.2f}\"",
            distancia,
            administrador
        ])

    # Exportar los datos a un archivo Excel
    exportar_datos_a_excel(datos_para_exportar, ruta)

def exportar_datos_a_excel(datos, ruta_base):

    try:
        # Crear la ruta completa de la carpeta 'excelantenas'
        ruta_carpeta = os.path.join(ruta_base, "1 - LISTA_ANTENAS_CERCANAS")
        
        # Crear la carpeta si no existe
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
            print(f"Carpeta creada: {ruta_carpeta}")
        else:
            print(f"Carpeta ya existente: {ruta_carpeta}")

        # Definir la ruta completa del archivo Excel
        archivo_excel = os.path.join(ruta_carpeta, "lista de antenas descargadas.xlsx")

        # Crear un libro de trabajo
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Antenas Más Cercanas"

        # Escribir encabezados
        encabezados = ["Nombre", "Latitud", "Longitud", "Distancia", "Administrador"]
        ws.append(encabezados)

        # Escribir los datos
        for fila in datos:
            ws.append(fila)

        # Guardar el archivo en la ruta especificada
        wb.save(archivo_excel)
        print(f"Datos exportados exitosamente a: {archivo_excel}")

    except Exception as e:
        print(f"Error al exportar los datos a Excel: {e}")
        print("Detalles del error:", repr(e))

#******************************************************
# Variables globales Rutas específica del proyecto

# Ruta del proyecto REDGEOSCAN
ruta_proyecto = r"C:\redGeoScan"

# Ruta del RTKLIB
ruta_rtk = r"C:\RTKLIB_v2.4.3_B33"

# Ruta base para descargas
ruta_descargas = r"C:\Users\camil-code\Desktop"

#******************************************************
# Variables globales Rutas específica del proyecto

# Nombre del archivo ejecutable del programa RTKLIB
nombre_exe = "rtkpost_win64.exe"

# Nombre del archivo KML esperado en el proyecto
nombre_archivo_kml = "KML.xlsx"

#******************************************************
# Variables globales Rutas específica del proyecto

# URL del servicio antenas igac
antenas_igac = (
    "https://serviciosgeovisor.igac.gov.co:8080/Geovisor/geodesia?draw=1&columns%5B0%5D%5Bdata%5D=ID_ESTACION&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=ID_ESTACION&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=ID_ESTACION&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=ID_ESTACION&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=ID_ESTACION&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=ID_ESTACION&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=254&search%5Bvalue%5D=&search%5Bregex%5D=false&cmd=query_estaciones&tipo=Activa&administrador=&estacion="
)

#******************************************************
# Variables globales mensajes depuracion componentes

# Mesajes de estado base de antenas kml
msj_kml = [
    "No se encontró el archivo KML en la carpeta del proyecto."
    "La selección de la base de antenas ha sido cancelada.",
    "La base de antenas se ha cargado correctamente.",
    "La base de antenas se ha cargado satisfactoriamente.",
    "No se pudo guardar la base de antenas."
]

# Mensajes de estado funcion de selección de proyecto
msj_select_proyect = [
    "Selecciona la carpeta de tu proyecto",
    "Usuario selecciono la carpeta del proyecto:",
    "La carpeta seleccionada no cumple el estadar",
    "No se encontro ninguna carpeta en la ruta: ",
    "No se encontro el archivo con extención: ",
    "No se selecciono ninguna carpeta.",
    "La ruta no es un directorio: ",
    "Sub carpeta encontradas en esta ruta: ",
    "Carpeta seleccioanda: ",
    "Error al seleccionar una sub carpeta",
    "La ruta no existe",
    "No se encontro el archivo con extencion: ",
    "La ruta completa del archivo es :",
    "Archivo .pos ya existe en la ruta: "
]

# Mensajes estado componente buscador de carpetas
msj_buscador_carpetas =[
    "La ruta no existe: ",
    "Directorio '6. TOPOGRAFIA' no se encontro en: ",
    "Directorio 'RASTREOS' no se encontro en: ",
    "Directorio 'RASTREOS' en esta ruta: ",
    "Directorio con nombre de 'Fecha' encontrada en ruta:",
    "Directorio con nombre de 'Fecha' no encontrada (101024) en ruta:",
    "Directorio 'RED ACTIVA'no de encotro en: ",
    "Ruta Final encontrada: ",
    "Explorando:"
]

# Mensajes de estado de base archivo pos
msj_pos = [
    "Línea ignorada por error en conversión",
    "No se seleccionó ningún archivo. Salida de la función.",
    "No se encontraron datos válidos en el archivo POS",
    "El archivo .POS se ha cargado correctamente.",
    "El archivo .POS seleccionado no cumple con los requisitos."
]

# Mensajes main
msj_main = [
    "Archivo KML Vacio",
    "Archivo KML cargado Exitosamente",
    "No se selecciono ningun Proyecto",
    "Hubo un error en calcular la coordenada media base",
]
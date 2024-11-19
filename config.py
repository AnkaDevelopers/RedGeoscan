# Ruta específica del proyecto
ruta_proyecto = r"C:\redGeoScan"

# Nombre del archivo KML esperado en el proyecto
nombre_archivo_kml = "KML.xlsx"

# Mesajes de estado base de antenas kml
msj_kml = [
    "La base de antenas se ha cargado correctamente.",
    "La selección de la base de antenas ha sido cancelada.",
    "La base de antenas se ha cargado en la carpeta del proyecto.",
    "No se pudo guardar la base de antenas."
]

# Mensajes de estado de base archivo pos
msj_pos = [
    "Línea ignorada por error en conversión",
    "No se seleccionó ningún archivo. Salida de la función.",
    "No se encontraron datos válidos en el archivo POS",
    "El archivo POS se ha cargado correctamente."
]

# URL del servicio antenas igac
antenas_igac = (
    "https://serviciosgeovisor.igac.gov.co:8080/Geovisor/geodesia?draw=1&columns%5B0%5D%5Bdata%5D=ID_ESTACION&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=ID_ESTACION&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=ID_ESTACION&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=ID_ESTACION&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=ID_ESTACION&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=ID_ESTACION&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=254&search%5Bvalue%5D=&search%5Bregex%5D=false&cmd=query_estaciones&tipo=Activa&administrador=&estacion="
)

# Ruta base para descargas
ruta_descargas = r"C:\Users\camil-code\Desktop"

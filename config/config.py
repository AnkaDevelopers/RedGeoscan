#************************************************************************************************************
# RUTAS DOCS NECESARIOS

# Ruta Cola proyectos
ruta_excel = r"C:\RedGeoscan\docs\Cola_proyectos.xlsx"

# Ruta Cola antenas
ruta_kml = r"C:\RedGeoscan\docs\kml_antenas.xlsx"

#************************************************************************************************************
# RPA RTKLIB

# Ruta del RTKLIB
ruta_rtk = r"C:\RTKLIB_v2.4.3_B33"

# Nombre del archivo ejecutable del programa RTKLIB
nombre_exe = "rtkpost_win64.exe"

#************************************************************************************************************
# RPA TOKEN PRINCIPAL

# Ruta de la página
ruta_gov = "https://www.colombiaenmapas.gov.co/?e=-74.19790397936877,4.606824129536961,-74.05594002062873,4.715639657991442,4686&b=igac&u=0&t=25&servicio=8#"

# Verifica la ruta del perfil de usuario
ruta_perfil = r"C:\Users\red-g\AppData\Local\Microsoft\Edge\User Data"
nombre_perfil = "Profile 1" #en la maquina virtual debe ser Default
webdriver_path = r"C:\Webdriver\msedgedriver.exe"
target_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo"

# Ruta archivo .txt donde alamacenamos el token principal
ruta_token = r"C:\RedGeoscan\docs"

#************************************************************************************************************
# SERVICIOS ANKAPLANNER

# CONSULTAR TODOS LOS PROYECTOS
api_allProyects = "http://192.168.1.12:3000/api/proyectos"

# ACTUALIZAR ESTADOS PROYECTOS
api_putProyects = "http://192.168.1.12:3000/api/proyectos"

#************************************************************************************************************
# CORREOS EQUIPO DE SOPORTE

# CORREO1
correoDesarrollo = "cristian.c.castillo1707@gmail.com"
correoTopografos = "ankalidarcol@gmail.com"

#************************************************************************************************************
# REPORTES REDGEOSCAN:
ruta_img_para_reporte: r'C:\RedGeoscan\data\logo_anka.jpg' 

#************************************************************************************************************
# RUTA A LOG GLOBAL:
ruta_a_log: r'C:\RedGeoscan'

# RUTA A DOCS
ruta_a_docs : r"C:\RedGeoscan\docs" 
#************************************************************************************************************
# Ruta del archivo Excel
ruta_excel = [r"Z:\1 - CAPTURADOR DE RUTAS\RutaList",r"C:\bot-auto\docs"]

# Nombres archivos Excel
nombre_archivo_excel = ["Cola_proyectos.xlsx", "kml_antenas.xlsx"]

# Mensajes de respuesta para correos
mensaje_respuesta = (
    "Hola {remitente},\n\n"
    "La ruta que enviaste ya ha sido registrada y está en cola para ser procesada.\n"
    "En las próximas horas recibirás información sobre el progreso.\n\n"
    "Saludos cordiales,\nEquipo de Desarrollo"
)

# Mensaje en caso de que un proyecto ya esté en cola
mensaje_proyecto_en_cola = (
    "Hola {remitente},\n\n"
    "Hemos detectado que la ruta que enviaste corresponde a un proyecto que ya está en cola desde el {fecha}. "
    "Este proyecto fue enviado previamente por el/la Sr./Sra. {emisor}.\n\n"
    "Gracias por tu comprensión,\nEquipo de Desarrollo"
)

# Mensaje de error para casos de monitoreo fallido (si deseas usarlo en el futuro)
mensaje_error_ruta = (
    "Hola {remitente},\n\n"
    "Hemos detectado un problema al procesar la información que enviaste. "
    "Por favor, verifica la integridad de la ruta y vuelve a enviarla.\n\n"
    "Gracias por tu colaboración,\nEquipo de Desarrollo"
)

# Mensaje de error para casos de monitoreo fallido (si deseas usarlo en el futuro)
mensaje_error_monitoreo = (
    "Hola {remitente},\n\n"
    "Hemos detectado un problema al procesar la información que enviaste. "
    "Por favor, asegúrate de que la estructura del correo cumpla con el formato requerido y vuelve a enviarlo.\n\n"
    "Gracias por tu colaboración,\nEquipo de Desarrollo"
)

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
# Verifica la ruta del perfil de usuario
ruta_perfil = r"C:\Users\red-g\AppData\Local\Microsoft\Edge\User Data"
nombre_perfil = "Default"
webdriver_path = r"C:\Webdriver\msedgedriver.exe"
target_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo"

# Ruta archivo .txt donde alamacenamos el token principal
ruta_token = r"C:\\bot-auto\\docs\\"
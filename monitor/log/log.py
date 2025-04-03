# Importaciones de módulos
from monitor.firma.firma import construir_firma_html 

# Importaciones adicionales
from win32com.client import Dispatch
from datetime import datetime
import os

# ************************************************************************************************************
# Variable global para almacenar los logs
log_info = []
log_file = None

# ************************************************************************************************************
# Función para agregar mensajes al log
def agregar_log(mensaje):
    
    global log_info
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_info.append(f"{timestamp} - {mensaje}")
    
    # mensaje de depuracion en la consola
    print(f"{timestamp} - {mensaje}") 

# ************************************************************************************************************
# Función para guardar los logs en un archivo
def guardar_log_en_archivo(name_log):
    global log_file

    try:
        # Establecer la ruta absoluta del directorio de logs
        log_dir = os.path.join("C:\\bot-auto", "log")

        # Crear el directorio si no existe
        print(f"Intentando crear el directorio de log en: {log_dir}")
        os.makedirs(log_dir, exist_ok=True)

        # Definir la ruta del archivo log
        log_file = os.path.join(log_dir, f"{name_log}.txt")
        
        # Imprimir información del archivo log
        print(f"Ruta completa del archivo log: {log_file}")

        # Comprobar permisos de escritura
        if not os.access(log_dir, os.W_OK):
            raise PermissionError("No se tienen permisos de escritura en el directorio de logs.")

        # Guardar el log en el archivo
        with open(log_file, "w", encoding="utf-8") as archivo:
            archivo.write("\n".join(log_info))

        print("Log guardado correctamente en el archivo.")
    
    except Exception as e:
        print(f"Error al guardar el log en archivo: {type(e).__name__}: {e}")


# ************************************************************************************************************
# Función para enviar el log por correo
def enviar_log_por_correo(motivo):

    try:
        # Configuración del correo
        remitente = "red-geo-scan@hotmail.com" 
        destinatario = "redgeoscan@groups.outlook.com" 
        asunto = f"{motivo} - {datetime.now().strftime('%d-%b-%Y %I:%M %p')}"

        if not log_file:
            print("No se pudo enviar el correo porque no se pudo generar el archivo de log.")
            return

        # Generar la firma HTML
        firma_html, ruta_imagen_local = construir_firma_html()

        # Crear y enviar correo
        outlook = Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # Nuevo correo
        mail.SentOnBehalfOfName = remitente
        mail.To = destinatario
        mail.Subject = asunto

        # Construir el cuerpo HTML del correo con firma
        mail.HTMLBody = f"""
        <p>Adjunto el log generado durante la ejecución del programa.</p>
        <br>
        {firma_html}
        """ + mail.HTMLBody

        # Adjuntar el archivo log
        mail.Attachments.Add(log_file)

        # Adjuntar la imagen embebida con Content-ID
        if ruta_imagen_local:
            adjunto = mail.Attachments.Add(ruta_imagen_local)
            property_accessor = adjunto.PropertyAccessor
            property_accessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "logo_anka"
            )

        # Enviar el correo
        mail.Send()
        print(f"Correo enviado correctamente al grupo '{destinatario}' desde '{remitente}'.")

    except Exception as e:
        mensaje_error = f"Error al enviar el log por correo: {e}"
        print(mensaje_error)

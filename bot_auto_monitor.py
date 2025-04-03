# Importaciones de módulos
from monitor.log.log import agregar_log, guardar_log_en_archivo, enviar_log_por_correo
from monitor.monitor_correos.monitor_correos import monitorear_correos
from monitor.guardar_excel.gestion_excel import inicializar_excel
from config import config

# Importaciones adicionales
import time
import datetime

# Variables globales
ruta_archivo_excel = config.ruta_excel
nombre_archivo_excel = config.nombre_archivo_excel[0]

# ************************************************************************************************************
# Programa principal
def programa_principal():
    # Crear o abrir el archivo Excel
    path_completo = inicializar_excel(nombre_archivo_excel)

    log_enviado_hoy = False
    fecha_actual = datetime.date.today()

    while True:
        try:
            # Guardar LOG
            agregar_log("Inicio Monitoreo")

            # Monitorear correos SIEMPRE
            monitorear_correos(path_completo)

            # Guardar LOG
            agregar_log("*" * 50 + "\n")

        except Exception as e:
            agregar_log(f"Error al monitorear correos: {e}")
            guardar_log_en_archivo("Proceso_monitoreo_correo")
            enviar_log_por_correo("Proceso_monitoreo_correo")

        # Verificar si son las 8:00 PM y aún no se ha enviado el log hoy
        ahora = datetime.datetime.now()
        if ahora.time().hour == 20 and not log_enviado_hoy:
            guardar_log_en_archivo("Proceso_monitoreo_correo")
            enviar_log_por_correo("Proceso_monitoreo_correo")
            log_enviado_hoy = True
            agregar_log("Log diario enviado a las 20:00")

        # Reiniciar la bandera si cambia el día
        if ahora.date() != fecha_actual:
            fecha_actual = ahora.date()
            log_enviado_hoy = False

        # Esperar 1 minuto antes de volver a monitorear
        time.sleep(60)

# Configuración para ejecutar al iniciar el PC
if __name__ == "__main__":
    programa_principal()

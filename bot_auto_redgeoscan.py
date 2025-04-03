# IMPORTACIONES MODULOS
#from monitor.guardar_excel.gestion_excel import inicializar_excel
from monitor.log.log import agregar_log, guardar_log_en_archivo, enviar_log_por_correo
from director_redgeoscan import control_redgeoscan
from config import config

# IMPORTACIONES ADICIONALES
import time
from datetime import datetime
from edge_utils import verificar_y_actualizar_edgedriver  

# Variables globales
ruta_archivo_excel = config.ruta_excel
nombre_archivo_excel = config.nombre_archivo_excel

# ************************************************************************************************************
# Proceso principal que ejecuta Redgeoscan TODO EL DÍA y guarda log tras cada ejecución
def programa_principal():
    # Inicializa Excel
    #inicializar_excel(nombre_archivo_excel)

    while True:
        hora_actual = datetime.now().hour  
        if 5 <= hora_actual < 22:  
            try:
                agregar_log("Verificando EdgeDriver...")  
                if verificar_y_actualizar_edgedriver(agregar_log):  
                    agregar_log("Inicio Redgeoscan")
                    control_redgeoscan(ruta_archivo_excel, nombre_archivo_excel)
                    agregar_log("Redgeoscan finalizado correctamente")
                else:
                    agregar_log("No se pudo verificar o actualizar el EdgeDriver.")
            except Exception as e:
                agregar_log(f"Error en Redgeoscan: {e}")
        else:
            agregar_log("Fuera del horario de ejecución (5am-12pm). Esperando...")  

        # Esperar 10 minutos antes de la siguiente ejecución
        time.sleep(60)

# ************************************************************************************************************
if __name__ == "__main__":
    programa_principal()

# IMPORTACIONES MODULOS
#from monitor.guardar_excel.gestion_excel import inicializar_excel
from monitor.log.log import agregar_log, guardar_log_en_archivo, enviar_log_por_correo
from director_redgeoscan import control_redgeoscan
from director_geoEpoca import control_verificacion_proyectos
from RutaList.rutaList import rutaList

# IMPORTACIONES ADICIONALES
import time
from datetime import datetime
from edge_utils import verificar_y_actualizar_edgedriver  


# ************************************************************************************************************
# Proceso principal que ejecuta Redgeoscan TODO EL DÍA y guarda log tras cada ejecución
def programa_principal():

    while True:
        hora_actual = datetime.now().hour  
        if 0 <= hora_actual: #< 25:  
            try:
                
                agregar_log("Verificando EdgeDriver...\n")  
                if verificar_y_actualizar_edgedriver(agregar_log):  
                    
                    agregar_log("Inicio actualizacion listado de proyectos\n")
                    rutaList()
                    
                    agregar_log("Inicio Redgeoscan")                                                                        
                    control_redgeoscan()
                    agregar_log("Redgeoscan finalizado correctamente\n")

                    agregar_log("Inicio GeoEpoca")
                    control_verificacion_proyectos()
                    agregar_log("GeoEpoca finalizado correctamente\n")


                else:
                    agregar_log("No se pudo verificar o actualizar el EdgeDriver.")
                    
            except Exception as e:
                agregar_log(f"Error: {e}")
        else:
            agregar_log("Fuera del horario de ejecución (5am-12pm). Esperando...")  

        # Esperar 1 minuto antes de la siguiente ejecución
        time.sleep(60)

# ************************************************************************************************************
if __name__ == "__main__":
    programa_principal()
                                    
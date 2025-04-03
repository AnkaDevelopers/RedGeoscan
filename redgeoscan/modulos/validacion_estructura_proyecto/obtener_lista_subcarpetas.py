# Importar modulos de monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
    
    
def obtener_lista_sub_carpetas(ruta_carpeta, carpeta):
    
    # Mensaje de depuración
    agregar_log(f"Obteniendo listado de subcarpetas de carpeta: {carpeta}")
    
    try:
        # Obtenemos todos los elementos en la ruta_carpeta y filtramos las carpetas
        carpetas = [d for d in os.listdir(ruta_carpeta) if os.path.isdir(os.path.join(ruta_carpeta, d)) and "-completo" not in d.lower()]

        
        # Verificar si se encontraron carpetas
        if not carpetas:
            msj = f"No se encontraron subcarpetas en la ruta o ya estan revisadas: {ruta_carpeta}"
            return msj, "completo"

        # Mensaje de depuración
        agregar_log("Listado de subcarpetas obtenido exitosamente")
        
        return None, carpetas
    
    except Exception as e:
        print("aca")
        msj = f"Hubo un error al intenar listar las subcarpetas: \n {e}"
        return msj, None
import os
import stat
import shutil
from pathlib import Path
import requests

# Importar configuraciones globales
from config.config import api_delete, api_allGps_proyect

def eliminar_proyecto_db(id_proyecto):
    # Formatear la URL con el ID del proyecto
    url = api_delete.format(id_proyecto=id_proyecto)
    
    # Hacer una solicitud DELETE al API
    try:
        response = requests.delete(url)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print(f"El proyecto con ID {id_proyecto} ha sido eliminado exitosamente.")
        else:
            print(f"Error al eliminar el proyecto con ID {id_proyecto}. Código de respuesta: {response.status_code}")
            print(f"Detalles: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error al intentar eliminar el proyecto: {e}")



def eliminar_proyecto(ruta: str) -> None:
    """
    Elimina la carpeta indicada por 'ruta' junto con todo su contenido.
    Maneja errores con try/except para evitar caídas.
    """
    try:
        p = Path(ruta).resolve()

        # Validar que exista
        if not p.exists():
            #print(f"❌ La ruta no existe: {p}")
            return

        # Evitar eliminar la raíz del sistema (/, C:\, etc.)
        if str(p) == p.anchor:
            print("⚠️ No se permite eliminar la raíz del sistema/unidad.")
            return

        # Si es un enlace simbólico, solo se elimina el enlace
        if p.is_symlink():
            p.unlink()
            print(f"✅ Enlace simbólico eliminado: {p}")
            return

        # Debe ser carpeta
        if not p.is_dir():
            print(f"❌ La ruta no es una carpeta: {p}")
            return

        # Función auxiliar para archivos de solo lectura
        def _handle_remove_readonly(func, path, exc_info):
            os.chmod(path, stat.S_IWRITE)
            func(path)

        # Eliminar la carpeta y subcarpetas
        shutil.rmtree(p, onerror=_handle_remove_readonly)
        print(f"✅ Carpeta eliminada correctamente: {p}")

    except Exception as e:
        print(f"❌ Error al eliminar la carpeta: {e}")


def obtener_numero_gps(id_proyecto):
    # Mensaje de depuración: mostrando el ID del proyecto
    print(f"Obteniendo el número de GPS para el proyecto con ID: {id_proyecto}")
    
    # Formatear la URL con el id_proyecto
    url = api_allGps_proyect.format(id_proyecto=id_proyecto)
    print(f"URL formada para la solicitud: {url}")
    
    try:
        # Hacer una solicitud GET al API
        print(f"Realizando la solicitud GET a la URL: {url}")
        response = requests.get(url)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print(f"Respuesta exitosa. Código de estado: {response.status_code}")
            # Suponiendo que la respuesta tiene el número de GPS
            datos = response.json()
            print(f"Datos recibidos: {datos}")
            
            # Retornar el número de GPS si está presente
            numero_gps = datos.get('numero_gps', 0)
            print(f"Número de GPS obtenido: {numero_gps}")
            return numero_gps
        else:
            print(f"Error al obtener el número de GPS. Código de respuesta: {response.status_code}")
            print(f"Detalles de la respuesta: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión o solicitud: {e}")
        return None
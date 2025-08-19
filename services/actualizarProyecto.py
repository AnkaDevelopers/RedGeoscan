# actualizarProyecto.py
import requests

# Importar configuraciones globales
from config import config

def actualizarProyecto(ID_PROYECTO, FECHA_CREACION= None ,RADIO_BUSQUEDA=None, ESTADO_RED=None, ESTADO_GEO=None):
    
    # 1) Validar insumos mínimos
    if ID_PROYECTO is None: 
        return None

    # 2) Armar URL final (PUT /api/proyectos/:id)
    url = f"{config.api_putProyects}/{ID_PROYECTO}"

    # 3) Armar cuerpo con solo los campos enviados
    payload = {}
    if FECHA_CREACION is not None:
        payload["fecha_creacion"] = FECHA_CREACION
    if RADIO_BUSQUEDA is not None:
        payload["radio_busqueda"] = RADIO_BUSQUEDA
    if ESTADO_RED is not None:
        payload["estado_red"] = ESTADO_RED
    if ESTADO_GEO is not None:
        payload["estado_geo"] = ESTADO_GEO

    # Si no hay nada que actualizar, no hacemos la petición
    if not payload:
        return None

    try:
        # 4) Consumir servicio (PUT)
        resp = requests.put(url, json=payload, timeout=5)

        # 5) Validar respuesta (tu controlador responde 200 en éxito)
        if resp.status_code == 200:
            return True
        else:
            return None

    except requests.ConnectionError:
        # No hay conexión con el servidor
        return None
    except Exception:
        # Cualquier otro error inesperado
        return None

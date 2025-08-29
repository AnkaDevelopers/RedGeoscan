# rutaList.py

# Módulos Ruta List
from RutaList.consumoServicioProyectos import consumoServicioProyectos
from RutaList.listarProyectos import listarProyectos

# Importar configuración y rutas
from config import config

# Importar módulos de monitor
from monitor.log.log import agregar_log, enviar_correo_personalizado

# Funcion encargada del Control de listado de proyectos
def rutaList():
    try:
        agregar_log("Iniciando rutaList - consumo API proyectos")

        # 1) Capturamos la respuesta del consumo
        response = consumoServicioProyectos(config.api_allProyects)
        agregar_log("Consumo API finalizado")

        # 2) Validación de los datos
        if len(response) == 0:  # Lista vacía
            agregar_log("Sin proyectos disponibles")
            return None
        if response is None:  # Error inesperado en el consumo
            agregar_log("Fallo el consumo de la API de proyectos")
            enviar_correo_personalizado(destinatario="camiloAnka@hotmail.com",  asunto="Falla consumo API", cuerpo_html="<p>Fallo el consumo de la API de proyectos.</p>")
            return None

        agregar_log(f"Proyectos obtenidos: {len(response)}")

        # 3) Listamos los proyectos
        confirmacionListado = listarProyectos(response, config.ruta_excel)
        agregar_log("Proceso de listado finalizado")

        # 4) Validación del listado
        if not confirmacionListado:
            agregar_log("Fallo en el listado de proyectos")
            return None

        # 5) Todo bien
        agregar_log("rutaList ejecutada correctamente")
        return True

    except Exception as e:
        agregar_log(f"Error inesperado en rutaList: {str(e)}")
        return None

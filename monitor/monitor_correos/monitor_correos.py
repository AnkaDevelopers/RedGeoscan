# Importaciones modulos
from monitor.guardar_excel.gestion_excel import guardar_en_excel, id_ya_registrado, ruta_ya_en_cola
from monitor.responder_correo.responder_correo import responder_correo
from monitor.log.log import agregar_log, guardar_log_en_archivo, enviar_log_por_correo
from config import config

# Importaciones adicionales
from win32com.client import Dispatch
import time
import string
import os

#************************************************************************************************************
# Función para verificar si la ruta existe
def verificar_ruta(ruta): 
    # Si la ruta comienza con una letra seguida de ":", la reemplaza
    if len(ruta) > 2 and ruta[1] == ":" and ruta[0].upper() in string.ascii_uppercase:
        ruta = r"\\192.168.1.81\Proyectos3" + ruta[2:]
    return os.path.exists(ruta)

#************************************************************************************************************
# Función para monitorear los correos
def monitorear_correos(ruta_nombre_archivo_excel):

    try:

        # Instancia que nos permite conectarnos a la aplicación Outlook
        outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
        
        # Acceder a la bandeja de entrada
        bandeja_entrada = outlook.GetDefaultFolder(6)  # 6 es la bandeja de entrada
        
        # Acceder a la carpeta de reciclaje
        carpeta_eliminados = outlook.GetDefaultFolder(3)  # 3 es la carpeta de elementos eliminados
        
        # Obtener los correos electrónicos en la bandeja de entrada
        mensajes = bandeja_entrada.Items
        
        # Ordenar los correos por fecha
        mensajes.Sort("[ReceivedTime]", True)  # Ordenar por fecha de recepción
        
        # Inicizlizamos la variable mensaje id
        mensaje_id = None
        
        # Recorrer los correos electrónicos
        agregar_log('Inicio recorrido mensajes') 
        for mensaje in mensajes:
            
            # Intervalo de Tiempo entre revision de mensajes
            time.sleep(2)
            
            # Validar que el asunto inicie con "redgeoscan" y capturar el nombre del proyecto
            agregar_log('Validando que el mensaje cumpla con la estructura')
            if mensaje.Subject.startswith("redgeoscan") and "ruta" in mensaje.Body: 
                
                 
                # Extraer el ID del correo
                mensaje_id = mensaje.EntryID 
                texto_log = 'Analizando mensaje con id: ' + mensaje_id
                agregar_log(texto_log)
                
                # Validamos si el ID del correo ya esta registrado
                agregar_log('Validando si el correo ya se encuentra registrado')
                if not id_ya_registrado(ruta_nombre_archivo_excel, mensaje_id):
                    
                    # Buscar la posición después de "ruta:"
                    inicio_ruta = mensaje.Body.find("ruta:") + len("ruta:")
                    inicio = mensaje.Body.find("<", inicio_ruta) + len("<")  # Buscar el primer "<" después de "ruta:"
                    fin = mensaje.Body.find(">", inicio)  # Buscar el ">"

                    # Extraer la ruta directamente
                    ruta_proyecto = mensaje.Body[inicio:fin].strip()
                 
                    texto_log = 'Validando existencia de la ruta: ' + ruta_proyecto
                    
                    agregar_log(texto_log) 
                    # Validamos si la ruta es valida
                    if verificar_ruta(ruta_proyecto):
                        
                        # Función para verificar si un proyecto esta en cola
                        validacion_ruta_proyecto, fecha_carga_ruta, nombre_remitente_carga = ruta_ya_en_cola(ruta_nombre_archivo_excel, ruta_proyecto)
                        
                        # Obtener el nombre del remitente y la fecha del correo
                        remitente = mensaje.SenderName
                        fecha = mensaje.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Capturar el nombre del proyecto, lo que sigue después de "redgeoscan " en el asunto del correo
                        proyecto_inicio = mensaje.Subject.find("redgeoscan") + len("redgeoscan")
                        nombre_proyecto = mensaje.Subject[proyecto_inicio:].strip()
                            
                        agregar_log('Validacion en caso de que la ruta del proyecto ya se enceuntra en cola')
                        # Verificamos que la ruta_proyecto no este en cola
                        if validacion_ruta_proyecto == False:
                           
                            # Nuevo estado del proyecto
                            estado = "En Proceso"

                            # Guardar en Excel
                            agregar_log('Guardando el proyecto en la base excel')
                            guardar_en_excel(ruta_nombre_archivo_excel, fecha, remitente, ruta_proyecto, mensaje_id, nombre_proyecto, estado)
                            
                            # Guardar LOG
                            ruta_add = f"Ruta detectada y procesada: {ruta_proyecto}, "
                            ruta_add_two = f"Remitente: {remitente}, Fecha: {fecha}"
                            agregar_log(ruta_add) 
                            agregar_log(ruta_add_two) 
                            
                            # Responder al remitente usando el mensaje definido en config.py
                            respuesta = config.mensaje_respuesta.format(remitente=remitente)
                            responder_correo(mensaje, respuesta)
                            
                        else:
                            
                            # Responder al remitente usando el mensaje definido en config.py
                            respuesta = config.mensaje_proyecto_en_cola.format(remitente=remitente, fecha=fecha_carga_ruta, emisor=nombre_remitente_carga)
                            responder_correo(mensaje, respuesta)
                            
                            # Guardar LOG
                            ruta_repit= f"El correo con ID {mensaje_id} Descartado."
                            agregar_log(ruta_repit) 
                            
                            # Elimianmso el mensaje
                            mensaje.delete()
                            
                            # Guardar LOG
                            ruta_proyecto_existe = f"El proyecto {nombre_proyecto} ya se enceuntra en cola"
                            agregar_log(ruta_proyecto_existe) 
                            
                    else:
                        
                        # Si la ruta_proyecto no existe, enviar mensaje de error
                        remitente = mensaje.SenderName
                        respuesta_error = config.mensaje_error_ruta.format(remitente=remitente)
                        responder_correo(mensaje, respuesta_error)
                        
                        # Guardar LOG
                        ruta_fake = f"Ruta no encontrada: {ruta_proyecto}. Se notificó al remitente: {remitente}."
                        agregar_log(ruta_fake) 
                        
                        # Eliminar el mensaje
                        mensaje.delete()
                        
                        # Guardar LOG
                        ruta_repit= f"El correo con ID {mensaje_id} Descartado."
                        agregar_log(ruta_repit) 
                        
                        continue
                    
                else:
                    # Guardar LOG
                    agregar_log("Este correo ya fue registrado")
                    continue
                 
            else:
                
                # Si la estructura del correo no cumple
                remitente = mensaje.SenderName
                respuesta_error = config.mensaje_error_monitoreo.format(remitente=remitente)
                responder_correo(mensaje, respuesta_error)   
                
                # Eliminar el mensaje
                mensaje.delete()
                
                # Guardar LOG
                ruta_repit= f"El correo con ID {mensaje_id} Descartado."
                agregar_log(ruta_repit) 
                print(ruta_repit) 
                
                continue
        
        # En caso de no haber correos en la bandeja
        if mensaje_id == None:
            
            # Log y Mensaje de depuración
            agregar_log("No hay correos en la bandeja")
            return 
            
                  
    except Exception as e:
        
        agregar_log(f"Error al monitorear correos: {e}" )
        guardar_log_en_archivo("Proceso_monitoreo_correo")
        enviar_log_por_correo(f"Error al monitorear correos: {e}")
        return
     

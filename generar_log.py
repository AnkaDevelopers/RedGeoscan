# Definimos la variable global como una lista vacía
global_list = []

def agregar_log(texto):

    # Indicamos que queremos usar la variable global
    global global_list  
    
    # En caso de querer regresar el log
    if "imprimir" in texto.lower():
        return global_list
    
    # Insertamos el texto en la posición 0 (al inicio)
    global_list.insert(0, texto)  
    



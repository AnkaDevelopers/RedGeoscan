from tkinter import filedialog, messagebox
from generar_log import agregar_log
import pandas as pd
import config  
import shutil
import os


#*********************************************************************************************************************************************************
# Variables globales extraidas del archivo config.py
ruta = config.ruta_proyecto
archivo = config.nombre_archivo_kml
msj_estado = config.msj_kml

#*********************************************************************************************************************************************************
# Funcion para cargar archivo kml
def cargar_base_kml():
    
    # Variable para almacenar el excel con los datos  de las antenas (KML)
    archivo_excel = None
    
    # Busca el archivo kml en la ruta especificada con el nombre del archivo
    archivo_excel = os.path.join(ruta, archivo)
    
    # Verifica si el archivo existe
    if not os.path.isfile(archivo_excel):
        
        
        # Mensaje de advertencia
        messagebox.showinfo("Advertencia", msj_estado[0])
        
        # Generamos log de depuración
        agregar_log(msj_estado[0])
            
        # Permite al usuario seleccionar el archivo manualmente
        archivo_excel = filedialog.askopenfilename(
            filetypes=[("Archivos Excel", "*.xlsx")],
            title="Selecciona un archivo KML"
        )
        
        # Si el usuario cancela la selección, sale de la función
        if not archivo_excel:
            
            # Generamos log de depuración
            agregar_log(msj_estado[1])
 
            # retornamos una variable None y un mensaje de depuracion
            return archivo_excel, msj_estado[1]
            
        # Copia el archivo KML al directorio del proyecto
        destino = os.path.join(ruta, archivo)
        
        try:
            
            # La base de antenas ha caragado satisfactoriamente
            shutil.copy(archivo_excel, destino)
            
            # Mensaje de confirmación
            messagebox.showinfo("Info", f"{msj_estado[3]}: {destino}")
            
            # Generar log de depuración 
            agregar_log(msj_estado[3])
            
            datos_excel = pd.read_excel(archivo_excel)
            
            # Retornamos los datos del kml y el mensaje de confirmación
            return datos_excel,msj_estado[3]
        
        # Manejo de errores en caso de no poder guardar el archivo en al carpeta
        except Exception as e:
            
            # Generar log de depuración
            agregar_log(msj_estado[4])
            
            # Mensaje de error
            messagebox.showerror("Error", f"{msj_estado[3]}: {e}")
            
            # Retornamos una variable vacia y el mensaje de error
            return archivo_excel,msj_estado[4]
    else:
        
        # En caso de que el archivo kml si exista en el proyecto
        datos_kml = pd.read_excel(archivo_excel)
        
        # Generar lod de depuración
        agregar_log(msj_estado[2])
        
        # Retornamos los datos de las antenas y el mensaje de confirmación
        return datos_kml,msj_estado[2]
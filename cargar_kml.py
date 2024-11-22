from tkinter import filedialog, messagebox
import pandas as pd
import shutil
import config  
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
        
        # Alerta en caso de no encontrar el archivo
        messagebox.showinfo("Advertencia", msj_estado[0])
        print('*'*50,'\n', msj_estado)
            
        # Permite al usuario seleccionar el archivo manualmente
        archivo_excel = filedialog.askopenfilename(
            filetypes=[("Archivos Excel", "*.xlsx")],
            title="Selecciona un archivo KML"
        )
        
        # Si el usuario cancela la selección, sale de la función
        if not archivo_excel:
            print('*'*50,'\n', msj_estado[1])
            return archivo_excel, msj_estado[1]
            
        # Copia el archivo KML al directorio del proyecto
        destino = os.path.join(ruta, archivo)
        
        try:
            
            # Validacion de la carga del archivo KML
            shutil.copy(archivo_excel, destino)
            messagebox.showinfo("Info", f"{msj_estado[3]}: {destino}")
            print('*'*50,'\n',msj_estado[3])
            datos_excel = pd.read_excel(archivo_excel)
            return datos_excel,msj_estado[3]
        
        except Exception as e:
            
            # Manejo de errores en caso de no poder guardar el archivo en al carpeta
            messagebox.showerror("Error", f"{msj_estado[3]}: {e}")
            return archivo_excel,msj_estado[4]
    else:
        datos_kml = pd.read_excel(archivo_excel)
        return datos_kml,msj_estado[2]
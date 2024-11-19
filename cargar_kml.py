from tkinter import filedialog, messagebox
import pandas as pd
import shutil
import config  
import os

ruta = config.ruta_proyecto
archivo = config.nombre_archivo_kml
msj_estado = config.msj_kml

# Funcion para cargar archivo kml
def cargar_base_kml():
    archivo_excel = None
    #busca el archivo kml en la ruta especificada con el nombre del archivo
    archivo_excel = os.path.join(ruta, archivo)
    # Verifica si el archivo existe
    if not os.path.isfile(archivo_excel):
        # Si el archivo no existe
        messagebox.showinfo("Advertencia", "No se encontró el archivo KML en la carpeta del proyecto.")
            
        # Permite al usuario seleccionar el archivo manualmente
        archivo_excel = filedialog.askopenfilename(
            filetypes=[("Archivos Excel", "*.xlsx")],
            title="Selecciona un archivo KML"
        )
        # Si el usuario cancela la selección, sale de la función
        if not archivo_excel:
            return archivo_excel,msj_estado[1]
            
        # Copia el archivo KML al directorio del proyecto
        destino = os.path.join(ruta, archivo)
        try:
            shutil.copy(archivo_excel, destino)
            messagebox.showinfo("Info", f"{msj_estado[2]}: {destino}")
            datos_excel = pd.read_excel(archivo_excel)
            return datos_excel,msj_estado[2]
        except Exception as e:
            messagebox.showerror("Error", f"{msj_estado[3]}: {e}")
            return archivo_excel,msj_estado[3]
    else:
        datos_kml = pd.read_excel(archivo_excel)
        return datos_kml,msj_estado[0]
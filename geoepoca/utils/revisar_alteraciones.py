# Importar modulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import os
import pandas as pd


# *********************************************************************
# Función para validar la existencia del archivo NAVEGADO
def buscar_archivo_navegado(ruta_proyecto):

    agregar_log("Iniciando búsqueda del archivo NAVEGADO...")

    subruta_navegado = os.path.join(ruta_proyecto, "Procesamiento", "1. Topografia", "Reportes", "NAVEGADO")

    if not os.path.exists(subruta_navegado):
        agregar_log("Ruta NAVEGADO no existe.")
        return None

    ruta_excel = os.path.join(subruta_navegado, "Puntos Navegados.xlsx")
    if os.path.exists(ruta_excel):
        agregar_log("Archivo 'Puntos Navegados.xlsx' encontrado.")
        return ruta_excel

    agregar_log("Archivo 'Puntos Navegados.xlsx' no encontrado. Buscando CSV para convertir...")

    for archivo in os.listdir(subruta_navegado):
        archivo_path = os.path.join(subruta_navegado, archivo)
        nombre, extension = os.path.splitext(archivo.lower())

        if extension == ".csv":
            agregar_log(f"Archivo CSV encontrado: {archivo}")
            try:
                try:
                    df = pd.read_csv(archivo_path, encoding="utf-8", sep=";", header=None)
                    agregar_log("CSV leído con separador ';'")
                except Exception:
                    try:
                        df = pd.read_csv(archivo_path, encoding="utf-8", sep=",", header=None)
                        agregar_log("CSV leído con separador ','")
                    except Exception:
                        df = pd.read_csv(archivo_path, encoding="latin-1", sep=",", header=None)
                        agregar_log("CSV leído con codificación 'latin-1' y separador ','")

                columnas_eliminar_letras = ['N', 'O', 'P', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA']
                columnas_eliminar = []

                for letra in columnas_eliminar_letras:
                    if len(letra) == 1:
                        idx = ord(letra) - ord('A')
                    else:
                        idx = (ord(letra[0]) - ord('A') + 1) * 26 + (ord(letra[1]) - ord('A'))
                    columnas_eliminar.append(idx)

                columnas_existentes = [i for i in columnas_eliminar if i < df.shape[1]]
                df.drop(columns=columnas_existentes, inplace=True)
                agregar_log(f"Columnas eliminadas: {columnas_existentes}")

                nueva_ruta = os.path.join(subruta_navegado, "Puntos Navegados.xlsx")
                df.to_excel(nueva_ruta, index=False, header=False)
                agregar_log(f"CSV convertido y guardado como Excel: {nueva_ruta}")
                return nueva_ruta

            except Exception as e:
                agregar_log(f"Error al convertir CSV a Excel en NAVEGADO: {e}")
                return None

    agregar_log("No se encontró archivo válido en la carpeta NAVEGADO.")
    return False

# *********************************************************************
# Función para validar la existencia del archivo FIX (CSV o Excel)
def buscar_archivo_fix(ruta_proyecto):
    agregar_log("Iniciando búsqueda del archivo FIX...")

    subruta_fix = os.path.join(ruta_proyecto, "Procesamiento", "1. Topografia", "Reportes", "FIX")

    if not os.path.exists(subruta_fix):
        agregar_log("Ruta FIX no existe.")
        return None

    ruta_excel = os.path.join(subruta_fix, "Cartera Fix.xlsx")
    if os.path.exists(ruta_excel):
        agregar_log("Archivo 'Cartera Fix.xlsx' encontrado.")
        return ruta_excel

    agregar_log("Archivo 'Cartera Fix.xlsx' no encontrado. Buscando CSV para convertir...")

    for archivo in os.listdir(subruta_fix):
        archivo_path = os.path.join(subruta_fix, archivo)
        nombre, extension = os.path.splitext(archivo.lower())

        if extension == ".csv":
            agregar_log(f"Archivo CSV encontrado: {archivo}")
            try:
                try:
                    df = pd.read_csv(archivo_path, encoding="utf-8", sep=",", header=None, engine='python')
                    agregar_log("CSV leído correctamente con utf-8 y separador ',' (engine=python)")
                    if df.shape[1] == 1:
                        raise ValueError("Archivo no separado correctamente, intentando con latin-1...")
                except Exception:
                    df = pd.read_csv(archivo_path, encoding="latin-1", sep=",", header=None, engine='python')
                    agregar_log("CSV leído correctamente con latin-1 y separador ',' (engine=python)")

                df.reset_index(drop=True, inplace=True)

                # Eliminar columnas de la O (índice 14) a la T (índice 19)
                columnas_a_eliminar = list(range(14, 20))
                columnas_existentes = [i for i in columnas_a_eliminar if i < df.shape[1]]
                df.drop(columns=columnas_existentes, inplace=True)
                agregar_log(f"Columnas eliminadas: {columnas_existentes}")

                nueva_ruta = os.path.join(subruta_fix, "Cartera Fix.xlsx")
                df.to_excel(nueva_ruta, index=False, header=False)
                agregar_log(f"CSV convertido y guardado como Excel: {nueva_ruta}")
                return nueva_ruta

            except Exception as e:
                agregar_log(f"Error al convertir CSV a Excel en FIX: {e}")
                return None

    agregar_log("No se encontró archivo válido en la carpeta FIX.")
    return False


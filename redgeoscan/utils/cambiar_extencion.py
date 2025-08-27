import subprocess
import os

def ejecutar_crx2rnx_desde_consola(ruta_archivo_crx):
    ruta_exe = r"C:\RedGeoscan\docs\crx2rnx.exe"

    if not os.path.exists(ruta_archivo_crx):
        print("El archivo .crx no existe.")
        return

    if not os.path.exists(ruta_exe):
        print("El ejecutable crx2rnx.exe no se encontró.")
        return

    try:
        # Ejecuta como si arrastraras el archivo al .exe desde consola
        subprocess.run(f'"{ruta_exe}" "{ruta_archivo_crx}"', shell=True, check=True)
        print("✅ Conversión completada correctamente.")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Error al ejecutar la conversión:", e)
        return None

# Ejemplo de uso
# ejecutar_crx2rnx_desde_consola(r"F:\MAAT\2503-AVR_GUADUAS\Procesamiento\1. Topografia\Rastreos\070325\Red activa\GPS1\IGAC\CALI\CALI00COL_R_20250770000_01D_15S_MO.crx")

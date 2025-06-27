# Importar módulos monitor
from monitor.log.log import agregar_log

import pandas as pd

def comparar_archivos_excel(ruta_navegado, ruta_cartera_fix):
    try:
        agregar_log("Iniciando comparación de archivos Excel...")

        # Leer archivos
        agregar_log(f"Leyendo archivo navegado: {ruta_navegado}")
        df_nav = pd.read_excel(ruta_navegado, header=None)
        agregar_log(f"Archivo navegado leído correctamente con {len(df_nav)} filas.")

        agregar_log(f"Leyendo archivo cartera_fix: {ruta_cartera_fix}")
        df_fix = pd.read_excel(ruta_cartera_fix, header=None)
        agregar_log(f"Archivo cartera_fix leído correctamente con {len(df_fix)} filas.")

        # Columnas para diferencias: X, Y, Z
        cols_nav = [7, 8, 9]    # H, I, J
        cols_fix = [8, 9, 10]  # I, J, K

        encabezados = ['ID Base', 'Difer X', 'Difer Y', 'Difer Z']
        resultados = [encabezados]
        agregar_log("Encabezados establecidos correctamente.")

        # Calcular diferencias
        agregar_log("Iniciando cálculo de diferencias entre puntos coincidentes...")
        coincidencias = 0
        for _, fila_nav in df_nav.iterrows():
            id_base = fila_nav[0]
            fila_fix = df_fix[df_fix[0] == id_base]
            if fila_fix.empty:
                agregar_log(f"ID {id_base} no encontrado en cartera_fix. Se omite.")
                continue
            fila_fix = fila_fix.iloc[0]
            coincidencias += 1

            diferencias = []
            for c_nav, c_fix in zip(cols_nav, cols_fix):
                try:
                    valor_nav = float(fila_nav[c_nav])
                    valor_fix = float(fila_fix[c_fix])
                    diferencia = round(valor_nav - valor_fix, 2)
                    diferencias.append(f"{diferencia}m")
                except Exception as e:
                    agregar_log(f"Error al procesar diferencia para ID {id_base} en columnas {c_nav}-{c_fix}: {e}")
                    diferencias.append("ERROR")

            resultados.append([id_base] + diferencias)

        agregar_log(f"Se encontraron y procesaron {coincidencias} puntos coincidentes.")
        agregar_log("Proceso de comparación finalizado correctamente.")
        return resultados

    except Exception as e:
        agregar_log(f"Error general en comparar_archivos_excel: {e}")
        return None

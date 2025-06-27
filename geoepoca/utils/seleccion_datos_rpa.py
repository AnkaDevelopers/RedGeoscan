# Importar módulos monitor
from monitor.log.log import agregar_log

# Importaciones adicionales
import openpyxl

def seleccion_datos_para_rpa(ruta_cartera_fix, fecha_rastreo):
    try:
        agregar_log("🔍 Iniciando procesamiento del archivo Excel...")
        wb = openpyxl.load_workbook(ruta_cartera_fix, data_only=True)
        ws = wb.active
        agregar_log("✅ Archivo Excel cargado correctamente.")

        datos = [["ID", "X", "Y", "Z", "Fecha Rastreo", "Fecha referencia"]]

        for i, fila in enumerate(ws.iter_rows(min_row=1), start=1):
            try:
                id_ = fila[0].value
                x = fila[8].value
                y = fila[9].value
                z = fila[10].value

                if id_ is not None and x is not None and y is not None and z is not None:
                    datos.append([id_, x, y, z, fecha_rastreo, "1/01/2018"])
                    agregar_log(f"✅ Fila {i} procesada correctamente: {id_}, {x}, {y}, {z}")
                else:
                    agregar_log(f"⚠️ Fila {i} incompleta, omitida.")
            except Exception as e:
                agregar_log(f"❌ Error procesando fila {i}: {e}")

        agregar_log("🎯 Procesamiento finalizado con éxito.")
        return datos

    except Exception as e:
        agregar_log(f"❌ Error al procesar el archivo Excel: {e}")
        return None

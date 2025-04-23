# Importaciones modulos
from monitor.log.log import agregar_log

# Importaciones adicionales
from fpdf import FPDF
import time
import os

def generar_informe_pdf_por_gps(datos_proyecto, radio):

    class PDF(FPDF):
        def header(self):
            self.image('C:\\bot-auto\\data\\logo_anka.jpg', 10, 8, 33)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.title, align='C', ln=True)
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Página {self.page_no()}', align='C')

    try:
        for dia_rastreo, info_dia in datos_proyecto['dias_rastreos'].items():
            subcarpetas = info_dia.get('subcarpetas', {})
            red_activa = subcarpetas.get('Red activa', None)

            if not red_activa:
                print(f"No se encontró la carpeta 'Red activa' para el día {dia_rastreo}.")
                continue

            base_subcarpetas = subcarpetas.get('Base', {}).get('sub_carpetas', {})

            for nombre_gps, info_gps in base_subcarpetas.items():
                ruta_gps = info_gps['ruta']
                informacion_pos = info_gps.get('informacion_pos', {})
                antenas_cercanas = info_gps.get('antenas_cercanas', [])

                antenas_descargadas = [antena for antena in antenas_cercanas if antena.get('DESCARGA', '').upper() == "COMPLETA"]
                antenas_no_descargadas = [antena for antena in antenas_cercanas if antena.get('DESCARGA', '').upper() != "COMPLETA"]

                pdf = PDF(orientation='L')
                pdf.title = f"Informe de GPS - {nombre_gps}"
                pdf.add_page()

                pdf.set_font("Arial", style="B", size=14)
                pdf.cell(0, 10, txt="Resumen General", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, txt=f"Antenas totales analizadas en un radio de {radio} km: {len(antenas_cercanas)}", ln=True)
                pdf.cell(0, 10, txt=f"Número de antenas descargadas: {len(antenas_descargadas)}", ln=True)
                pdf.ln(10)

                pdf.set_font("Arial", style="B", size=14)
                pdf.cell(0, 10, txt="Coordenada Media", ln=True)
                pdf.set_font("Arial", size=10)

                pdf.cell(0, 10, txt=f"Latitud: {informacion_pos.get('latitud', 'N/A')}", ln=True)
                pdf.cell(0, 10, txt=f"Longitud: {informacion_pos.get('longitud', 'N/A')}", ln=True)
                pdf.cell(0, 10, txt=f"Fecha: {informacion_pos.get('fecha', 'N/A')}", ln=True)
                pdf.cell(0, 10, txt=f"Semana: {informacion_pos.get('semana', 'N/A')} - Día: {informacion_pos.get('dia', 'N/A')}", ln=True)
                pdf.ln(10)

                # Página individual por cada antena descargada
                for idx, antena in enumerate(antenas_descargadas, start=1):
                    pdf.add_page()
                    pdf.set_font("Arial", style="B", size=12)
                    pdf.cell(0, 10, txt=f"Antena {idx} - Detalles", ln=True)
                    pdf.set_font("Arial", size=10)

                    nombre = antena.get('NAME', 'N/A')
                    distancia = round(float(antena.get('Distancia', 0)), 1)
                    tiempo = antena.get('Tiempo de Rastreo (h)', 'N/A')
                    materializada = antena.get('MATERIALIZADA', 'N/A')
                    orden = antena.get('ORDEN', 'N/A')
                    coordenada = antena.get('COORDENADA', 'N/A')

                    pdf.cell(0, 10, txt=f"Nombre: {nombre}", ln=True)
                    pdf.cell(0, 10, txt=f"Distancia: {distancia} km", ln=True)
                    pdf.cell(0, 10, txt=f"Tiempo de Rastreo: {tiempo} (h)", ln=True)
                    pdf.cell(0, 10, txt=f"Materializada o administrada por: {materializada}", ln=True)
                    pdf.cell(0, 10, txt=f"Orden: {orden}", ln=True)

                    if orden == "0":
                        pdf.cell(0, 10, txt=f"Coordenadas: {coordenada}", ln=True)
                        if all(k in antena for k in ['x', 'y', 'z']):
                            pdf.cell(0, 10, txt=f"    X: {antena['x']}", ln=True)
                            pdf.cell(0, 10, txt=f"    Y: {antena['y']}", ln=True)
                            pdf.cell(0, 10, txt=f"    Z: {antena['z']}", ln=True)

                # Antenas no descargadas
                pdf.add_page()
                pdf.set_font("Arial", style="B", size=12)
                pdf.cell(0, 10, txt="Antenas No Descargadas:", ln=True)
                pdf.set_font("Arial", size=10)

                if not antenas_no_descargadas:
                    pdf.cell(0, 10, txt="Todas las antenas fueron descargadas.", ln=True)
                else:
                    for antena in antenas_no_descargadas:
                        nombre = antena.get('NAME', 'N/A')
                        distancia = round(float(antena.get('Distancia', 0)), 1)
                        descarga = antena.get('DESCARGA', 'N/A')
                        pdf.cell(0, 10, txt=f"Nombre: {nombre} - Distancia: {distancia} km - Descarga: {descarga}", ln=True)

                ruta_guardado = os.path.join(red_activa, f"INFORME-{nombre_gps}.pdf")
                pdf.output(ruta_guardado)
                agregar_log(f"Informe PDF generado y guardado en: {ruta_guardado}")

        return None, True

    except Exception as e:
        msj_depuracion = f"Error al generar los informes PDF: {e}"
        return msj_depuracion, None

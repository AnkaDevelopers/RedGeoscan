# Importaciones modulos
from monitor.log.log import agregar_log

# Importaciones adicionales
from fpdf import FPDF
import os

def generar_informe_pdf_por_gps(datos_proyecto):
    class PDF(FPDF):
        def header(self):
            # Logo
            self.image('C:\\bot-auto\\data\\logo_anka.jpg', 10, 8, 33)
            self.set_font('Arial', 'B', 12)
            # Título dinámico
            self.cell(0, 10, self.title, align='C', ln=True)
            self.ln(10)

        def footer(self):
            # Posición a 1.5 cm del final
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            # Número de página
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

                # Filtrar antenas descargadas y no descargadas
                antenas_descargadas = [antena for antena in antenas_cercanas if antena.get('DESCARGA', '').upper() == "COMPLETA"]
                antenas_no_descargadas = [antena for antena in antenas_cercanas if antena.get('DESCARGA', '').upper() != "COMPLETA"]

                # Crear PDF personalizado para la carpeta GPS
                pdf = PDF(orientation='L')
                pdf.title = f"Informe de GPS - {nombre_gps}"
                pdf.add_page()

                # Página 1: Resumen General y Coordenada Media
                pdf.set_font("Arial", style="B", size=14)
                pdf.cell(0, 10, txt="Resumen General", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, txt=f"Antenas totales analizadas en un radio de 150 km: {len(antenas_cercanas)}", ln=True)
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

                # A partir de la página 2: Detalles de las antenas descargadas
                pdf.set_font("Arial", style="B", size=12)
                pdf.add_page()
                pdf.cell(0, 10, txt="Antenas Cercanas:", ln=True)
                pdf.set_font("Arial", size=10)

                if not antenas_descargadas:
                    pdf.cell(0, 10, txt="No se encontraron antenas descargadas.", ln=True)
                else:
                    for idx, antena in enumerate(antenas_descargadas, start=1):
                        if (idx - 1) % 2 == 0 and idx > 1:  # Cada dos antenas, agregar una nueva página
                            pdf.add_page()
                            pdf.set_font("Arial", style="B", size=12)
                            pdf.cell(0, 10, txt="Antenas Cercanas (Continuación):", ln=True)
                            pdf.set_font("Arial", size=10)

                        coordenada = antena.get('COORDENADA', '0')
                        pdf.cell(0, 10, txt=f"{idx}. Nombre: {antena['NAME']}", ln=True)
                        pdf.cell(0, 10, txt=f"   Distancia: {antena['Distancia']} km", ln=True)
                        pdf.cell(0, 10, txt=f"   Coordenadas: {coordenada}", ln=True)
                        pdf.cell(0, 10, txt=f"   Tiempo de Rastreo (h): {antena.get('Tiempo de Rastreo (h)', 'N/A')}", ln=True)
                        pdf.cell(0, 10, txt=f"   Materializada: {antena.get('MATERIALIZADA', 'N/A')}", ln=True)
                        pdf.cell(0, 10, txt=f"   Orden: {antena.get('ORDEN', 'N/A')}", ln=True)
                        pdf.cell(0, 10, txt=f"   Descarga: {antena.get('DESCARGA', 'N/A')}", ln=True)
                        pdf.ln(5)

                # Lista de antenas no descargadas
                pdf.add_page()
                pdf.set_font("Arial", style="B", size=12)
                pdf.cell(0, 10, txt="Antenas No Descargadas:", ln=True)
                pdf.set_font("Arial", size=10)

                if not antenas_no_descargadas:
                    pdf.cell(0, 10, txt="Todas las antenas fueron descargadas.", ln=True)
                else:
                    for antena in antenas_no_descargadas:
                        pdf.cell(0, 10, txt=f"Nombre: {antena['NAME']} - Distancia: {antena['Distancia']} km - Descarga: {antena.get('DESCARGA', 'N/A')}", ln=True)

                # Guardar PDF en la ruta de Red Activa + nombre de la carpeta GPS
                ruta_guardado = os.path.join(red_activa, f"{nombre_gps}_informe_descargas.pdf")
                pdf.output(ruta_guardado)
                agregar_log(f"Informe PDF generado y guardado en: {ruta_guardado}")

        return None, True  

    except Exception as e:
        msj_depuracion = f"Error al generar los informes PDF: {e}"
        return msj_depuracion, None  

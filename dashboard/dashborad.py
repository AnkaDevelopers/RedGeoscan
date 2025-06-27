# Importar modulos monitor
from monitor.log.log import agregar_log

# importaciones adicionales
import pandas as pd
import time
import os

# Rutas
EXCEL_PATH = r'F:\1 - CAPTURADOR DE RUTAS\RutaList\Cola_proyectos.xlsx'  # Ajusta el nombre exacto del archivo
HTML_OUTPUT = r'F:\estado_proyectos.html'

# Template HTML con marcador para insertar tabla
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estado de Proyectos</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #aaa;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #007BFF;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
<h2>Visualizador de Estado de Proyectos</h2>
<p>Última actualización: {fecha}</p>
{tabla}
</body>
</html>
"""

def main():
    try:
        df = pd.read_excel(EXCEL_PATH)
        tabla_html = df.to_html(index=False, border=0, classes='tabla', escape=False)
        contenido_final = HTML_TEMPLATE.format(tabla=tabla_html, fecha=pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))

        with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
            f.write(contenido_final)
        agregar_log(f"[✓] HTML actualizado: {HTML_OUTPUT}")
    except Exception as e:
        agregar_log(f"[✗] Error al generar HTML: {e}")
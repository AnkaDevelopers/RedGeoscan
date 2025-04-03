import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class CarpetaProyectoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Estructura de Proyecto")

        self.dias_rastreos = []

        self.frame_main = ttk.Frame(root, padding=20)
        self.frame_main.pack(fill="both", expand=True)

        self.crear_formulario_principal()

    def crear_formulario_principal(self):
        ttk.Label(self.frame_main, text="Nombre del Proyecto:").grid(row=0, column=0, sticky="w")
        self.entry_nombre = ttk.Entry(self.frame_main, width=40)
        self.entry_nombre.grid(row=0, column=1, pady=5)

        ttk.Label(self.frame_main, text="Año (AA):").grid(row=1, column=0, sticky="w")
        self.entry_anio = ttk.Entry(self.frame_main, width=10)
        self.entry_anio.grid(row=1, column=1, sticky="w")

        ttk.Label(self.frame_main, text="Mes (MM):").grid(row=2, column=0, sticky="w")
        self.entry_mes = ttk.Entry(self.frame_main, width=10)
        self.entry_mes.grid(row=2, column=1, sticky="w")

        self.boton_agregar_dia = ttk.Button(self.frame_main, text="Agregar Día de Rastreo", command=self.agregar_dia_rastreo)
        self.boton_agregar_dia.grid(row=3, column=0, columnspan=2, pady=10)

        self.lista_dias = tk.Listbox(self.frame_main, width=60, height=8)
        self.lista_dias.grid(row=4, column=0, columnspan=2, pady=5)

        self.boton_crear = ttk.Button(self.frame_main, text="Crear Carpeta del Proyecto", command=self.crear_estructura)
        self.boton_crear.grid(row=5, column=0, columnspan=2, pady=15)

    def agregar_dia_rastreo(self):
        fecha = simpledialog.askstring("Fecha de Rastreo", "Ingrese la fecha en formato ddmmaa:")
        if not fecha:
            return

        try:
            num_gps = int(simpledialog.askstring("Cantidad de GPS", f"¿Cuántos GPS para el {fecha}?:"))
        except:
            messagebox.showerror("Error", "Ingrese un número válido de GPS")
            return

        gps_nombres = []
        for i in range(num_gps):
            nombre_gps = simpledialog.askstring("Nombre del GPS", f"Nombre del GPS {i+1}:")
            if nombre_gps:
                gps_nombres.append(nombre_gps.strip())

        self.dias_rastreos.append({"fecha": fecha, "gps": gps_nombres})
        self.lista_dias.insert(tk.END, f"{fecha} - GPS: {', '.join(gps_nombres)}")

    def crear_estructura(self):
        nombre_proyecto = self.entry_nombre.get().strip().upper()
        anio = self.entry_anio.get().strip()
        mes = self.entry_mes.get().strip()

        if not (nombre_proyecto and anio and mes):
            messagebox.showerror("Error", "Debe completar todos los campos del proyecto.")
            return

        nombre_raiz = f"{anio}{mes}-{nombre_proyecto}"
        Path(nombre_raiz).mkdir(parents=True, exist_ok=True)

        entregables = ["CURVAS", "DSM", "DTM", "NUBE", "ORTOMOSAICO", "RESTITUCION/DIGITALIZACIóN", "RESTITUCION/GDB"]
        procesamiento = ["1. Topografia", "2. Poligonos"]

        for carpeta in entregables:
            Path(os.path.join(nombre_raiz, "Entregables", *carpeta.split('/'))).mkdir(parents=True, exist_ok=True)

        for dia in self.dias_rastreos:
            fecha = dia["fecha"]
            gps_list = dia["gps"]
            ruta_dia = os.path.join(nombre_raiz, "Procesamiento", procesamiento[0], "Rastreos", fecha)
            Path(os.path.join(ruta_dia, "Base")).mkdir(parents=True, exist_ok=True)
            Path(os.path.join(ruta_dia, "Red activa")).mkdir(parents=True, exist_ok=True)
            for gps in gps_list:
                Path(os.path.join(ruta_dia, "Base", gps)).mkdir(parents=True, exist_ok=True)
                Path(os.path.join(ruta_dia, "Red activa", gps)).mkdir(parents=True, exist_ok=True)

        messagebox.showinfo("¡Éxito!", f"Estructura creada en la carpeta: {nombre_raiz}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CarpetaProyectoApp(root)
    root.mainloop()
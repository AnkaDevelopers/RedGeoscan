from tkinter import filedialog, messagebox,Toplevel
import tkinter as tk
import pandas as pd
import sys
import os

# Ruta del archivo Excel
excel_path = r"\\Desarrollo\redgeoscan\1 - CAPTURADOR DE RUTAS\RutaList\Cola_proyectos.xlsx"

# Colores corporativos
COLOR_PRIMARIO = "#24365D"    # Azul oscuro
COLOR_SECUNDARIO = "#E76F00"  # Naranja
COLOR_FONDO = "#E8E8E8"       # Gris claro

def recurso_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

def seleccionar_carpeta():
    # Crear ventana temporal para centrar y reducir visualmente el tamaño
    top = Toplevel()
    top.withdraw()  # Oculta la ventana pero la mantiene activa
    top.geometry("1x1+600+300")  # Tamaño mínimo y posición centrada aprox.
    carpeta = filedialog.askdirectory(parent=top, title="Seleccionar carpeta del proyecto")
    top.destroy()  # Cierra la ventana temporal

    if carpeta:
        entrada_ruta.delete(0, tk.END)
        entrada_ruta.insert(0, carpeta)

def cargar_ruta():
    ruta = entrada_ruta.get().strip()

    if not ruta:
        messagebox.showwarning("Advertencia", "La ruta no puede estar vacía.")
        return
    # Reemplazar cualquier unidad (Ej: Z:\ o X:\) por \\Desarrollo\redgeoscan\
    if len(ruta) >= 2 and ruta[1] == ":":
        ruta = ruta.replace(ruta[:2], r"\\Desarrollo\redgeoscan", 1)

    # Verificar si existe en el sistema
    if not os.path.isdir(ruta):
        messagebox.showerror("Ruta inválida", "La ruta ingresada no es válida o no existe.")
        return

    try:
        df = pd.read_excel(excel_path)

        if 'estado' not in df.columns:
            df['estado'] = ""

        if ruta in df['ruta'].values:
            df.loc[df['ruta'] == ruta, 'estado'] = 'En proceso'
            mensaje = "Ruta ya existente. Estado actualizado a 'En proceso'."
        else:
            nueva_fila = pd.DataFrame({'ruta': [ruta], 'estado': ['En proceso']})
            df = pd.concat([df, nueva_fila], ignore_index=True)
            mensaje = "Ruta agregada correctamente con estado 'En proceso'."

        df.to_excel(excel_path, index=False)
        messagebox.showinfo("Éxito", mensaje)
        entrada_ruta.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo escribir en el archivo:\n{e}")

# Interfaz
ventana = tk.Tk()
ventana.title("R.G.S- Capturador de Rutas")
ventana.geometry("600x160")
ventana.configure(bg=COLOR_FONDO)
ventana.resizable(False, False)

# Título
tk.Label(
    ventana,
    text="Ingrese la ruta del proyecto",
    bg=COLOR_FONDO,
    fg=COLOR_PRIMARIO,
    font=("Arial", 12, "bold")
).pack(pady=(15, 5))

# Input + botón "..."
frame_input = tk.Frame(ventana, bg=COLOR_FONDO)
frame_input.pack(padx=20, fill="x")

entrada_ruta = tk.Entry(frame_input, font=("Arial", 10))
entrada_ruta.pack(side=tk.LEFT, fill="x", expand=True)

btn_buscar = tk.Button(
    frame_input,
    text="...",
    width=4,
    bg=COLOR_PRIMARIO,
    fg="white",
    command=seleccionar_carpeta,
    cursor="hand2"
)
btn_buscar.pack(side=tk.LEFT, padx=(5, 0))

# Botón cargar ruta
btn_cargar = tk.Button(
    ventana,
    text="CARGAR RUTA",
    bg=COLOR_SECUNDARIO,
    fg="white",
    font=("Arial", 10, "bold"),
    command=cargar_ruta,
    cursor="hand2"
)
btn_cargar.pack(pady=15)

ventana.mainloop()

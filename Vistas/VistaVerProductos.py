import tkinter as tk
from tkinter import ttk

class VistaVerProductos:
    def __init__(self, root, lista_productos):
        self.window = tk.Toplevel(root)
        self.window.title("Lista de Productos")
        self.window.geometry("850x300")

        cols = ["Código", "Nombre", "Descripción", "Proveedor", "Categoría", "Stock", "Fecha"]
        self.tree = ttk.Treeview(self.window, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True)

        for p in lista_productos:
            self.tree.insert("", "end", values=(
                p.get_codigo(),
                p.get_nombre(),
                p.get_descripcion(),
                p.get_proveedor(),
                p.get_categoria(),
                p.get_stock(),
                p.get_fechaActualizacion()
            ))

import tkinter as tk
from tkinter import ttk

class VistaReporteStock:
    def __init__(self, root, productos):
        self.win = tk.Toplevel(root)
        self.win.title("Reporte de Stock")
        self.win.geometry("700x400")

        self.tree = ttk.Treeview(self.win, columns=("codigo", "nombre", "stock", "categoria", "proveedor"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        for p in productos:
            self.tree.insert("", tk.END, values=(
                p.get_codigo(),
                p.get_nombre(),
                p.get_stock(),
                p.get_categoria(),
                p.get_proveedor()
            ))

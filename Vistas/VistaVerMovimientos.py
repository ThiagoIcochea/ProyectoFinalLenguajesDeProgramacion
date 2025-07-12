import tkinter as tk
from tkinter import ttk

class VistaVerMovimientos:
    def __init__(self, root, movimientos):
        self.win = tk.Toplevel(root)
        self.win.title("Historial de Movimientos")
        self.win.geometry("700x400")

        self.tree = ttk.Treeview(self.win, columns=("fecha", "producto", "tipo", "cantidad", "usuario", "motivo"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        for m in movimientos:
            self.tree.insert("", tk.END, values=(
                m.get_fecha(),
                m.get_producto_codigo(),
                m.get_tipo(),
                m.get_cantidad(),
                m.get_usuario(),
                m.get_motivo()
            ))

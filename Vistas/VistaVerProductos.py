import tkinter as tk
from tkinter import ttk

class VistaVerProductos:
    def __init__(self, root, controlador_producto):
        self.productos = controlador_producto.listar_productos()
        self.win = tk.Toplevel(root)
        self.win.title("Lista de Productos")
        self.win.geometry("800x500")

    
        filtro_frame = tk.Frame(self.win)
        filtro_frame.pack(pady=10)

        tk.Label(filtro_frame, text="Filtrar por nombre o código:").grid(row=0, column=0, padx=5)
        self.entry_filtro = tk.Entry(filtro_frame)
        self.entry_filtro.grid(row=0, column=1, padx=5)
        tk.Button(filtro_frame, text="Filtrar", command=self.filtrar).grid(row=0, column=2, padx=5)
        tk.Button(filtro_frame, text="Limpiar", command=self.limpiar).grid(row=0, column=3, padx=5)

       
        self.tree = ttk.Treeview(self.win, columns=("codigo", "nombre", "stock", "categoria", "proveedor"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.cargar_datos(self.productos)

    def cargar_datos(self, lista):
        self.tree.delete(*self.tree.get_children())
        for p in lista:
            self.tree.insert("", tk.END, values=(
                p.get_codigo(),
                p.get_nombre(),
                p.get_stock(),
                p.get_categoria(),
                p.get_proveedor()
            ))

    def filtrar(self):
        texto = self.entry_filtro.get().lower()
        filtrados = [p for p in self.productos if texto in p.get_nombre().lower() or texto in p.get_codigo().lower()]
        self.cargar_datos(filtrados)

    def limpiar(self):
        self.entry_filtro.delete(0, tk.END)
        self.cargar_datos(self.productos)

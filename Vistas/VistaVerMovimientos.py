import tkinter as tk
from tkinter import ttk

class VistaVerMovimientos:
    def __init__(self, root, controlador_movimiento):
        self.controlador_movimiento = controlador_movimiento
        self.movimientos = controlador_movimiento.listar_movimientos()

        self.win = tk.Toplevel(root)
        self.win.title("Historial de Movimientos")
        self.win.geometry("900x500")

        
        filtro_frame = tk.Frame(self.win)
        filtro_frame.pack(pady=10)

        
        tk.Label(filtro_frame, text="Código de producto:").grid(row=0, column=0, padx=5)
        self.entry_codigo = tk.Entry(filtro_frame)
        self.entry_codigo.grid(row=0, column=1, padx=5)

        
        tk.Label(filtro_frame, text="Tipo:").grid(row=0, column=2, padx=5)
        self.combo_tipo = ttk.Combobox(filtro_frame, values=["", "entrada", "salida"], state="readonly", width=10)
        self.combo_tipo.grid(row=0, column=3, padx=5)
        self.combo_tipo.set("")

        tk.Button(filtro_frame, text="Filtrar", command=self.filtrar).grid(row=0, column=4, padx=5)
        tk.Button(filtro_frame, text="Limpiar", command=self.limpiar).grid(row=0, column=5, padx=5)

        
        self.tree = ttk.Treeview(self.win, columns=("fecha", "producto", "tipo", "cantidad", "usuario", "motivo"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.cargar_datos(self.movimientos)

    def cargar_datos(self, movimientos):
        self.tree.delete(*self.tree.get_children())
        for m in movimientos:
            self.tree.insert("", tk.END, values=(
                m.get_fecha(),
                m.get_producto_codigo(),
                m.get_tipo(),
                m.get_cantidad(),
                m.get_usuario(),
                m.get_motivo()
            ))

    def filtrar(self):
        codigo = self.entry_codigo.get().strip().lower()
        tipo = self.combo_tipo.get().strip().lower()

        filtrados = [
            m for m in self.movimientos
            if (codigo in m.get_producto_codigo().lower() if codigo else True)
            and (m.get_tipo().lower() == tipo if tipo else True)
        ]
        self.cargar_datos(filtrados)

    def limpiar(self):
        self.entry_codigo.delete(0, tk.END)
        self.combo_tipo.set("")
        self.cargar_datos(self.movimientos)

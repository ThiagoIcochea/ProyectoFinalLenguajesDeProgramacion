import tkinter as tk
from tkinter import ttk, messagebox

class VistaEditarStock:
    def __init__(self, root, controlador_producto):
        self.window = tk.Toplevel(root)
        self.window.title("Editar Stock")
        self.window.geometry("320x200")
        self.controlador = controlador_producto

      
        tk.Label(self.window, text="Selecciona código de producto:").pack(pady=5)
        self.codigos = [p.get_codigo() for p in self.controlador.listar_productos()]
        self.combo_codigos = ttk.Combobox(self.window, values=self.codigos, state="readonly")
        self.combo_codigos.pack()
        self.combo_codigos.bind("<<ComboboxSelected>>", self.cargar_stock_actual)

        
        tk.Label(self.window, text="Nuevo stock:").pack(pady=5)
        self.var_stock = tk.IntVar()
        self.spin_stock = tk.Spinbox(self.window, from_=0, to=100000, textvariable=self.var_stock, width=10)
        self.spin_stock.pack()

        
        tk.Button(self.window, text="Actualizar", command=self.actualizar_stock).pack(pady=10)

    def cargar_stock_actual(self, event):
        codigo = self.combo_codigos.get()
        producto = self.controlador.obtener_producto(codigo)
        if producto:
            self.var_stock.set(producto.get_stock())

    def actualizar_stock(self):
        codigo = self.combo_codigos.get()
        if not codigo:
            messagebox.showerror("Error", "Debes seleccionar un producto.")
            return

        nuevo_stock = self.var_stock.get()
        if self.controlador.actualizar_stock(codigo, int(nuevo_stock)):
            messagebox.showinfo("Éxito", "Stock actualizado correctamente.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el stock.")

import tkinter as tk
from tkinter import messagebox, ttk, filedialog

class VistaAgregarProducto:
    def __init__(self, root, controlador_producto):
        self.window = tk.Toplevel(root)
        self.window.title("Agregar Producto")
        self.window.geometry("420x550")
        self.controlador = controlador_producto

        self.campos = {}

        tk.Label(self.window, text="Código:").pack()
        self.campos["codigo"] = tk.Entry(self.window)
        self.campos["codigo"].pack()

        tk.Label(self.window, text="Nombre:").pack()
        self.campos["nombre"] = tk.Entry(self.window)
        self.campos["nombre"].pack()

        tk.Label(self.window, text="Descripción:").pack()
        self.campos["descripcion"] = tk.Entry(self.window)
        self.campos["descripcion"].pack()

        tk.Label(self.window, text="Categoría:").pack()
        categorias = [
            "Sillas", "Escritorios", "Computadoras", "Impresoras",
            "Papelería", "Monitores", "Teclados", "Mouses",
            "Almacenamiento", "Otros"
        ]
        self.campos["categoria"] = ttk.Combobox(self.window, values=categorias, state="readonly")
        self.campos["categoria"].pack()
        self.campos["categoria"].current(0)

        tk.Label(self.window, text="Proveedor:").pack()
        proveedores = [
            "Office Depot", "Staples", "HP", "Lenovo", "Canon",
            "Epson", "Logitech", "Samsung", "Amazon", "Otros"
        ]
        self.campos["proveedor"] = ttk.Combobox(self.window, values=proveedores, state="readonly")
        self.campos["proveedor"].pack()
        self.campos["proveedor"].current(0)

        tk.Label(self.window, text="Stock inicial:").pack()
        self.campos["stock"] = tk.Entry(self.window)
        self.campos["stock"].pack()

        tk.Button(self.window, text="Agregar producto", command=self.agregar).pack(pady=15)

        
        tk.Button(self.window, text="Importar desde Excel", command=self.importar_excel).pack(pady=5)

   
        tk.Button(self.window, text="Exportar a Excel", command=self.exportar_excel).pack(pady=5)

    def agregar(self):
        try:
            codigo = self.campos["codigo"].get().strip()
            nombre = self.campos["nombre"].get().strip()
            descripcion = self.campos["descripcion"].get().strip()
            categoria = self.campos["categoria"].get().strip()
            proveedor = self.campos["proveedor"].get().strip()
            stock_str = self.campos["stock"].get().strip()

            if not all([codigo, nombre, descripcion, categoria, proveedor, stock_str]):
                raise ValueError("Todos los campos son obligatorios.")
            if not stock_str.isdigit():
                raise ValueError("Stock debe ser numérico.")
            stock = int(stock_str)

            if self.controlador.agregar_producto(codigo, nombre, descripcion, proveedor, categoria, stock):
                messagebox.showinfo("Éxito", "Producto agregado.")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Código ya registrado.")
        except ValueError as e:
            messagebox.showerror("Validación", str(e))

    def importar_excel(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if ruta:
            try:
                cantidad = self.controlador.importar_desde_excel(ruta)
                messagebox.showinfo("Importación exitosa", f"Se importaron {cantidad} productos.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo importar: {str(e)}")

    def exportar_excel(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if ruta:
            try:
                self.controlador.exportar_a_excel(ruta)
                messagebox.showinfo("Exportación exitosa", f"Productos exportados a:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

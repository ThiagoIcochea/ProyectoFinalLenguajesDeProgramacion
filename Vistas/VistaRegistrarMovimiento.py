import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VistaRegistrarMovimiento:
    def __init__(self, root, controlador_producto, controlador_movimiento, usuario):
        self.top = tk.Toplevel(root)
        self.top.title("Registrar Movimiento")
        self.top.geometry("400x400")

        self.controlador_producto = controlador_producto
        self.controlador_movimiento = controlador_movimiento
        self.usuario = usuario

        tk.Label(self.top, text="Código de producto:").pack(pady=5)
        self.combo_codigos = ttk.Combobox(
            self.top,
            values=[p.get_codigo() for p in controlador_producto.listar_productos()],
            state="readonly"
        )
        self.combo_codigos.pack()

        tk.Label(self.top, text="Tipo de movimiento:").pack(pady=5)
        self.tipo_combo = ttk.Combobox(self.top, values=["entrada", "salida"], state="readonly")
        self.tipo_combo.pack()

        tk.Label(self.top, text="Cantidad:").pack(pady=5)
        self.spin_cantidad = tk.Spinbox(self.top, from_=1, to=100, width=5)
        self.spin_cantidad.pack()

        tk.Label(self.top, text="Motivo (opcional):").pack(pady=5)
        self.entry_motivo = tk.Entry(self.top)
        self.entry_motivo.pack()

        tk.Button(self.top, text="Registrar", command=self.registrar_movimiento).pack(pady=10)

    def registrar_movimiento(self):
        codigo = self.combo_codigos.get()
        tipo = self.tipo_combo.get()
        motivo = self.entry_motivo.get().strip()

        try:
            cantidad = int(self.spin_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido.")
            return

        if not codigo or not tipo:
            messagebox.showerror("Error", "Todos los campos obligatorios deben estar completos.")
            return

        producto = self.controlador_producto.obtener_producto(codigo)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        if tipo == "salida" and cantidad > producto.get_stock():
            messagebox.showerror("Error", "No hay suficiente stock disponible.")
            return

        nuevo_stock = producto.get_stock() + cantidad if tipo == "entrada" else producto.get_stock() - cantidad
        producto.set_stock(nuevo_stock)
        producto.set_fechaActualizacion(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.controlador_movimiento.registrar_movimiento(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            codigo,
            tipo,
            cantidad,
            self.usuario.get_username(),
            motivo
        )

        messagebox.showinfo("Éxito", "Movimiento registrado correctamente.")
        self.top.destroy()

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Entidades.Solicitud import Solicitud

class VistaRegistrarSolicitud:
    def __init__(self, root, controlador_producto, controlador_solicitud, usuario):
        self.top = tk.Toplevel(root)
        self.top.title("Solicitar Producto")
        self.top.geometry("400x300")

        self.controlador_producto = controlador_producto
        self.controlador_solicitud = controlador_solicitud
        self.usuario = usuario

        tk.Label(self.top, text="Código de producto:").pack(pady=5)
        self.combo_codigos = ttk.Combobox(
            self.top,
            values=[p.get_codigo() for p in controlador_producto.listar_productos()],
            state="readonly"
        )
        self.combo_codigos.pack()

        tk.Label(self.top, text="Cantidad:").pack(pady=5)
        self.entry_cantidad = tk.Entry(self.top)
        self.entry_cantidad.pack()

        tk.Button(self.top, text="Enviar Solicitud", command=self.enviar_solicitud).pack(pady=10)

    def enviar_solicitud(self):
        codigo = self.combo_codigos.get()
        cantidad_str = self.entry_cantidad.get()

        if not codigo or not cantidad_str.isdigit():
            messagebox.showerror("Error", "Completa todos los campos correctamente.")
            return

        cantidad = int(cantidad_str)
        producto = self.controlador_producto.obtener_producto(codigo)

        if not producto:
            messagebox.showerror("Error", "Producto no válido.")
            return

       

        self.controlador_solicitud.registrar_solicitud(self.usuario.get_username(),producto,cantidad,"pendiente",datetime.now())
        messagebox.showinfo("Éxito", "Solicitud registrada exitosamente.")
        self.top.destroy()

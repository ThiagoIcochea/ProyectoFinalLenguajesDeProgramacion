import tkinter as tk
from tkinter import ttk

class VistaVerSolicitudes:
    def __init__(self, root, controlador_solicitud, usuario):
        self.top = tk.Toplevel(root)
        self.top.title("Solicitudes")
        self.top.geometry("800x400")
        self.controlador_solicitud = controlador_solicitud
        self.usuario = usuario

        self._crear_interfaz()

    def _crear_interfaz(self):
        label_titulo = tk.Label(self.top, text="Solicitudes", font=("Arial", 16))
        label_titulo.pack(pady=10)

        columnas = ("ID", "Producto", "Cantidad", "Fecha", "Estado", "Solicitante")
        self.tree = ttk.Treeview(self.top, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._cargar_datos()

    def _cargar_datos(self):
        solicitudes = self.controlador_solicitud.listar_solicitudes()

        rol = self.usuario.get_rol().strip().lower()
        nombre_usuario = self.usuario.get_username()

        for solicitud in solicitudes:
            id_sol = solicitud.get_id()
            producto = solicitud.get_producto().get_nombre()
            cantidad = solicitud.get_cantidad()
            fecha = solicitud.get_fecha()
            estado = solicitud.get_estado()
            solicitante = solicitud.get_empleado()

            if rol == "responsable" or (rol == "empleado" and solicitante == nombre_usuario):
                self.tree.insert("", "end", values=(id_sol, producto, cantidad, fecha, estado, solicitante))

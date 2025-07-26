import tkinter as tk
from tkinter import ttk

class VistaVerSolicitudes:
    def __init__(self, root, controlador_solicitud, usuario):
        self.top = tk.Toplevel(root)
        self.top.title("Solicitudes")
        self.top.geometry("900x500")
        self.top.configure(bg="#F5F5F5")  # Fondo claro
        self.controlador_solicitud = controlador_solicitud
        self.usuario = usuario

        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.top, bg="#FFFFFF", bd=1, relief="solid")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg="#0078D7")  # Color de acento azul
        self.title_frame.pack(fill="x", pady=(0, 20))

        titulo_label = tk.Label(
            self.title_frame,
            text="SOLICITUDES",
            font=("Segoe UI", 16, "bold"),
            bg="#0078D7",
            fg="#FFFFFF",
            pady=10
        )
        titulo_label.pack()

        # Contenedor para la tabla
        self.table_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Estilo personalizado para el Treeview
        self.style = ttk.Style()
        self.style.configure("Futurista.Treeview",
                             background="#FFFFFF",
                             foreground="#333333",
                             rowheight=30,
                             fieldbackground="#FFFFFF")
        self.style.map('Futurista.Treeview',
                       background=[('selected', "#0078D7")],
                       foreground=[('selected', "#FFFFFF")])

        self.style.configure("Futurista.Treeview.Heading",
                             background="#0078D7",
                             foreground="#373737",
                             relief="flat",
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Futurista.Treeview.Heading",
                       background=[('active', "#005BB5")])

        # Treeview para mostrar solicitudes
        columnas = ("ID", "Producto", "Cantidad", "Fecha", "Estado", "Solicitante")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columnas,
            show="headings",
            style="Futurista.Treeview"
        )

        # Configurar columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # Agregar scrollbar
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self._cargar_datos()

    def _cargar_datos(self):
        solicitudes = self.controlador_solicitud.listar_solicitudes()

        rol = self.usuario.get_rol().strip().lower()
        nombre_usuario = self.usuario.get_username()

        self.tree.delete(*self.tree.get_children())
        for solicitud in solicitudes:
            id_sol = solicitud.get_id()
            producto = solicitud.get_producto().get_nombre()
            cantidad = solicitud.get_cantidad()
            fecha = solicitud.get_fecha()
            estado = solicitud.get_estado()
            solicitante = solicitud.get_empleado()

            if rol == "responsable" or (rol == "empleado" and solicitante == nombre_usuario):
                self.tree.insert("", "end", values=(id_sol, producto, cantidad, fecha, estado, solicitante))

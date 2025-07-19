import tkinter as tk
from tkinter import Menu
from Controladoras.ControladorProducto import ControladorProducto
from Controladoras.ControladorMovimiento import ControladorMovimiento
from Controladoras.ControladorSolicitud import ControladorSolicitud

class VistaMenu:
    def __init__(self, usuario, controlador_usuario, controlador_producto, controlador_movimiento,controlador_solicitudes):
        self.usuario = usuario
        self.controlador_usuario = controlador_usuario
        self.controlador_producto = controlador_producto
        self.controlador_movimiento = controlador_movimiento
        self.controlador_solicitud = controlador_solicitudes

        self.crearProductos()

        self.root = tk.Tk()
        self.root.title("Gestor de Inventarios")
        self.root.geometry("800x500")

        self._crear_menu()

        self.label_bienvenida = tk.Label(
            self.root,
            text=f"Ten una cordial bienvenida, {usuario.get_nombre()}, al Gestor de Inventarios",
            font=("Arial", 14),
            wraplength=600,
            justify="center"
        )
        self.label_bienvenida.pack(expand=True)

        self.root.mainloop()

    def _crear_menu(self):
        menu_bar = Menu(self.root)
        rol = self.usuario.get_rol().strip().lower()

        menu_productos = Menu(menu_bar, tearoff=0)
        if rol in ["admin", "responsable"]:
            menu_productos.add_command(label="Agregar producto", command=self.agregar_producto)
            menu_productos.add_command(label="Editar stock", command=self.editar_stock)
        menu_productos.add_command(label="Ver productos", command=self.ver_productos)
        menu_bar.add_cascade(label="Productos", menu=menu_productos)

        if rol == "admin":
            menu_usuarios = Menu(menu_bar, tearoff=0)
            menu_usuarios.add_command(label="Agregar usuario", command=self.agregar_usuario)
            menu_usuarios.add_command(label="Ver usuarios", command=self.ver_usuarios)
            menu_bar.add_cascade(label="Usuarios", menu=menu_usuarios)

        if rol in ["admin", "responsable"]:
            menu_mov = Menu(menu_bar, tearoff=0)
            menu_mov.add_command(label="Registrar movimiento", command=self.registrar_movimiento)
            menu_mov.add_command(label="Ver movimientos", command=self.ver_movimientos)
            menu_bar.add_cascade(label="Movimientos", menu=menu_mov)

        if rol == "responsable":
            menu_reportes = Menu(menu_bar, tearoff=0)
            menu_reportes.add_command(label="Reporte de Stock", command=self.reporte_stock)
            menu_bar.add_cascade(label="Reportes", menu=menu_reportes)

            menu_sol_resp = Menu(menu_bar, tearoff=0)
            menu_sol_resp.add_command(label="Gestionar solicitudes", command=self.gestionar_solicitudes)
            menu_sol_resp.add_command(label="Ver solicitudes", command=self.ver_solicitudes)
            menu_bar.add_cascade(label="Solicitudes", menu=menu_sol_resp)

        if rol == "empleado":
            menu_sol_emp = Menu(menu_bar, tearoff=0)
            menu_sol_emp.add_command(label="Solicitar producto", command=self.solicitar_producto)
            menu_sol_emp.add_command(label="Ver solicitudes", command=self.ver_solicitudes)
            menu_bar.add_cascade(label="Solicitudes", menu=menu_sol_emp)
            

        menu_usuario = Menu(menu_bar, tearoff=0)
        menu_usuario.add_command(label="Cerrar sesión", command=self.cerrar_sesion)
        menu_bar.add_cascade(label=self.usuario.get_nombre(), menu=menu_usuario)

        self.root.config(menu=menu_bar)

    def agregar_producto(self):
        from Vistas.VistaAgregarProducto import VistaAgregarProducto
        VistaAgregarProducto(self.root, self.controlador_producto)

    def ver_productos(self):
        from Vistas.VistaVerProductos import VistaVerProductos
        VistaVerProductos(self.root, self.controlador_producto)

    def editar_stock(self):
        from Vistas.VistaEditarStock import VistaEditarStock
        VistaEditarStock(self.root, self.controlador_producto)

    def agregar_usuario(self):
        from Vistas.VistaAgregarUsuario import VistaAgregarUsuario
        VistaAgregarUsuario(self.root, self.controlador_usuario)

    def ver_usuarios(self):
        from Vistas.VistaVerUsuarios import VistaVerUsuarios
        VistaVerUsuarios(self.root, self.controlador_usuario)

    def registrar_movimiento(self):
        from Vistas.VistaRegistrarMovimiento import VistaRegistrarMovimiento
        VistaRegistrarMovimiento(self.root, self.controlador_producto, self.controlador_movimiento, self.usuario)

    def ver_movimientos(self):
        from Vistas.VistaVerMovimientos import VistaVerMovimientos
        VistaVerMovimientos(self.root, self.controlador_movimiento)

    def reporte_stock(self):
        from Vistas.VistaReporteStock import VistaReporteStock
        VistaReporteStock(self.root, self.controlador_producto.listar_productos())

    def solicitar_producto(self):
        from Vistas.VistaRegistrarSolicitud import VistaRegistrarSolicitud
        VistaRegistrarSolicitud(self.root, self.controlador_producto, self.controlador_solicitud, self.usuario)

    def gestionar_solicitudes(self):
        from Vistas.VistaGestionarSolicitudes import VistaGestionarSolicitudes
        VistaGestionarSolicitudes(self.root, self.controlador_solicitud)

    def ver_solicitudes(self):
        from Vistas.VistaVerSolicitudes import VistaVerSolicitudes
        VistaVerSolicitudes(self.root, self.controlador_solicitud, self.usuario)

    def cerrar_sesion(self):
        self.root.destroy()
        from Vistas.VistaLogin import VistaLogin
        tk_root = tk.Tk()
        VistaLogin(tk_root, self.controlador_usuario, self.controlador_producto, self.controlador_movimiento, self.controlador_solicitud)
        tk_root.mainloop()

    def crearProductos(self):
        self.controlador_producto.agregar_producto("P001", "Silla ejecutiva", "Silla ergonómica con ruedas", "OfiCorp", "Muebles", 15)
        self.controlador_producto.agregar_producto("P002", "Escritorio", "Escritorio de madera con cajones", "MobiOficina", "Muebles", 10)
        self.controlador_producto.agregar_producto("P003", "Laptop Lenovo", "Laptop Lenovo ThinkPad", "TechWorld", "Tecnología", 8)
        self.controlador_producto.agregar_producto("P004", "Monitor Dell", "Monitor LED 24 pulgadas", "Dell", "Tecnología", 12)
        self.controlador_producto.agregar_producto("P005", "Impresora HP", "Impresora multifunción", "HP", "Tecnología", 5)
        self.controlador_producto.agregar_producto("P006", "Pizarra acrílica", "Pizarra blanca con marco de aluminio", "OfiCorp", "Utilitarios", 7)
        self.controlador_producto.agregar_producto("P007", "Archivador metálico", "Archivador de 4 gavetas", "AlmacenamientoPlus", "Muebles", 6)
        self.controlador_producto.agregar_producto("P008", "Proyector Epson", "Proyector HD con HDMI", "Epson", "Tecnología", 4)
        self.controlador_producto.agregar_producto("P009", "Teléfono IP", "Teléfono de escritorio VoIP", "Cisco", "Tecnología", 10)
        self.controlador_producto.agregar_producto("P010", "Router WiFi", "Router doble banda para oficinas", "TP-Link", "Tecnología", 9)

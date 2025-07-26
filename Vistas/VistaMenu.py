# Importación de bibliotecas necesarias para la interfaz
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw  # Para manejo de imágenes redimensionadas y circulares

# Vista principal del sistema después del login
class VistaMenu:
    def __init__(self, usuario, controlador_usuario, controlador_producto, controlador_movimiento, controlador_solicitudes):
        self.usuario = usuario  # Usuario que ha iniciado sesión
        self.controlador_usuario = controlador_usuario
        self.controlador_producto = controlador_producto
        self.controlador_movimiento = controlador_movimiento
        self.controlador_solicitud = controlador_solicitudes

        # Carga productos por defecto al iniciar
        self.crearProductos()

        # Configuración inicial de la ventana principal
        self.root = tk.Tk()
        self.root.title("Gestor de Inventarios - Konecta")
        self.root.geometry("1200x720")

        # Configura layout en forma de grid: 2 columnas (sidebar + contenido)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Sidebar lateral izquierdo
        self.sidebar = tk.Frame(self.root, bg="#273c75", width=350)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Área de contenido principal
        self.content = tk.Frame(self.root, bg="white")
        self.content.grid(row=0, column=1, sticky="nsew")

        # Construcción de menú lateral y pantalla de bienvenida
        self._crear_sidebar()
        self._mostrar_bienvenida()

        # Ejecuta el loop de la interfaz gráfica
        self.root.mainloop()

    def _crear_sidebar(self):
        # Muestra el logo según el rol del usuario
        logo_path = self._get_logo_path()
        logo_image = Image.open(logo_path).resize((100, 100), Image.LANCZOS)
        logo_image = self._convert_to_circle(logo_image)
        self.logo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.sidebar, image=self.logo, bg="#273c75")
        logo_label.pack(pady=20)

        # Menú de productos
        self._crear_menu_desplegable("Productos", [
            ("Agregar producto", self.agregar_producto),
            ("Editar stock", self.editar_stock),
            ("Ver productos", self.ver_productos)
        ])

        # Menú solo para administradores
        if self.usuario.get_rol().strip().lower() == "admin":
            self._crear_menu_desplegable("Usuarios", [
                ("Agregar usuario", self.agregar_usuario),
                ("Ver usuarios", self.ver_usuarios)
            ])

        # Menú de movimientos
        self._crear_menu_desplegable("Movimientos", [
            ("Registrar movimiento", self.registrar_movimiento),
            ("Ver movimientos", self.ver_movimientos)
        ])

        # Menú para responsables (reportes y solicitudes)
        if self.usuario.get_rol().strip().lower() == "responsable":
            self._crear_menu_desplegable("Reportes", [
                ("Reporte de Stock", self.reporte_stock)
            ])
            self._crear_menu_desplegable("Solicitudes", [
                ("Gestionar solicitudes", self.gestionar_solicitudes),
                ("Ver solicitudes", self.ver_solicitudes)
            ])

        # Menú para empleados (solo solicitudes)
        if self.usuario.get_rol().strip().lower() == "empleado":
            self._crear_menu_desplegable("Solicitudes", [
                ("Solicitar producto", self.solicitar_producto),
                ("Ver solicitudes", self.ver_solicitudes)
            ])

        # Botón de cierre de sesión
        tk.Button(self.sidebar, text="Cerrar sesión", command=self.cerrar_sesion, bg="#dcdde1", fg="#273c75", relief="flat").pack(side="bottom", pady=20)

    def _convert_to_circle(self, image):
        # Convierte una imagen cuadrada en circular usando máscara
        size = image.size
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        result = Image.new("RGBA", size)
        result.paste(image, (0, 0), mask)
        return result

    def _crear_menu_desplegable(self, titulo, opciones):
        # Crea botones tipo acordeón con subopciones
        frame = tk.Frame(self.sidebar, bg="#273c75")
        frame.pack(fill="x", pady=10)

        btn_titulo = tk.Button(frame, text=titulo, bg="#273c75", fg="white", relief="flat", anchor="w")
        btn_titulo.pack(fill="x")

        subframe = tk.Frame(frame, bg="#273c75")

        def toggle():
            # Mostrar u ocultar el submenú
            if subframe.winfo_ismapped():
                subframe.pack_forget()
            else:
                subframe.pack(fill="x")

        btn_titulo.config(command=toggle)

        for label, command in opciones:
            # Crea cada opción dentro del submenú
            tk.Button(subframe, text=label, bg="#dcdde1", fg="#273c75", relief="flat", anchor="w", command=command).pack(fill="x")

    def _mostrar_bienvenida(self):
        # Muestra mensaje inicial en el panel derecho
        label_bienvenida = tk.Label(
            self.content,
            text=f"Bienvenido, {self.usuario.get_nombre()} al Gestor de Inventarios",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#273c75",
            wraplength=800,
            justify="center"
        )
        label_bienvenida.pack(pady=20)

    def _get_logo_path(self):
        # Devuelve la ruta del logo según el rol del usuario
        rol = self.usuario.get_rol().strip().lower()
        if rol == "admin":
            return "Utils/assets/admin-logo.jpg"
        elif rol == "responsable":
            return "Utils/assets/responsable-logo.jpg"
        elif rol == "empleado":
            return "Utils/assets/empleado-logo.jpg"
        return "Utils/assets/default-logo.jpg"

    # ======================
    # Métodos de navegación
    # ======================

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
        # Cierra la ventana y vuelve al login
        self.root.destroy()
        from Vistas.VistaLogin import VistaLogin
        tk_root = tk.Tk()
        VistaLogin(tk_root, self.controlador_usuario, self.controlador_producto, self.controlador_movimiento, self.controlador_solicitud)
        tk_root.mainloop()

    def crearProductos(self):
        # Agrega productos predefinidos para pruebas
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

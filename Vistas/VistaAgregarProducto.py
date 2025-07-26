# Librerías necesarias para interfaz gráfica, imágenes, archivos y estilos
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont
import os
from functools import partial
import colorsys

# Paleta de colores definida para un estilo moderno/futurista
COLORES = {
    "bg_light": "#E3F2FD",
    "bg_medium": "#BBDEFB",
    "bg_dark": "#90CAF9",
    "accent": "#2196F3",
    "icon": "#242627",
    "accent_dark": "#1976D2",
    "white": "#FFFFFF",
    "off_white": "#F8F9FA",
    "text_dark": "#263238",
    "text_light": "#FFFFFF"
}

# Vista para registrar un nuevo producto en el inventario
class VistaAgregarProducto:
    def __init__(self, root, controlador_producto):
        # Se crea una ventana secundaria
        self.window = tk.Toplevel(root)
        self.window.title("Agregar Producto")
        self.window.geometry("750x550")
        self.window.minsize(700, 520)
        self.window.configure(bg=COLORES["bg_light"])
        self.controlador = controlador_producto

        self.crear_recursos()  # Cargar iconos y estilos visuales
        self.campos = {}       # Diccionario para almacenar campos de entrada

        # Frame principal centrado
        self.main_frame = tk.Frame(self.window, bg=COLORES["white"])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        self.aplicar_fondo_gradiente()  # Fondo degradado visual

        # Título principal
        self.title_frame = tk.Frame(self.main_frame, bg=COLORES["accent"])
        self.title_frame.pack(fill="x", pady=(0, 20))
        tk.Label(self.title_frame, text="NUEVO PRODUCTO", font=("Segoe UI", 16, "bold"),
                 bg=COLORES["accent"], fg=COLORES["white"], pady=10).pack()

        # Frame para los campos
        self.campos_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.campos_frame.pack(fill="both", expand=True, padx=20, pady=5)
        self.campos_frame.columnconfigure(0, weight=1)
        self.campos_frame.columnconfigure(1, weight=1)
        for i in range(4): self.campos_frame.rowconfigure(i, weight=1)

        # Campos de entrada
        self.crear_campo_estilizado("Código", "codigo", self.campos_frame, 0, 0)
        self.crear_campo_estilizado("Nombre", "nombre", self.campos_frame, 0, 1)
        self.crear_campo_estilizado("Descripción", "descripcion", self.campos_frame, 1, 0, columnspan=2)

        # ComboBox: Categoría
        categorias = ["Sillas", "Escritorios", "Computadoras", "Impresoras", "Papelería",
                      "Monitores", "Teclados", "Mouses", "Almacenamiento", "Otros"]
        self.crear_combobox_estilizado("Categoría", "categoria", categorias, self.campos_frame, 2, 0)

        # ComboBox: Proveedor
        proveedores = ["Office Depot", "Staples", "HP", "Lenovo", "Canon", "Epson",
                       "Logitech", "Samsung", "Amazon", "Otros"]
        self.crear_combobox_estilizado("Proveedor", "proveedor", proveedores, self.campos_frame, 2, 1)

        # Campo numérico: Stock
        self.crear_campo_estilizado("Stock inicial", "stock", self.campos_frame, 3, 0, is_numerico=True)

        # Botones inferiores
        self.btn_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.btn_frame.pack(fill="x", pady=10, padx=20)
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)

        # Botones de acción
        self.crear_boton(self.btn_frame, "Agregar producto", self.agregar, 0, 0, icon_name="check")
        self.crear_boton(self.btn_frame, "Importar Excel", self.importar_excel, 0, 1, icon_name="import")
        self.crear_boton(self.btn_frame, "Exportar Excel", self.exportar_excel, 0, 2, icon_name="export")

    # ========================
    # Lógica funcional
    # ========================

    def agregar(self):
        """Lógica para agregar un producto al sistema"""
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
        """Importar productos desde archivo Excel"""
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if ruta:
            try:
                cantidad = self.controlador.importar_desde_excel(ruta)
                messagebox.showinfo("Importación exitosa", f"Se importaron {cantidad} productos.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo importar: {str(e)}")

    def exportar_excel(self):
        """Exportar productos a archivo Excel"""
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if ruta:
            try:
                self.controlador.exportar_a_excel(ruta)
                messagebox.showinfo("Exportación exitosa", f"Productos exportados a:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    # ========================
    # Estilo y diseño UI
    # ========================

    def crear_recursos(self):
        """Carga iconos personalizados y estilos"""
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.iconos = {}
        self.crear_icono("check", self.dibujar_icono_check)
        self.crear_icono("import", self.dibujar_icono_import)
        self.crear_icono("export", self.dibujar_icono_export)

        self.style = ttk.Style()
        self.style.configure("Futurista.TCombobox", background=COLORES["white"],
                             fieldbackground=COLORES["white"], foreground=COLORES["text_dark"])

    def crear_icono(self, nombre, dibujar_funcion, tamano=24):
        """Genera un icono vectorial simple"""
        img = Image.new("RGBA", (tamano, tamano), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        dibujar_funcion(draw, tamano)
        self.iconos[nombre] = ImageTk.PhotoImage(img)

    def dibujar_icono_check(self, draw, t):  # ícono check ✔
        draw.line([(5, t/2), (t/2.5, t-8), (t-5, 5)], fill=COLORES["icon"], width=3)

    def dibujar_icono_import(self, draw, t):  # ícono import ⬇
        draw.line([(t/2, 3), (t/2, t-3)], fill=COLORES["icon"], width=2)
        draw.line([(t/2-5, t-8), (t/2, t-3), (t/2+5, t-8)], fill=COLORES["icon"], width=2)
        draw.line([(5, t-5), (t-5, t-5)], fill=COLORES["icon"], width=2)

    def dibujar_icono_export(self, draw, t):  # ícono export ⬆
        draw.line([(t/2, 3), (t/2, t-3)], fill=COLORES["icon"], width=2)
        draw.line([(t/2-5, 8), (t/2, 3), (t/2+5, 8)], fill=COLORES["icon"], width=2)
        draw.line([(5, t-5), (t-5, t-5)], fill=COLORES["icon"], width=2)

    def aplicar_fondo_gradiente(self):
        """Aplica un fondo degradado a toda la ventana"""
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()

        gradient = Image.new('RGBA', (width, height), color=0)
        draw = ImageDraw.Draw(gradient)
        color_top = self.hex_to_rgb(COLORES["bg_light"])
        color_bottom = self.hex_to_rgb(COLORES["bg_dark"])

        for y in range(height):
            ratio = y / height
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        path = os.path.join(self.temp_dir, "gradient_bg.png")
        gradient.save(path)

        self.bg_image = ImageTk.PhotoImage(file=path)
        bg_label = tk.Label(self.window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()

    def hex_to_rgb(self, hex_color):
        """Convierte un color en formato HEX a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def crear_campo_estilizado(self, label, key, parent, row, col, columnspan=1, is_largo=False, is_numerico=False):
        """Crea un campo Entry o Spinbox con estilos visuales"""
        frame = tk.Frame(parent, bg=COLORES["white"])
        frame.grid(row=row, column=col, padx=8, pady=5, sticky="nsew", columnspan=columnspan)

        tk.Label(frame, text=label, font=("Segoe UI", 10), bg=COLORES["white"], fg=COLORES["accent_dark"]).pack(anchor="w", pady=(0, 3))

        entry_frame = tk.Frame(frame, bg=COLORES["accent"], bd=0)
        entry_frame.pack(fill="x" if not is_largo else "both", expand=is_largo)

        inner_frame = tk.Frame(entry_frame, bg=COLORES["white"], bd=0)
        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

        if is_numerico:
            widget = tk.Spinbox(inner_frame, from_=0, to=99999, font=("Segoe UI", 10), bg=COLORES["white"], bd=0)
        else:
            widget = tk.Entry(inner_frame, font=("Segoe UI", 10), bg=COLORES["white"], bd=0)
        widget.pack(fill="both", expand=True, padx=8, pady=8)
        self.campos[key] = widget

    def crear_combobox_estilizado(self, label, key, values, parent, row, col):
        """Combobox con estilo personalizado"""
        frame = tk.Frame(parent, bg=COLORES["white"])
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        tk.Label(frame, text=label, font=("Segoe UI", 10), bg=COLORES["white"], fg=COLORES["accent_dark"]).pack(anchor="w", pady=(0, 5))
        combo_frame = tk.Frame(frame, bg=COLORES["accent"])
        combo_frame.pack(fill="x")

        combo = ttk.Combobox(combo_frame, values=values, state="readonly", style="Futurista.TCombobox")
        combo.pack(fill="x", padx=1, pady=1)
        combo.current(0)
        self.campos[key] = combo

    def crear_boton(self, parent, texto, comando, row, col, icon_name=None):
        """Botón con estilo futurista e iconos"""
        container = tk.Frame(parent, bg=COLORES["white"])
        container.grid(row=row, column=col, padx=10, pady=10)

        btn = tk.Button(container, text="  " + texto if icon_name else texto,
                        font=("Segoe UI", 10, "bold"), bg=COLORES["accent"],
                        fg=COLORES["white"], activebackground=COLORES["accent_dark"],
                        relief="flat", bd=0, padx=15, pady=8, cursor="hand2",
                        command=comando)

        if icon_name and icon_name in self.iconos:
            btn.config(image=self.iconos[icon_name], compound="left")

        btn.pack()
        btn.bind("<Enter>", lambda e: btn.config(bg=COLORES["accent_dark"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLORES["accent"]))
        return btn

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont
import os
from functools import partial
import colorsys

# Constantes de estilo futurista
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

class VistaAgregarProducto:
    def __init__(self, root, controlador_producto):
        self.window = tk.Toplevel(root)
        self.window.title("Agregar Producto")
        self.window.geometry("750x550")
        self.window.minsize(700, 520)  # Tamaño mínimo para evitar distorsiones
        self.window.configure(bg=COLORES["bg_light"])
        self.controlador = controlador_producto
        
        # Crear recursos visuales
        self.crear_recursos()
        
        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.window, bg=COLORES["white"])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
        # Aplicar fondo con gradiente
        self.aplicar_fondo_gradiente()

        self.campos = {}

        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg=COLORES["accent"])
        self.title_frame.pack(fill="x", pady=(0, 20))
        
        titulo_label = tk.Label(
            self.title_frame, 
            text="NUEVO PRODUCTO",
            font=("Segoe UI", 16, "bold"),
            bg=COLORES["accent"],
            fg=COLORES["white"],
            pady=10
        )
        titulo_label.pack()
        
        # Contenedor para los campos
        self.campos_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.campos_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Configurar el grid
        self.campos_frame.columnconfigure(0, weight=1)
        self.campos_frame.columnconfigure(1, weight=1)
        
        # Configurar filas con espacio uniforme
        for i in range(4):
            self.campos_frame.rowconfigure(i, weight=1)
        
        # Crear campos con estilo moderno en dos columnas
        self.crear_campo_estilizado("Código", "codigo", self.campos_frame, 0, 0)
        self.crear_campo_estilizado("Nombre", "nombre", self.campos_frame, 0, 1)
        self.crear_campo_estilizado("Descripción", "descripcion", self.campos_frame, 1, 0, columnspan=2)
        
        # Categorías
        categorias = [
            "Sillas", "Escritorios", "Computadoras", "Impresoras",
            "Papelería", "Monitores", "Teclados", "Mouses",
            "Almacenamiento", "Otros"
        ]
        self.crear_combobox_estilizado("Categoría", "categoria", categorias, self.campos_frame, 2, 0)

        # Proveedores
        proveedores = [
            "Office Depot", "Staples", "HP", "Lenovo", "Canon",
            "Epson", "Logitech", "Samsung", "Amazon", "Otros"
        ]
        self.crear_combobox_estilizado("Proveedor", "proveedor", proveedores, self.campos_frame, 2, 1)
        
        # Stock inicial
        self.crear_campo_estilizado("Stock inicial", "stock", self.campos_frame, 3, 0, is_numerico=True)
        
        # Panel de botones con efecto glassmorphism
        self.btn_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.btn_frame.pack(fill="x", pady=10, padx=20)
        
        # Configurar el grid de botones
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)
        
        # Botones modernos
        self.crear_boton(
            self.btn_frame, 
            "Agregar producto", 
            self.agregar, 
            0, 0, 
            icon_name="check"
        )
        
        self.crear_boton(
            self.btn_frame, 
            "Importar Excel", 
            self.importar_excel, 
            0, 1, 
            icon_name="import"
        )
        
        self.crear_boton(
            self.btn_frame, 
            "Exportar Excel", 
            self.exportar_excel, 
            0, 2, 
            icon_name="export"
        )

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

    # Métodos para UI futurista
    def crear_recursos(self):
        """Crea recursos visuales como iconos y estilos"""
        # Crear directorio temporal para recursos si no existe
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Diccionario para almacenar iconos
        self.iconos = {}
        
        # Crear iconos vectoriales
        self.crear_icono("check", self.dibujar_icono_check)
        self.crear_icono("import", self.dibujar_icono_import)
        self.crear_icono("export", self.dibujar_icono_export)
        
        # Crear estilo para widgets
        self.style = ttk.Style()
        self.style.configure(
            "Futurista.TCombobox",
            background=COLORES["white"],
            fieldbackground=COLORES["white"],
            foreground=COLORES["text_dark"],
            borderwidth=0
        )

    def crear_icono(self, nombre, dibujar_funcion, tamano=24):
        """Crea un icono vectorial y lo guarda como PhotoImage"""
        # Crear imagen con fondo transparente
        img = Image.new("RGBA", (tamano, tamano), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Dibujar el icono llamando a la función específica
        dibujar_funcion(draw, tamano)
        
        # Convertir a PhotoImage
        photo_img = ImageTk.PhotoImage(img)
        self.iconos[nombre] = photo_img
        
    def dibujar_icono_check(self, draw, tamano):
        """Dibuja un icono de check (marca de verificación)"""
        color = COLORES["icon"]
        # Dibujar check
        draw.line([(5, tamano/2), (tamano/2.5, tamano-8), (tamano-5, 5)], 
                  fill=color, width=3)
    
    def dibujar_icono_import(self, draw, tamano):
        """Dibuja un icono de importación (flecha hacia abajo)"""
        color = COLORES["icon"]
        # Dibujar flecha hacia abajo
        draw.line([(tamano/2, 3), (tamano/2, tamano-3)], fill=color, width=2)
        draw.line([(tamano/2-5, tamano-8), (tamano/2, tamano-3), (tamano/2+5, tamano-8)], 
                  fill=color, width=2)
        # Dibujar base
        draw.line([(5, tamano-5), (tamano-5, tamano-5)], fill=color, width=2)
    
    def dibujar_icono_export(self, draw, tamano):
        """Dibuja un icono de exportación (flecha hacia arriba)"""
        color = COLORES["icon"]
        # Dibujar flecha hacia arriba
        draw.line([(tamano/2, 3), (tamano/2, tamano-3)], fill=color, width=2)
        draw.line([(tamano/2-5, 8), (tamano/2, 3), (tamano/2+5, 8)], 
                  fill=color, width=2)
        # Dibujar base
        draw.line([(5, tamano-5), (tamano-5, tamano-5)], fill=color, width=2)

    def aplicar_fondo_gradiente(self):
        """Aplica un fondo con gradiente a la ventana"""
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        
        # Crear imagen de fondo con gradiente
        gradient = Image.new('RGBA', (width, height), color=0)
        draw = ImageDraw.Draw(gradient)
        
        # Convertir colores hex a RGB
        color_top = self.hex_to_rgb(COLORES["bg_light"])
        color_bottom = self.hex_to_rgb(COLORES["bg_dark"])
        
        # Dibujar gradiente
        for y in range(height):
            # Calcular color interpolado
            ratio = y / height
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Guardar imagen temporal 
        # Diego: Wtf osea realiza el gradiente y lo guarda en un archivo temporal? wtfff porque o que xd
        # pero está bueno y según copilot es para evitar problemas de rendimiento, asi que god, igual Yohaldo
        # tu lo explicas si el profe pregunta
        gradient_path = os.path.join(self.temp_dir, "gradient_bg.png")
        gradient.save(gradient_path)
        
        # Establecer como fondo
        self.bg_image = ImageTk.PhotoImage(file=gradient_path)
        bg_label = tk.Label(self.window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()  # Enviar al fondo
    
    def hex_to_rgb(self, hex_color):
        """Convierte un color hexadecimal a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def crear_campo_estilizado(self, label_text, key, parent, row, col, columnspan=1, is_largo=False, is_numerico=False):
        """Crea un campo de entrada estilizado con etiqueta"""
        # Frame contenedor
        frame = tk.Frame(parent, bg=COLORES["white"])
        frame.grid(row=row, column=col, padx=8, pady=5, sticky="nsew", columnspan=columnspan)
        
        # Etiqueta
        label = tk.Label(
            frame, 
            text=label_text, 
            font=("Segoe UI", 10), 
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        label.pack(anchor="w", pady=(0, 3))
        
        # Campo de entrada con borde redondeado (simulado)
        entry_frame = tk.Frame(frame, bg=COLORES["accent"], bd=0, highlightthickness=0)
        entry_frame.pack(fill="x" if not is_largo else "both", expand=is_largo)
        
        # Padding interior para simular borde redondeado
        inner_frame = tk.Frame(entry_frame, bg=COLORES["white"], bd=0)
        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Widget de entrada
        if is_numerico:
            spinbox = tk.Spinbox(
                inner_frame, 
                from_=0, 
                to=99999,
                font=("Segoe UI", 10),
                bg=COLORES["white"],
                bd=0,
                highlightthickness=0
            )
            spinbox.pack(fill="both", expand=True, padx=8, pady=8)
            self.campos[key] = spinbox
        else:
            entry = tk.Entry(
                inner_frame, 
                font=("Segoe UI", 10),
                bg=COLORES["white"],
                bd=0,
                highlightthickness=0
            )
            entry.pack(fill="both", expand=True, padx=8, pady=8)
            self.campos[key] = entry
    
    def crear_combobox_estilizado(self, label_text, key, valores, parent, row, col):
        """Crea un combobox estilizado con etiqueta"""
        # Frame contenedor
        frame = tk.Frame(parent, bg=COLORES["white"])
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Etiqueta
        label = tk.Label(
            frame, 
            text=label_text, 
            font=("Segoe UI", 10), 
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        label.pack(anchor="w", pady=(0, 5))
        
        # Combobox con borde simulado
        combo_frame = tk.Frame(frame, bg=COLORES["accent"], bd=0)
        combo_frame.pack(fill="x")
        
        # Combobox
        combo = ttk.Combobox(
            combo_frame, 
            values=valores, 
            state="readonly",
            style="Futurista.TCombobox"
        )
        combo.pack(fill="x", padx=1, pady=1)
        combo.current(0)
        
        self.campos[key] = combo

    def crear_boton(self, parent, texto, comando, row, col, icon_name=None):
        """Crea un botón moderno estilo glassmorphism"""
        # Frame contenedor para el botón con efecto de sombra
        btn_container = tk.Frame(parent, bg=COLORES["white"])
        btn_container.grid(row=row, column=col, padx=10, pady=10)
        
        # Botón principal con color de acento
        btn = tk.Button(
            btn_container, 
            text="  " + texto if icon_name else texto,
            font=("Segoe UI", 10, "bold"),
            bg=COLORES["accent"],
            fg=COLORES["white"],
            activebackground=COLORES["accent_dark"],
            activeforeground=COLORES["white"],
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=comando
        )
        btn.pack()
        
        # Agregar icono si se especificó
        if icon_name and icon_name in self.iconos:
            btn.config(compound="left", image=self.iconos[icon_name])
            
        # Efectos de hover
        btn.bind("<Enter>", lambda e: btn.config(bg=COLORES["accent_dark"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLORES["accent"]))
        
        return btn

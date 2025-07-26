import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont

# Constantes de estilo futurista
COLORES = {
    "bg_light": "#E3F2FD",
    "bg_medium": "#BBDEFB",
    "bg_dark": "#90CAF9",
    "accent": "#2196F3",
    "accent_dark": "#1976D2",
    "white": "#FFFFFF",
    "off_white": "#F8F9FA",
    "text_dark": "#263238",
    "text_light": "#FFFFFF"
}

class VistaEditarStock:
    def __init__(self, root, controlador_producto):
        self.window = tk.Toplevel(root)
        self.window.title("Editar Stock")
        self.window.geometry("530x450")
        self.window.minsize(480, 400)  # Aumentado el tamaño mínimo
        self.window.configure(bg=COLORES["bg_light"])
        self.controlador = controlador_producto
        
        # Crear recursos visuales
        self.crear_recursos()
        
        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.window, bg=COLORES["white"])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
        # Aplicar fondo con gradiente
        self.aplicar_fondo_gradiente()
        
        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg=COLORES["accent"])
        self.title_frame.pack(fill="x", pady=(0, 20))
        
        titulo_label = tk.Label(
            self.title_frame, 
            text="EDITAR STOCK",
            font=("Segoe UI", 16, "bold"),
            bg=COLORES["accent"],
            fg=COLORES["white"],
            pady=10
        )
        titulo_label.pack()
        
        # Contenedor para los campos
        self.campos_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.campos_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Etiqueta para el selector de producto
        selector_label = tk.Label(
            self.campos_frame, 
            text="Selecciona código de producto:", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        selector_label.pack(anchor="w", pady=(10, 5))
        
        # Combobox estilizado
        combo_frame = tk.Frame(self.campos_frame, bg=COLORES["accent"], bd=0)
        combo_frame.pack(fill="x", pady=5)
        
        self.codigos = [p.get_codigo() for p in self.controlador.listar_productos()]
        
        self.combo_codigos = ttk.Combobox(
            combo_frame, 
            values=self.codigos, 
            state="readonly",
            font=("Segoe UI", 10),
            style="Futurista.TCombobox"
        )
        self.combo_codigos.pack(fill="x", padx=1, pady=1)
        self.combo_codigos.bind("<<ComboboxSelected>>", self.cargar_stock_actual)

        # Sección de stock actual
        self.info_frame = tk.Frame(self.campos_frame, bg=COLORES["bg_light"], bd=0)
        self.info_frame.pack(fill="x", pady=10)
        self.info_frame.pack_propagate(False)
        self.info_frame.configure(height=50)  # Reducido un poco la altura
        
        self.stock_actual_label = tk.Label(
            self.info_frame, 
            text="Stock actual: No seleccionado", 
            font=("Segoe UI", 11),
            bg=COLORES["bg_light"],
            fg=COLORES["text_dark"]
        )
        self.stock_actual_label.pack(anchor="center", pady=15)  # Reducido el padding
        
        # Etiqueta para nuevo stock
        nuevo_stock_label = tk.Label(
            self.campos_frame, 
            text="Nuevo stock:", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        nuevo_stock_label.pack(anchor="w", pady=(10, 5))  # Reducido el padding superior
        
        # Spinbox estilizado para el stock
        spin_frame = tk.Frame(self.campos_frame, bg=COLORES["accent"], bd=0)
        spin_frame.pack(fill="x", pady=5)
        
        inner_frame = tk.Frame(spin_frame, bg=COLORES["white"], bd=0)
        inner_frame.pack(fill="x", padx=1, pady=1)
        
        self.var_stock = tk.IntVar()
        self.spin_stock = tk.Spinbox(
            inner_frame, 
            from_=0, 
            to=100000, 
            textvariable=self.var_stock, 
            font=("Segoe UI", 11),
            bg=COLORES["white"],
            bd=0,
            highlightthickness=0
        )
        self.spin_stock.pack(padx=8, pady=6, fill="x")  # Reducido el padding vertical
        
        # Botón de actualización - ajustado para que siempre sea visible
        self.btn_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.btn_frame.pack(fill="x", pady=10, padx=20)  # Reducido el padding vertical
        
        # Configurar grid para centrar el botón
        self.btn_frame.columnconfigure(0, weight=1)
        
        # Crear botón
        self.crear_boton(
            self.btn_frame, 
            "Actualizar Stock", 
            self.actualizar_stock, 
            0, 0, 
            icon_name="update"
        )

    def cargar_stock_actual(self, event):
        codigo = self.combo_codigos.get()
        producto = self.controlador.obtener_producto(codigo)
        if producto:
            stock_actual = producto.get_stock()
            self.var_stock.set(stock_actual)
            self.stock_actual_label.config(text=f"Stock actual: {stock_actual}")
            # Cambiar color según nivel de stock
            if stock_actual <= 5:
                color = "#F44336"  # Rojo para stock bajo
            elif stock_actual <= 20:
                color = "#FF9800"  # Naranja para stock medio
            else:
                color = "#4CAF50"  # Verde para stock alto
            self.stock_actual_label.config(fg=color)

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
            
    # Métodos para UI futurista
    def crear_recursos(self):
        """Crea recursos visuales como iconos y estilos"""
        # Crear directorio temporal para recursos si no existe
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Diccionario para almacenar iconos
        self.iconos = {}
        
        # Crear iconos vectoriales
        self.crear_icono("update", self.dibujar_icono_update)
        
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
        
    def dibujar_icono_update(self, draw, tamano):
        """Dibuja un icono de actualización (refresh)"""
        color = COLORES["accent_dark"]
        # Dibujar un círculo para el refresh
        radio = tamano // 2 - 3
        centro_x, centro_y = tamano // 2, tamano // 2
        
        # Dibujar arco superior
        draw.arc([(centro_x-radio, centro_y-radio), (centro_x+radio, centro_y+radio)], 
                 30, 300, fill=color, width=2)
        
        # Dibujar flecha en el extremo
        arrow_x = centro_x + int(radio * 0.8)
        arrow_y = centro_y - int(radio * 0.8)
        draw.line([(arrow_x, arrow_y), (arrow_x+5, arrow_y-3)], fill=color, width=2)
        draw.line([(arrow_x, arrow_y), (arrow_x+3, arrow_y+5)], fill=color, width=2)

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
    
    def crear_boton(self, parent, texto, comando, row, col, icon_name=None):
        """Crea un botón moderno estilo glassmorphism"""
        # Frame contenedor para el botón con efecto de sombra
        btn_container = tk.Frame(parent, bg=COLORES["white"])
        btn_container.grid(row=row, column=col, padx=10, pady=5)  # Reducido el padding vertical
        
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
            padx=15,  # Reducido el padding horizontal
            pady=8,   # Reducido el padding vertical
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

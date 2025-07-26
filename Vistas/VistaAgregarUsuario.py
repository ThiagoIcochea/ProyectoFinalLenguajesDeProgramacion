import tkinter as tk
from tkinter import ttk, messagebox
import re
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

class VistaAgregarUsuario:
    def __init__(self, root, controlador):
        self.win = tk.Toplevel(root)
        self.win.title("Agregar Usuario")
        self.win.geometry("950x700")
        self.win.minsize(750, 580)  # Tamaño mínimo para evitar distorsiones
        self.win.configure(bg=COLORES["bg_light"])
        self.controlador = controlador
        
        # Crear recursos visuales
        self.crear_recursos()
        
        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.win, bg=COLORES["white"])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
        # Aplicar fondo con gradiente
        self.aplicar_fondo_gradiente()

        self.campos = {}

        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg=COLORES["accent"])
        self.title_frame.pack(fill="x", pady=(0, 20))
        
        titulo_label = tk.Label(
            self.title_frame, 
            text="REGISTRO DE USUARIO",
            font=("Segoe UI", 16, "bold"),
            bg=COLORES["accent"],
            fg=COLORES["white"],
            pady=10
        )
        titulo_label.pack()
        
        # Contenedor para los campos, dividido en columnas
        self.campos_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.campos_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Configurar el grid con pesos específicos para columnas
        self.campos_frame.columnconfigure(0, weight=1)
        self.campos_frame.columnconfigure(1, weight=1)
        
        # Configurar filas con espacio uniforme
        for i in range(8):
            self.campos_frame.rowconfigure(i, weight=1)
        
        # Datos personales
        titulo_personales = tk.Label(
            self.campos_frame, 
            text="Información Personal", 
            font=("Segoe UI", 12, "bold"),
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        titulo_personales.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Crear campos en la primera columna
        self.crear_campo_estilizado("Nombre", "nombre", self.campos_frame, 1, 0)
        self.crear_campo_estilizado("Apellido Paterno", "apellidoP", self.campos_frame, 2, 0)
        self.crear_campo_estilizado("Apellido Materno", "apellidoM", self.campos_frame, 3, 0)
        self.crear_campo_estilizado("DNI", "dni", self.campos_frame, 4, 0)
        
        # Datos de contacto
        titulo_contacto = tk.Label(
            self.campos_frame, 
            text="Información de Contacto", 
            font=("Segoe UI", 12, "bold"),
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        titulo_contacto.grid(row=0, column=1, sticky="w", pady=(0, 10))
        
        # Crear campos en la segunda columna
        self.crear_campo_estilizado("Teléfono", "telefono", self.campos_frame, 1, 1)
        self.crear_campo_estilizado("Correo", "correo", self.campos_frame, 2, 1)
        self.crear_campo_estilizado("Dirección", "direccion", self.campos_frame, 3, 1)
        
        # Campo edad con spinner
        self.crear_campo_numerico("Edad", "edad", self.campos_frame, 4, 1, min_val=18, max_val=120)
        
        # Datos de cuenta
        titulo_cuenta = tk.Label(
            self.campos_frame, 
            text="Información de Cuenta", 
            font=("Segoe UI", 12, "bold"),
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        titulo_cuenta.grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 10))
        
        # Campos de acceso
        self.crear_campo_estilizado("Username", "username", self.campos_frame, 6, 0)
        self.crear_campo_estilizado("Contraseña", "password", self.campos_frame, 6, 1, is_password=True)
        
        # Rol del usuario
        self.crear_combobox_estilizado("Rol de Usuario", "rol", ["admin", "responsable", "empleado"], self.campos_frame, 7, 0, columnspan=2)
        
        # Panel de botones
        self.btn_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.btn_frame.pack(fill="x", pady=15, padx=20)
        
        # Configurar el grid de botones
        self.btn_frame.columnconfigure(0, weight=1)
        
        # Botón de registro con icono
        self.crear_boton(
            self.btn_frame, 
            "Registrar Usuario", 
            self.registrar, 
            0, 0, 
            icon_name="user_add"
        )

    def registrar(self):
        datos = {k: v.get().strip() for k, v in self.campos.items()}

        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not datos["edad"].isdigit() or int(datos["edad"]) < 18:
            messagebox.showerror("Error", "La edad debe ser un número mayor o igual a 18.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", datos["correo"]):
            messagebox.showerror("Error", "Correo no válido.")
            return

        if not datos["dni"].isdigit() or len(datos["dni"]) != 8:
            messagebox.showerror("Error", "DNI inválido. Debe tener 8 dígitos.")
            return

        if self.controlador.verificar_dni(datos["dni"]):
            messagebox.showerror("Error", "El DNI ya está registrado.")
            return

        registrado = self.controlador.registrar_usuario(
            datos["username"], datos["password"], datos["nombre"],
            datos["apellidoP"], datos["apellidoM"], datos["edad"],
            datos["telefono"], datos["correo"], datos["direccion"],
            datos["dni"], datos["rol"]
        )

        if registrado:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.win.destroy()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya está en uso.")
            
    # Métodos para UI futurista
    def crear_recursos(self):
        """Crea recursos visuales como iconos y estilos"""
        # Crear directorio temporal para recursos si no existe
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Diccionario para almacenar iconos
        self.iconos = {}
        
        # Crear iconos vectoriales
        self.crear_icono("user_add", self.dibujar_icono_usuario)
        
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
        
    def dibujar_icono_usuario(self, draw, tamano):
        """Dibuja un icono de usuario con signo +"""
        color = COLORES["accent"]
        # Dibujar círculo para la cabeza
        draw.ellipse([(tamano/4, 2), (tamano*3/4, tamano/2)], outline=color, width=2)
        # Dibujar cuerpo
        draw.arc([(tamano/4, tamano/2), (tamano*3/4, tamano)], 0, 180, fill=color, width=2)
        # Dibujar signo +
        draw.line([(tamano*3/4+2, tamano/3), (tamano*3/4+8, tamano/3)], fill=color, width=2)
        draw.line([(tamano*3/4+5, tamano/3-3), (tamano*3/4+5, tamano/3+3)], fill=color, width=2)

    def aplicar_fondo_gradiente(self):
        """Aplica un fondo con gradiente a la ventana"""
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        
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
        bg_label = tk.Label(self.win, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()  # Enviar al fondo
    
    def hex_to_rgb(self, hex_color):
        """Convierte un color hexadecimal a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def crear_campo_estilizado(self, label_text, key, parent, row, col, columnspan=1, is_password=False):
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
        entry_frame.pack(fill="x", expand=True)
        
        # Padding interior para simular borde redondeado
        inner_frame = tk.Frame(entry_frame, bg=COLORES["white"], bd=0)
        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Widget de entrada
        entry = tk.Entry(
            inner_frame, 
            font=("Segoe UI", 10),
            bg=COLORES["white"],
            bd=0,
            highlightthickness=0,
            show="•" if is_password else ""
        )
        entry.pack(fill="both", expand=True, padx=6, pady=6)
        self.campos[key] = entry
    
    def crear_campo_numerico(self, label_text, key, parent, row, col, min_val=0, max_val=100):
        """Crea un campo numérico estilizado con etiqueta"""
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
        
        # Spinbox con borde redondeado (simulado)
        spin_frame = tk.Frame(frame, bg=COLORES["accent"], bd=0)
        spin_frame.pack(fill="x")
        
        # Inner padding
        inner_frame = tk.Frame(spin_frame, bg=COLORES["white"], bd=0)
        inner_frame.pack(fill="x", padx=1, pady=1)
        
        # Spinbox
        spinbox = tk.Spinbox(
            inner_frame,
            from_=min_val,
            to=max_val,
            font=("Segoe UI", 10),
            bg=COLORES["white"],
            bd=0,
            highlightthickness=0
        )
        spinbox.pack(padx=8, pady=8)
        self.campos[key] = spinbox
    
    def crear_combobox_estilizado(self, label_text, key, valores, parent, row, col, columnspan=1):
        """Crea un combobox estilizado con etiqueta"""
        # Frame contenedor
        frame = tk.Frame(parent, bg=COLORES["white"])
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew", columnspan=columnspan)
        
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

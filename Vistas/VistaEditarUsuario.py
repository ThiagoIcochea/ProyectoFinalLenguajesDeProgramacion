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

class VistaEditarUsuario:
    def __init__(self, root, controlador, username_preseleccionado=None):
        self.controlador = controlador
        self.win = tk.Toplevel(root)
        self.win.title("Editar Usuario")
        self.win.geometry("800x600")
        self.win.minsize(750, 580)  # Tamaño mínimo para evitar distorsiones
        self.win.configure(bg=COLORES["bg_light"])
        
        # Crear recursos visuales
        self.crear_recursos()
        
        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.win, bg=COLORES["white"])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
        # Aplicar fondo con gradiente
        self.aplicar_fondo_gradiente()
        
        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg=COLORES["accent"])
        self.title_frame.pack(fill="x", pady=(0, 20))
        
        titulo_label = tk.Label(
            self.title_frame, 
            text="EDITAR USUARIO",
            font=("Segoe UI", 16, "bold"),
            bg=COLORES["accent"],
            fg=COLORES["white"],
            pady=10
        )
        titulo_label.pack()
        
        # Selector de usuario
        selector_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        selector_frame.pack(fill="x", padx=20, pady=5)
        
        selector_label = tk.Label(
            selector_frame, 
            text="Selecciona un usuario:", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        selector_label.pack(anchor="w", pady=(0, 5))
        
        # Combobox estilizado
        combo_frame = tk.Frame(selector_frame, bg=COLORES["accent"], bd=0)
        combo_frame.pack(fill="x", pady=5)
        
        self.combo_usuarios = ttk.Combobox(
            combo_frame, 
            values=[u.get_username() for u in controlador.listar_usuarios()],
            font=("Segoe UI", 10),
            style="Futurista.TCombobox"
        )
        self.combo_usuarios.pack(fill="x", padx=1, pady=1)
        self.combo_usuarios.bind("<<ComboboxSelected>>", self.cargar_datos_usuario)
       

        # Contenedor para los campos, dividido en columnas
        self.campos_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.campos_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Configurar el grid con pesos específicos para columnas
        self.campos_frame.columnconfigure(0, weight=1)
        self.campos_frame.columnconfigure(1, weight=1)
        
        # Configurar filas con espacio uniforme
        for i in range(8):
            self.campos_frame.rowconfigure(i, weight=1)
        
        # Inicializar diccionario para almacenar campos
        self.campos = {}
        
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
        
        # Rol del usuario
        self.crear_combobox_estilizado("Rol de Usuario", "rol", ["admin", "responsable", "empleado"], self.campos_frame, 5, 0, columnspan=2)
        
        # Preseleccionar usuario si se especificó
        if username_preseleccionado:
            self.combo_usuarios.set(username_preseleccionado.get_username())
            self.cargar_datos_usuario(None)
        
        # Panel de botones
        self.btn_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.btn_frame.pack(fill="x", pady=15, padx=20)
        
        # Configurar grid para centrar el botón
        self.btn_frame.columnconfigure(0, weight=1)
        
        # Botón de guardar con icono
        self.crear_boton(
            self.btn_frame, 
            "Guardar Cambios", 
            self.actualizar_usuario, 
            0, 0, 
            icon_name="save"
        )

    def cargar_datos_usuario(self, event):
        """Carga los datos del usuario seleccionado en los campos"""
        username = self.combo_usuarios.get()
        if not username:
            return
            
        usuario = self.controlador.obtener_usuario(username)
        if usuario:
            # Mostrar mensaje de éxito
            self.mostrar_mensaje(f"Usuario '{username}' cargado correctamente", tipo="info")
            
            # Cargar datos en los campos
            self.campos["nombre"].delete(0, tk.END)
            self.campos["nombre"].insert(0, usuario.get_nombre())

            self.campos["apellidoP"].delete(0, tk.END)
            self.campos["apellidoP"].insert(0, usuario.get_apellidoP())

            self.campos["apellidoM"].delete(0, tk.END)
            self.campos["apellidoM"].insert(0, usuario.get_apellidoM())

            self.campos["edad"].delete(0, tk.END)
            self.campos["edad"].insert(0, usuario.get_edad())

            self.campos["telefono"].delete(0, tk.END)
            self.campos["telefono"].insert(0, usuario.get_telefono())

            self.campos["correo"].delete(0, tk.END)
            self.campos["correo"].insert(0, usuario.get_correo())

            self.campos["direccion"].delete(0, tk.END)
            self.campos["direccion"].insert(0, usuario.get_direccion())

            self.campos["dni"].delete(0, tk.END)
            self.campos["dni"].insert(0, usuario.get_dni())

            self.campos["rol"].set(usuario.get_rol())
            
    def mostrar_mensaje(self, mensaje, tipo="info"):
        """Muestra un mensaje en la interfaz"""
        color = {
            "info": COLORES["accent"],
            "error": "#F44336",
            "success": "#4CAF50"
        }.get(tipo, COLORES["accent"])
        
        # Si ya existe un mensaje, eliminarlo
        if hasattr(self, 'mensaje_label'):
            self.mensaje_label.destroy()
        
        # Crear nuevo mensaje
        self.mensaje_label = tk.Label(
            self.main_frame,
            text=mensaje,
            font=("Segoe UI", 10),
            bg=color,
            fg=COLORES["white"],
            pady=5
        )
        self.mensaje_label.pack(fill="x", pady=(5, 10))
        
        # Desaparecer después de 3 segundos
        self.win.after(3000, lambda: self.mensaje_label.destroy() if hasattr(self, 'mensaje_label') else None)

    def actualizar_usuario(self):
        """Valida y actualiza los datos del usuario"""
        username = self.combo_usuarios.get()
        if not username:
            self.mostrar_mensaje("Selecciona un usuario.", tipo="error")
            return

        datos = {k: v.get().strip() for k, v in self.campos.items()}

        # Validación de campos
        if not all(datos.values()):
            self.mostrar_mensaje("Todos los campos son obligatorios.", tipo="error")
            return

        if not datos["edad"].isdigit() or int(datos["edad"]) < 18:
            self.mostrar_mensaje("La edad debe ser un número mayor o igual a 18.", tipo="error")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", datos["correo"]):
            self.mostrar_mensaje("Correo no válido.", tipo="error")
            return

        if not datos["dni"].isdigit() or len(datos["dni"]) != 8:
            self.mostrar_mensaje("DNI inválido. Debe tener 8 dígitos.", tipo="error")
            return

        # Confirmar actualización
        confirmacion = messagebox.askyesno(
            "Confirmar actualización", 
            f"¿Estás seguro de actualizar los datos de {username}?"
        )
        
        if not confirmacion:
            return

        # Actualizar en el controlador
        actualizado = self.controlador.actualizar_usuario(
            username,
            datos["nombre"], datos["apellidoP"], datos["apellidoM"],
            datos["edad"], datos["telefono"], datos["correo"],
            datos["direccion"], datos["dni"], datos["rol"]
        )

        if actualizado:
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            self.win.destroy()
        else:
            self.mostrar_mensaje("No se pudo actualizar el usuario.", tipo="error")
            
    # Métodos para UI futurista
    def crear_recursos(self):
        """Crea recursos visuales como iconos y estilos"""
        # Crear directorio temporal para recursos si no existe
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Diccionario para almacenar iconos
        self.iconos = {}
        
        # Crear iconos vectoriales
        self.crear_icono("save", self.dibujar_icono_save)
        
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
        
    def dibujar_icono_save(self, draw, tamano):
        """Dibuja un icono de guardar (disquete)"""
        color = COLORES["white"]
        padding = 2
        
        # Cuerpo del disquete
        draw.rectangle(
            [(padding, padding), (tamano-padding, tamano-padding)],
            outline=color,
            width=2
        )
        
        # Parte superior del disquete
        draw.rectangle(
            [(tamano/3, padding), (tamano*2/3, tamano/3)],
            outline=color,
            width=1,
            fill=color
        )
        
        # Líneas decorativas
        draw.line([(tamano/4, tamano/2), (tamano*3/4, tamano/2)], fill=color, width=1)
        draw.line([(tamano/4, tamano*2/3), (tamano*3/4, tamano*2/3)], fill=color, width=1)
        draw.line([(tamano/4, tamano*5/6), (tamano*3/4, tamano*5/6)], fill=color, width=1)

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
        frame.grid(row=row, column=col, padx=8, pady=5, sticky="nsew")
        
        # Etiqueta
        label = tk.Label(
            frame, 
            text=label_text, 
            font=("Segoe UI", 10), 
            bg=COLORES["white"],
            fg=COLORES["accent_dark"]
        )
        label.pack(anchor="w", pady=(0, 3))
        
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
        spinbox.pack(padx=6, pady=6)
        self.campos[key] = spinbox
    
    def crear_combobox_estilizado(self, label_text, key, valores, parent, row, col, columnspan=1):
        """Crea un combobox estilizado con etiqueta"""
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
        btn_container.grid(row=row, column=col, padx=10, pady=5)
        
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

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
import colorsys

# Constantes de estilo futurista para toda la aplicación
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
    "text_light": "#FFFFFF",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336",
    "sidebar": "#273c75"
}

class EstiloApp:
    """Clase para manejar los estilos comunes de la aplicación"""
    
    @staticmethod
    def aplicar_tema():
        """Aplica el tema de la aplicación a los widgets ttk"""
        style = ttk.Style()
        
        # Estilo para Treeview
        style.configure(
            "Futurista.Treeview",
            background=COLORES["white"],
            foreground=COLORES["text_dark"],
            rowheight=25,
            fieldbackground=COLORES["white"],
            borderwidth=0,
            font=('Segoe UI', 10)
        )
        style.map('Futurista.Treeview',
                 background=[('selected', COLORES["accent"])],
                 foreground=[('selected', COLORES["white"])])
        
        # Estilo para encabezados de Treeview
        style.configure(
            "Futurista.Treeview.Heading",
            background=COLORES["accent_dark"],
            foreground=COLORES["white"],
            relief="flat",
            font=('Segoe UI', 10, 'bold')
        )
        style.map("Futurista.Treeview.Heading",
                 background=[('active', COLORES["accent"])])
        
        # Estilo para botones
        style.configure(
            "Futurista.TButton",
            background=COLORES["accent"],
            foreground=COLORES["white"],
            borderwidth=0,
            focusthickness=0,
            focuscolor=COLORES["accent"],
            font=('Segoe UI', 10),
            padding=10
        )
        style.map("Futurista.TButton",
                 background=[('active', COLORES["accent_dark"])])
        
        # Estilo para combobox
        style.configure(
            "Futurista.TCombobox",
            background=COLORES["white"],
            fieldbackground=COLORES["white"],
            foreground=COLORES["text_dark"],
            borderwidth=0,
            arrowsize=12
        )
        
        # Estilo para Entry
        style.configure(
            "Futurista.TEntry",
            background=COLORES["white"],
            foreground=COLORES["text_dark"],
            borderwidth=0,
            padding=5
        )
        
    @staticmethod
    def crear_boton_estilizado(parent, texto, comando, icon=None, ancho=None):
        """Crea un botón con estilo moderno"""
        frame = tk.Frame(parent, bg=COLORES["accent"], padx=1, pady=1, bd=0)
        inner_frame = tk.Frame(frame, bg=COLORES["white"], bd=0)
        inner_frame.pack(fill="both", expand=True)
        
        btn = tk.Button(
            inner_frame,
            text=texto,
            command=comando,
            bg=COLORES["accent"],
            fg=COLORES["white"],
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
            padx=15,
            pady=8,
            cursor="hand2"
        )
        
        if ancho:
            btn.config(width=ancho)
            
        btn.pack(fill="both", expand=True)
        
        # Efectos hover
        def on_enter(e):
            btn['background'] = COLORES["accent_dark"]
        
        def on_leave(e):
            btn['background'] = COLORES["accent"]
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return frame
    
    @staticmethod
    def crear_entrada_estilizada(parent, ancho=None):
        """Crea un campo de entrada estilizado"""
        frame = tk.Frame(parent, bg=COLORES["accent"], bd=0, highlightthickness=0)
        entry = tk.Entry(
            frame,
            bg=COLORES["white"],
            fg=COLORES["text_dark"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORES["bg_medium"],
            highlightcolor=COLORES["accent"],
            font=("Segoe UI", 10),
        )
        entry.pack(fill="both", expand=True, padx=1, pady=1)
        
        if ancho:
            entry.config(width=ancho)
            
        return frame, entry
    
    @staticmethod
    def crear_combobox_estilizado(parent, valores, ancho=None):
        """Crea un combobox estilizado"""
        combo = ttk.Combobox(
            parent,
            values=valores,
            state="readonly",
            style="Futurista.TCombobox",
            font=("Segoe UI", 10)
        )
        
        if ancho:
            combo.config(width=ancho)
            
        return combo
    
    @staticmethod
    def aplicar_fondo_gradiente(ventana, canvas=None):
        """Aplica un fondo con gradiente a la ventana"""
        if not canvas:
            canvas = tk.Canvas(ventana)
            canvas.pack(fill="both", expand=True)
            canvas.lower()
            
        width = ventana.winfo_screenwidth()
        height = ventana.winfo_screenheight()
        
        # Crear colores del gradiente
        color1 = EstiloApp.hex_to_rgb(COLORES["bg_light"])
        color2 = EstiloApp.hex_to_rgb(COLORES["bg_dark"])
        
        # Dibujar gradiente
        for i in range(height):
            # Interpolación de color
            r = int(color1[0] + (color2[0] - color1[0]) * i / height)
            g = int(color1[1] + (color2[1] - color1[1]) * i / height)
            b = int(color1[2] + (color2[2] - color1[2]) * i / height)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)
            
        return canvas
    
    @staticmethod
    def crear_panel_glassmorphism(parent, relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9):
        """Crea un panel con efecto glassmorphism"""
        frame = tk.Frame(
            parent,
            bg=COLORES["white"],
            highlightbackground=COLORES["bg_medium"],
            highlightthickness=1,
        )
        frame.place(relx=relx, rely=rely, anchor="center", relwidth=relwidth, relheight=relheight)
        
        return frame
    
    @staticmethod
    def crear_titulo(parent, texto):
        """Crea un panel de título con estilo moderno"""
        frame = tk.Frame(parent, bg=COLORES["accent"])
        frame.pack(fill="x", pady=(0, 20))
        
        label = tk.Label(
            frame,
            text=texto.upper(),
            font=("Segoe UI", 16, "bold"),
            bg=COLORES["accent"],
            fg=COLORES["white"],
            pady=10
        )
        label.pack()
        
        return frame
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """Convierte un color hexadecimal a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def configurar_tree_estilizado(tree):
        """Configura un Treeview con estilos modernos"""
        # Aplicar estilos
        tree.configure(style="Futurista.Treeview")
        
        # Configurar encabezados
        for col in tree["columns"]:
            tree.heading(col, text=col.title())
            tree.column(col, width=120)
            
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(tree.master, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        return tree

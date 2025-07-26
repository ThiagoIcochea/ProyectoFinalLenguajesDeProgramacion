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
    "text_light": "#FFFFFF",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "danger": "#F44336"
}

class VistaGestionarSolicitudes:
    def __init__(self, root, controlador_solicitud):
        self.root = tk.Toplevel(root)
        self.root.title("Gestionar Solicitudes")
        self.root.geometry("800x600")
        self.root.minsize(780, 580)
        self.root.configure(bg=COLORES["bg_light"])
        self.controlador_solicitud = controlador_solicitud
        
        # Crear recursos visuales
        self.crear_recursos()
        
        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.root, bg=COLORES["white"])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)
        
        # Aplicar fondo con gradiente
        self.aplicar_fondo_gradiente()
        
        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg=COLORES["accent"])
        self.title_frame.pack(fill="x", pady=(0, 15))
        
        titulo_label = tk.Label(
            self.title_frame, 
            text="GESTIÓN DE SOLICITUDES",
            font=("Segoe UI", 16, "bold"),
            bg=COLORES["accent"],
            fg=COLORES["white"],
            pady=10
        )
        titulo_label.pack()
        
        # Contenedor para la tabla y botones
        self.content_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Estilo personalizado para el Treeview
        self.style = ttk.Style()
        self.style.configure("Futurista.Treeview",
                            background=COLORES["white"],
                            foreground=COLORES["text_dark"],
                            rowheight=30,
                            fieldbackground=COLORES["white"])
        self.style.map('Futurista.Treeview',
                     background=[('selected', COLORES["accent_dark"])],
                     foreground=[('selected', COLORES["white"])])
        
        self.style.configure("Futurista.Treeview.Heading",
                           background=COLORES["accent"],
                           foreground=COLORES["white"],
                           relief="flat",
                           font=("Segoe UI", 10, "bold"))
        self.style.map("Futurista.Treeview.Heading",
                     background=[('active', COLORES["accent_dark"])])
        
        # Frame para el Treeview con borde
        self.tree_frame = tk.Frame(self.content_frame, bg=COLORES["accent"], bd=0)
        self.tree_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Treeview para mostrar solicitudes
        self.tree = ttk.Treeview(
            self.tree_frame, 
            columns=("ID", "Producto", "Cantidad", "Solicitante", "Estado"),
            show="headings",
            style="Futurista.Treeview"
        )
        
        # Configurar columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        
        # Configurar anchuras específicas para cada columna
        self.tree.column("ID", width=50)
        self.tree.column("Producto", width=150)
        self.tree.column("Cantidad", width=80)
        self.tree.column("Solicitante", width=150)
        self.tree.column("Estado", width=100)
        
        # Agregar scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # Panel de botones
        self.btn_frame = tk.Frame(self.main_frame, bg=COLORES["white"])
        self.btn_frame.pack(fill="x", pady=15, padx=20)
        
        # Crear botones modernos
        self.crear_boton(
            self.btn_frame, 
            "Aprobar Solicitud", 
            self.aprobar_solicitud, 
            0, 0, 
            icon_name="check",
            color=COLORES["success"]
        )
        
        self.crear_boton(
            self.btn_frame, 
            "Rechazar Solicitud", 
            self.rechazar_solicitud, 
            0, 1, 
            icon_name="cross",
            color=COLORES["danger"]
        )
        
        self.crear_boton(
            self.btn_frame, 
            "Actualizar", 
            self.cargar_solicitudes, 
            0, 2, 
            icon_name="refresh"
        )
        
        # Cargar solicitudes
        self.cargar_solicitudes()

    def cargar_solicitudes(self):
        # Limpiar tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Cargar solicitudes desde el controlador
        solicitudes = self.controlador_solicitud.listar_solicitudes()
        
        # Variable para controlar filas alternadas
        contador = 0
        
        # Insertar solicitudes pendientes
        for solicitud in solicitudes:
            if solicitud.get_estado() == "pendiente":
                # Insertar con tag para aplicar estilo
                item_id = self.tree.insert("", "end", values=(
                    solicitud.get_id(),
                    solicitud.get_producto().get_codigo(),
                    solicitud.get_cantidad(),
                    solicitud.get_empleado(),
                    solicitud.get_estado()
                ))
                
                # Aplicar color alternado a las filas
                if contador % 2 == 0:
                    self.tree.item(item_id, tags=("even",))
                else:
                    self.tree.item(item_id, tags=("odd",))
                contador += 1
        
        # Configurar tags para filas alternadas
        self.tree.tag_configure("even", background=COLORES["white"])
        self.tree.tag_configure("odd", background=COLORES["bg_light"])
        
        # Mostrar mensaje si no hay solicitudes
        if contador == 0:
            self.mostrar_mensaje_sin_datos()

    def mostrar_mensaje_sin_datos(self):
        """Muestra un mensaje cuando no hay datos disponibles"""
        # Insertar una fila con mensaje
        self.tree.insert("", "end", values=("", "No hay solicitudes pendientes", "", "", ""))
        
    def aprobar_solicitud(self):
        self.actualizar_estado("aprobada")

    def rechazar_solicitud(self):
        self.actualizar_estado("rechazada")

    def actualizar_estado(self, nuevo_estado):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una solicitud.")
            return

        item = self.tree.item(selected[0])
        valores = item["values"]
        
        # Verificar que es una fila válida (con ID)
        if not valores[0]:
            return
            
        id_solicitud = valores[0]
        
        # Mostrar diálogo de confirmación
        titulo = "Confirmar aprobación" if nuevo_estado == "aprobada" else "Confirmar rechazo"
        mensaje = f"¿Estás seguro de que deseas {nuevo_estado}r esta solicitud?"
        confirmacion = messagebox.askyesno(titulo, mensaje)
        
        if not confirmacion:
            return

        solicitud = next((s for s in self.controlador_solicitud.listar_solicitudes() if s.get_id() == id_solicitud), None)
        if solicitud is None:
            messagebox.showerror("Error", "Solicitud no encontrada.")
            return

        if nuevo_estado == "rechazada":
            self.controlador_solicitud.eliminar_solicitud(id_solicitud)
            messagebox.showinfo("Solicitud rechazada", "La solicitud ha sido eliminada.")
        else:
            solicitud.set_estado(nuevo_estado)
            messagebox.showinfo("Éxito", f"Solicitud marcada como {nuevo_estado}.")

        self.cargar_solicitudes()
        
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
        self.crear_icono("cross", self.dibujar_icono_cross)
        self.crear_icono("refresh", self.dibujar_icono_refresh)
    
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
        color = COLORES["white"]
        # Dibujar check
        draw.line([(5, tamano/2), (tamano/2.5, tamano-8), (tamano-5, 5)], 
                  fill=color, width=3)
    
    def dibujar_icono_cross(self, draw, tamano):
        """Dibuja un icono de X (cruz)"""
        color = COLORES["white"]
        padding = 5
        # Dibujar X
        draw.line([(padding, padding), (tamano-padding, tamano-padding)], fill=color, width=3)
        draw.line([(tamano-padding, padding), (padding, tamano-padding)], fill=color, width=3)
    
    def dibujar_icono_refresh(self, draw, tamano):
        """Dibuja un icono de actualización (refresh)"""
        color = COLORES["white"]
        # Dibujar un círculo para el refresh
        radio = tamano // 2 - 5
        centro_x, centro_y = tamano // 2, tamano // 2
        
        # Dibujar arco circular
        draw.arc([(centro_x-radio, centro_y-radio), (centro_x+radio, centro_y+radio)], 
                 30, 300, fill=color, width=2)
        
        # Dibujar flecha en el extremo
        arrow_x = centro_x + int(radio * 0.8)
        arrow_y = centro_y - int(radio * 0.8)
        draw.line([(arrow_x, arrow_y), (arrow_x+5, arrow_y-3)], fill=color, width=2)
        draw.line([(arrow_x, arrow_y), (arrow_x+3, arrow_y+5)], fill=color, width=2)

    def aplicar_fondo_gradiente(self):
        """Aplica un fondo con gradiente a la ventana"""
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        
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
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()  # Enviar al fondo
    
    def hex_to_rgb(self, hex_color):
        """Convierte un color hexadecimal a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def crear_boton(self, parent, texto, comando, row, col, icon_name=None, color=None):
        """Crea un botón moderno estilo glassmorphism"""
        if color is None:
            color = COLORES["accent"]
        
        # Frame contenedor para el botón
        btn_container = tk.Frame(parent, bg=COLORES["white"])
        btn_container.grid(row=row, column=col, padx=10, pady=10)
        
        # Botón principal con color personalizado
        btn = tk.Button(
            btn_container, 
            text="  " + texto if icon_name else texto,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg=COLORES["white"],
            activebackground=COLORES["accent_dark"] if color == COLORES["accent"] else color,
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
            
        # Color para efectos hover
        hover_color = self.oscurecer_color(color, factor=0.8)
            
        # Efectos de hover
        btn.bind("<Enter>", lambda e, c=hover_color: btn.config(bg=c))
        btn.bind("<Leave>", lambda e, c=color: btn.config(bg=c))
        
        return btn
        
    def oscurecer_color(self, hex_color, factor=0.8):
        """Oscurece un color hexadecimal por un factor dado"""
        # Convertir a RGB
        rgb = self.hex_to_rgb(hex_color)
        # Oscurecer
        rgb_oscuro = tuple(int(c * factor) for c in rgb)
        # Convertir de vuelta a hex
        hex_oscuro = '#{:02x}{:02x}{:02x}'.format(*rgb_oscuro)
        return hex_oscuro

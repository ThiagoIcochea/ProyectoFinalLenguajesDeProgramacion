import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Entidades.Solicitud import Solicitud

class VistaRegistrarSolicitud:
    def __init__(self, root, controlador_producto, controlador_solicitud, usuario):
        self.top = tk.Toplevel(root)
        self.top.title("Solicitar Producto")
        self.top.geometry("500x400")
        self.top.configure(bg="#F5F5F5")  # Fondo claro

        self.controlador_producto = controlador_producto
        self.controlador_solicitud = controlador_solicitud
        self.usuario = usuario

        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.top, bg="#FFFFFF", bd=1, relief="solid")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg="#0078D7")  # Color de acento azul
        self.title_frame.pack(fill="x", pady=(0, 20))

        titulo_label = tk.Label(
            self.title_frame,
            text="SOLICITAR PRODUCTO",
            font=("Segoe UI", 16, "bold"),
            bg="#0078D7",
            fg="#FFFFFF",
            pady=10
        )
        titulo_label.pack()

        # Contenedor para los campos
        self.campos_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.campos_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Configurar el grid
        self.campos_frame.columnconfigure(0, weight=1)
        self.campos_frame.columnconfigure(1, weight=1)

        # Crear campos con estilo moderno
        self.crear_campo_estilizado("Código de producto", "combo_codigos", [p.get_codigo() for p in controlador_producto.listar_productos()], self.campos_frame, 0, 0)
        self.crear_campo_numerico("Cantidad", "entry_cantidad", self.campos_frame, 1, 0, min_val=1, max_val=1000)

        # Botón de enviar solicitud
        self.btn_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.btn_frame.pack(fill="x", pady=10, padx=20)

        self.crear_boton(self.btn_frame, "Enviar Solicitud", self.enviar_solicitud, 0, 0)

    def crear_campo_estilizado(self, label_text, key, valores, parent, row, col, is_password=False):
        tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#333333"  # Texto oscuro
        ).grid(row=row, column=col, padx=10, pady=10, sticky="w")

        if valores:
            combo = ttk.Combobox(parent, values=valores, state="readonly")
            combo.grid(row=row, column=col + 1, padx=10, pady=10, sticky="ew")
            setattr(self, key, combo)
        else:
            entry = tk.Entry(parent, show="*" if is_password else None)
            entry.grid(row=row, column=col + 1, padx=10, pady=10, sticky="ew")
            setattr(self, key, entry)

    def crear_campo_numerico(self, label_text, key, parent, row, col, min_val=0, max_val=100):
        tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#333333"
        ).grid(row=row, column=col, padx=10, pady=10, sticky="w")

        spin = tk.Spinbox(parent, from_=min_val, to=max_val, width=10)
        spin.grid(row=row, column=col + 1, padx=10, pady=10, sticky="ew")
        setattr(self, key, spin)

    def crear_boton(self, parent, texto, comando, row, col):
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg="#0078D7",
            fg="#FFFFFF",
            font=("Segoe UI", 12),
            relief="flat"
        )
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

    def enviar_solicitud(self):
        codigo = self.combo_codigos.get()
        cantidad_str = self.entry_cantidad.get()

        if not codigo or not cantidad_str.isdigit():
            messagebox.showerror("Error", "Completa todos los campos correctamente.")
            return

        cantidad = int(cantidad_str)
        producto = self.controlador_producto.obtener_producto(codigo)

        if not producto:
            messagebox.showerror("Error", "Producto no válido.")
            return

       

        self.controlador_solicitud.registrar_solicitud(self.usuario.get_username(),producto,cantidad,"pendiente",datetime.now())
        messagebox.showinfo("Éxito", "Solicitud registrada exitosamente.")
        self.top.destroy()

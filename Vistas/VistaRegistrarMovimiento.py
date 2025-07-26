import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VistaRegistrarMovimiento:
    def __init__(self, root, controlador_producto, controlador_movimiento, usuario):
        self.top = tk.Toplevel(root)
        self.top.title("Registrar Movimiento")
        self.top.geometry("750x550")
        self.top.minsize(700, 520)
        self.top.configure(bg="#F5F5F5")  # Color de fondo claro

        self.controlador_producto = controlador_producto
        self.controlador_movimiento = controlador_movimiento
        self.usuario = usuario

        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.top, bg="#FFFFFF", bd=1, relief="solid")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg="#0078D7")  # Color de acento azul
        self.title_frame.pack(fill="x", pady=(0, 20))

        titulo_label = tk.Label(
            self.title_frame,
            text="REGISTRAR MOVIMIENTO",
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
        self.crear_campo_estilizado("Tipo de movimiento", "tipo_combo", ["entrada", "salida"], self.campos_frame, 1, 0)
        self.crear_campo_numerico("Cantidad", "spin_cantidad", self.campos_frame, 2, 0, min_val=1, max_val=1000)
        self.crear_campo_estilizado("Motivo (opcional)", "entry_motivo", None, self.campos_frame, 3, 0, is_password=False)

        # Botón de registrar
        self.btn_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.btn_frame.pack(fill="x", pady=10, padx=20)

        self.crear_boton(self.btn_frame, "Registrar Movimiento", self.registrar_movimiento, 0, 0)

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

    def registrar_movimiento(self):
        codigo = self.combo_codigos.get()
        tipo = self.tipo_combo.get()
        motivo = self.entry_motivo.get().strip()

        try:
            cantidad = int(self.spin_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido.")
            return

        if not codigo or not tipo:
            messagebox.showerror("Error", "Todos los campos obligatorios deben estar completos.")
            return

        producto = self.controlador_producto.obtener_producto(codigo)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        if tipo == "salida" and cantidad > producto.get_stock():
            messagebox.showerror("Error", "No hay suficiente stock disponible.")
            return

        nuevo_stock = producto.get_stock() + cantidad if tipo == "entrada" else producto.get_stock() - cantidad
        producto.set_stock(nuevo_stock)
        producto.set_fechaActualizacion(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.controlador_movimiento.registrar_movimiento(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            codigo,
            tipo,
            cantidad,
            self.usuario.get_username(),
            motivo
        )

        messagebox.showinfo("Éxito", "Movimiento registrado correctamente.")
        self.top.destroy()

import tkinter as tk
from tkinter import ttk, messagebox
from Vistas.VistaEditarUsuario import VistaEditarUsuario

class VistaVerUsuarios:
    def __init__(self, root, controlador_usuario):
        self.usuarios = controlador_usuario.listar_usuarios()
        self.win = tk.Toplevel(root)
        self.win.title("Lista de Usuarios")
        self.win.geometry("900x500")
        self.win.configure(bg="#F5F5F5")  # Fondo claro

        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.win, bg="#FFFFFF", bd=1, relief="solid")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg="#0078D7")  # Color de acento azul
        self.title_frame.pack(fill="x", pady=(0, 20))

        titulo_label = tk.Label(
            self.title_frame,
            text="LISTA DE USUARIOS",
            font=("Segoe UI", 16, "bold"),
            bg="#0078D7",
            fg="#FFFFFF",
            pady=10
        )
        titulo_label.pack()

        # Contenedor para los filtros
        self.filtro_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.filtro_frame.pack(pady=10)

        tk.Label(self.filtro_frame, text="Filtrar por nombre o usuario:", font=("Segoe UI", 12), bg="#FFFFFF", fg="#333333").grid(row=0, column=0, padx=5)
        self.entry_filtro = tk.Entry(self.filtro_frame)
        self.entry_filtro.grid(row=0, column=1, padx=5)

        self.crear_boton(self.filtro_frame, "Filtrar", self.filtrar, 0, 2)
        self.crear_boton(self.filtro_frame, "Limpiar", self.limpiar, 0, 3)

        # Contenedor para la tabla
        self.table_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Estilo personalizado para el Treeview
        self.style = ttk.Style()
        self.style.configure("Futurista.Treeview",
                             background="#FFFFFF",
                             foreground="#333333",
                             rowheight=30,
                             fieldbackground="#FFFFFF")
        self.style.map('Futurista.Treeview',
                       background=[('selected', "#0078D7")],
                       foreground=[('selected', "#FFFFFF")])

        self.style.configure("Futurista.Treeview.Heading",
                             background="#0078D7",
                             foreground="#303030",
                             relief="flat",
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Futurista.Treeview.Heading",
                       background=[('active', "#005BB5")])

        # Treeview para mostrar usuarios
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("usuario", "nombre", "rol"),
            show="headings",
            style="Futurista.Treeview"
        )

        # Configurar columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="center", width=150)

        # Agregar scrollbar
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.cargar_datos(self.usuarios)

    def cargar_datos(self, lista):
        self.tree.delete(*self.tree.get_children())
        for u in lista:
            self.tree.insert("", tk.END, values=(
                u.get_username(),
                u.get_nombre(),
                u.get_rol()
            ))

    def filtrar(self):
        texto = self.entry_filtro.get().lower()
        filtrados = [u for u in self.usuarios if texto in u.get_username().lower() or texto in u.get_nombre().lower()]
        self.cargar_datos(filtrados)

    def limpiar(self):
        self.entry_filtro.delete(0, tk.END)
        self.cargar_datos(self.usuarios)

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
        btn.grid(row=row, column=col, padx=5, pady=5)

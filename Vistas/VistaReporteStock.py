import tkinter as tk
from tkinter import ttk

class VistaReporteStock:
    def __init__(self, root, productos):
        self.win = tk.Toplevel(root)
        self.win.title("Reporte de Stock")
        self.win.geometry("800x500")
        self.win.configure(bg="#F5F5F5")  # Fondo claro

        # Frame principal con efecto glassmorphism
        self.main_frame = tk.Frame(self.win, bg="#FFFFFF", bd=1, relief="solid")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        # Panel de título
        self.title_frame = tk.Frame(self.main_frame, bg="#0078D7")  # Color de acento azul
        self.title_frame.pack(fill="x", pady=(0, 20))

        titulo_label = tk.Label(
            self.title_frame,
            text="REPORTE DE STOCK",
            font=("Segoe UI", 16, "bold"),
            bg="#0078D7",
            fg="#FFFFFF",
            pady=10
        )
        titulo_label.pack()

        # Contenedor para la tabla
        self.table_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Estilo personalizado para el Treeview
        self.style = ttk.Style()
        self.style.configure("Futurista.Treeview",
                             background="#FFFFFF",
                             foreground="#333333",
                             rowheight=30,
                             fieldbackground="#333232")
        self.style.map('Futurista.Treeview',
                       background=[('selected', "#0078D7")],
                       foreground=[('selected', "#FFF8F8")])

        self.style.configure("Futurista.Treeview.Heading",
                             background="#0078D7",
                             foreground="#373737",
                             relief="flat",
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Futurista.Treeview.Heading",
                       background=[('active', "#005BB5")])

        # Treeview para mostrar productos
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("codigo", "nombre", "stock", "categoria", "proveedor"),
            show="headings",
            style="Futurista.Treeview"
        )

        # Configurar columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="center", width=120)

        # Agregar scrollbar
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Insertar datos en la tabla
        for p in productos:
            self.tree.insert("", tk.END, values=(
                p.get_codigo(),
                p.get_nombre(),
                p.get_stock(),
                p.get_categoria(),
                p.get_proveedor()
            ))

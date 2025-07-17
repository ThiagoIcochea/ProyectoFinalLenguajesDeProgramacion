import tkinter as tk
from tkinter import ttk, messagebox
from Vistas.VistaEditarUsuario import VistaEditarUsuario

class VistaVerUsuarios:
    def __init__(self, root, controlador_usuario):
        self.usuarios = controlador_usuario.listar_usuarios()
        self.win = tk.Toplevel(root)
        self.win.title("Lista de Usuarios")
        self.win.geometry("800x500")

        filtro_frame = tk.Frame(self.win)
        filtro_frame.pack(pady=10)

        tk.Label(filtro_frame, text="Filtrar por nombre o usuario:").grid(row=0, column=0, padx=5)
        self.entry_filtro = tk.Entry(filtro_frame)
        self.entry_filtro.grid(row=0, column=1, padx=5)
        tk.Button(filtro_frame, text="Filtrar", command=self.filtrar).grid(row=0, column=2, padx=5)
        tk.Button(filtro_frame, text="Limpiar", command=self.limpiar).grid(row=0, column=3, padx=5)

        self.tree = ttk.Treeview(self.win, columns=("usuario", "nombre", "rol"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

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

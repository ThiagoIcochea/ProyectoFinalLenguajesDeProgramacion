import tkinter as tk
from tkinter import ttk, messagebox
from Vistas.VistaEditarUsuario import VistaEditarUsuario

class VistaVerUsuarios:
    def __init__(self, root, controlador_usuarios):
        self.controlador = controlador_usuarios
        self.win = tk.Toplevel(root)
        self.win.title("Usuarios Registrados")
        self.win.geometry("800x400")

        self.tree = ttk.Treeview(self.win, columns=(
            "username", "nombre", "apellidoP", "apellidoM", "edad", "telefono", "correo", "direccion", "dni", "rol"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        columnas = ["Usuario", "Nombre", "Apellido P.", "Apellido M.", "Edad", "Teléfono", "Correo", "Dirección", "DNI", "Rol"]
        for i, col in enumerate(columnas):
            self.tree.heading(self.tree["columns"][i], text=col)
            self.tree.column(self.tree["columns"][i], width=80)

        self._cargar_usuarios()

        botones = tk.Frame(self.win)
        botones.pack(pady=10)

        btn_editar = tk.Button(botones, text="Editar", command=self.editar_usuario)
        btn_editar.grid(row=0, column=0, padx=10)

        btn_eliminar = tk.Button(botones, text="Eliminar", command=self.eliminar_usuario)
        btn_eliminar.grid(row=0, column=1, padx=10)

    def _cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for usuario in self.controlador.listar_usuarios():
            self.tree.insert("", tk.END, values=(
                usuario.get_username(), usuario.get_nombre(), usuario.get_apellidoP(),
                usuario.get_apellidoM(), usuario.get_edad(), usuario.get_telefono(),
                usuario.get_correo(), usuario.get_direccion(), usuario.get_dni(), usuario.get_rol()
            ))

    def editar_usuario(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Seleccionar", "Selecciona un usuario para editar.")
            return
        username = self.tree.item(item[0])["values"][0]
        VistaEditarUsuario(self.win, self.controlador, username_preseleccionado=username)
        self.win.wait_window()  
        self._cargar_usuarios()

    def eliminar_usuario(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Seleccionar", "Selecciona un usuario para eliminar.")
            return
        username = self.tree.item(item[0])["values"][0]
        confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar al usuario '{username}'?")
        if confirm:
            eliminado = self.controlador.eliminar_usuario(username)
            if eliminado:
                messagebox.showinfo("Éxito", f"Usuario '{username}' eliminado.")
                self._cargar_usuarios()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar al usuario '{username}'.")

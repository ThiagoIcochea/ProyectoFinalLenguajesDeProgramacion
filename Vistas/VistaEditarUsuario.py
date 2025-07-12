import tkinter as tk
from tkinter import ttk, messagebox
import re

class VistaEditarUsuario:
    def __init__(self, root, controlador, username_preseleccionado=None):
        self.controlador = controlador
        self.win = tk.Toplevel(root)
        self.win.title("Editar Usuario")
        self.win.geometry("400x650")

        tk.Label(self.win, text="Selecciona un usuario:").pack()
        self.combo_usuarios = ttk.Combobox(self.win, values=[u.get_username() for u in controlador.listar_usuarios()])
        self.combo_usuarios.pack(pady=5)
        self.combo_usuarios.bind("<<ComboboxSelected>>", self.cargar_datos_usuario)

        self.campos = {}
        etiquetas = [
            ("Nombre", "nombre"),
            ("Apellido Paterno", "apellidoP"),
            ("Apellido Materno", "apellidoM"),
            ("Edad", "edad"),
            ("Teléfono", "telefono"),
            ("Correo", "correo"),
            ("Dirección", "direccion"),
            ("DNI", "dni"),
            ("Rol", "rol")
        ]

        for texto, clave in etiquetas:
            tk.Label(self.win, text=texto + ":").pack()
            if clave == "edad":
                campo = tk.Spinbox(self.win, from_=18, to=120, width=5)
            elif clave == "rol":
                campo = ttk.Combobox(self.win, values=["admin", "responsable", "empleado"], state="readonly")
            else:
                campo = tk.Entry(self.win)
            campo.pack()
            self.campos[clave] = campo

        if username_preseleccionado:
            self.combo_usuarios.set(username_preseleccionado)
            self.cargar_datos_usuario(None)

        tk.Button(self.win, text="Guardar Cambios", command=self.actualizar_usuario).pack(pady=10)

    def cargar_datos_usuario(self, event):
        username = self.combo_usuarios.get()
        usuario = self.controlador.obtener_usuario(username)
        if usuario:
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

    def actualizar_usuario(self):
        username = self.combo_usuarios.get()
        if not username:
            messagebox.showerror("Error", "Selecciona un usuario.")
            return

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
            messagebox.showerror("Error", "No se pudo actualizar el usuario.")

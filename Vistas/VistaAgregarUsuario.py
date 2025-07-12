import tkinter as tk
from tkinter import ttk, messagebox
import re

class VistaAgregarUsuario:
    def __init__(self, root, controlador):
        self.win = tk.Toplevel(root)
        self.win.title("Agregar Usuario")
        self.win.geometry("400x600")
        self.controlador = controlador

        self.campos = {}

        campos_normales = [
            ("Username", "username"),
            ("Contraseña", "password"),
            ("Nombre", "nombre"),
            ("Apellido Paterno", "apellidoP"),
            ("Apellido Materno", "apellidoM"),
            ("Teléfono", "telefono"),
            ("Correo", "correo"),
            ("Dirección", "direccion"),
            ("DNI", "dni"),
        ]

        for label, key in campos_normales:
            tk.Label(self.win, text=label + ":").pack()
            entry = tk.Entry(self.win)
            entry.pack()
            self.campos[key] = entry

        tk.Label(self.win, text="Edad:").pack()
        spin = tk.Spinbox(self.win, from_=18, to=120, width=5)
        spin.pack()
        self.campos["edad"] = spin

        tk.Label(self.win, text="Rol:").pack()
        rol_combo = ttk.Combobox(self.win, values=["admin", "responsable", "empleado"], state="readonly")
        rol_combo.pack()
        rol_combo.current(0)
        self.campos["rol"] = rol_combo

        tk.Button(self.win, text="Registrar Usuario", command=self.registrar).pack(pady=10)

    def registrar(self):
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

        if self.controlador.verificar_dni(datos["dni"]):
            messagebox.showerror("Error", "El DNI ya está registrado.")
            return

        registrado = self.controlador.registrar_usuario(
            datos["username"], datos["password"], datos["nombre"],
            datos["apellidoP"], datos["apellidoM"], datos["edad"],
            datos["telefono"], datos["correo"], datos["direccion"],
            datos["dni"], datos["rol"]
        )

        if registrado:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.win.destroy()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya está en uso.")

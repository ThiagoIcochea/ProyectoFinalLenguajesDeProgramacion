import tkinter as tk
from tkinter import messagebox
from Utils.Seguridad import verificar_password
from Vistas.VistaMenu import VistaMenu
class VistaLogin:
    def __init__(self, master, controlador_usuario):
        self.master = master
        self.master.title("Login de Inventario")
        self.master.geometry("300x200")
        self.controlador = controlador_usuario

        tk.Label(master, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack()

        tk.Label(master, text="Contraseña:").pack(pady=5)
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        self.btn_login = tk.Button(master, text="Iniciar sesión", command=self.login)
        self.btn_login.pack(pady=10)

    def login(self):
        username = self.entry_usuario.get()
        password = self.entry_password.get()
        usuario = self.controlador.obtener_usuario(username)

        if usuario and verificar_password(password,usuario.get_password()) :
            messagebox.showinfo("Éxito", f"Bienvenido {usuario.get_nombre()} ({usuario.get_rol()})")
            self.master.destroy()  
            VistaMenu(usuario, self.controlador)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

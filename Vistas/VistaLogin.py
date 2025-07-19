import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesario para manejar imágenes
from Utils.Seguridad import verificar_password
from Vistas.VistaMenu import VistaMenu

class VistaLogin:
    def __init__(self, master, controlador_usuarios,controlador_producto, controlador_movimiento):
        self.master = master
        self.master.title("Login de Biblioteca")
        self.master.geometry("600x300")
        self.master.configure(bg="#f5f6fa")
        self.controladorU = controlador_usuarios
        self.controladorP = controlador_producto
        self.controladorM = controlador_movimiento

        # Frame principal dividido en dos secciones
        self.frame_left = tk.Frame(master, bg="#ffffff", width=300, height=300)
        self.frame_left.pack(side="left", fill="both", expand=False)

        self.frame_right = tk.Frame(master, bg="#ffffff", width=300, height=300)
        self.frame_right.pack(side="right", fill="both", expand=False)

        # Imagen en el lado izquierdo
        self.image = Image.open("Utils/assets/konecta-logo.jpg")  # Cambia la ruta a tu imagen
        self.image = self.image.resize((300, 300), Image.Resampling.LANCZOS)  # Ajusta el tamaño de la imagen
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label_image = tk.Label(self.frame_left, image=self.image_tk, bg="#ffffff")
        self.label_image.pack(fill="both", expand=True)

        # Formulario de login en el lado derecho
        self.form_frame = tk.Frame(self.frame_right, bg="#ffffff")  # Sub-frame para centrar el contenido
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=220)

        tk.Label(self.form_frame, text="Iniciar Sesión", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#273c75").pack(pady=(10, 15))

        tk.Label(self.form_frame, text="Usuario:", font=("Segoe UI", 10), bg="#ffffff").pack(anchor="w", padx=20)
        self.entry_usuario = tk.Entry(self.form_frame, font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_usuario.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(self.form_frame, text="Contraseña:", font=("Segoe UI", 10), bg="#ffffff").pack(anchor="w", padx=20)
        self.entry_password = tk.Entry(self.form_frame, show="*", font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_password.pack(fill="x", padx=20, pady=(0, 15))

        self.btn_login = tk.Button(self.form_frame, text="Iniciar sesión", font=("Segoe UI", 10, "bold"),
                                   bg="#273c75", fg="#ffffff", activebackground="#40739e", activeforeground="#ffffff",
                                   bd=0, cursor="hand2", command=self.login)
        self.btn_login.pack(pady=5, ipadx=10, ipady=3)

    def login(self):
        username = self.entry_usuario.get()
        password = self.entry_password.get()
        usuario = self.controladorU.obtener_usuario(username)

        if usuario and verificar_password(password, usuario.get_password()):
            messagebox.showinfo("Éxito", f"Bienvenido {usuario.get_nombre()} ({usuario.get_rol()})")
            self.master.destroy()
            VistaMenu(usuario, self.controladorU,self.controladorP, self.controladorM)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
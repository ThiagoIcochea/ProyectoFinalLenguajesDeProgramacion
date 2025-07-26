# Importación de la biblioteca gráfica Tkinter
import tkinter as tk
from tkinter import messagebox  # Para mostrar cuadros de diálogo emergentes

# Librerías para manejo de imágenes
from PIL import Image, ImageTk  # Usadas para cargar y redimensionar imágenes en Tkinter

# Función de seguridad para verificar contraseñas encriptadas
from Utils.Seguridad import verificar_password

# Vista del menú principal que se muestra tras un login exitoso
from Vistas.VistaMenu import VistaMenu

# Clase que representa la ventana de inicio de sesión (login)
class VistaLogin:
    def __init__(self, master, controlador_usuarios, controlador_producto, controlador_movimiento, controlador_solicitudes):
        self.master = master
        self.master.title("Login de Biblioteca")  # Título de la ventana
        self.master.geometry("600x300")  # Tamaño fijo de la ventana
        self.master.configure(bg="#f5f6fa")  # Color de fondo

        # Controladores que maneja esta vista (usuarios, productos, etc.)
        self.controladorU = controlador_usuarios
        self.controladorP = controlador_producto
        self.controladorM = controlador_movimiento
        self.controladorS = controlador_solicitudes

        # =======================
        # INTERFAZ GRÁFICA
        # =======================

        # Sección izquierda (contiene la imagen/logo)
        self.frame_left = tk.Frame(master, bg="#ffffff", width=300, height=300)
        self.frame_left.pack(side="left", fill="both", expand=False)

        # Sección derecha (formulario de login)
        self.frame_right = tk.Frame(master, bg="#ffffff", width=300, height=300)
        self.frame_right.pack(side="right", fill="both", expand=False)

        # Carga y muestra de la imagen/logo en el lado izquierdo
        self.image = Image.open('Utils/assets/konecta-logo.jpg')  # Ruta a la imagen
        self.image = self.image.resize((300, 300), Image.Resampling.LANCZOS)  # Redimensiona la imagen
        self.image_tk = ImageTk.PhotoImage(self.image)  # Convierte imagen a formato Tkinter
        self.label_image = tk.Label(self.frame_left, image=self.image_tk, bg="#ffffff")
        self.label_image.pack(fill="both", expand=True)

        # Submarco centrado para el formulario de login
        self.form_frame = tk.Frame(self.frame_right, bg="#ffffff")
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=220)

        # Título del formulario
        tk.Label(self.form_frame, text="Iniciar Sesión", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#273c75").pack(pady=(10, 15))

        # Etiqueta y campo de entrada para el nombre de usuario
        tk.Label(self.form_frame, text="Usuario:", font=("Segoe UI", 10), bg="#ffffff").pack(anchor="w", padx=20)
        self.entry_usuario = tk.Entry(self.form_frame, font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_usuario.pack(fill="x", padx=20, pady=(0, 10))

        # Etiqueta y campo de entrada para la contraseña (oculta)
        tk.Label(self.form_frame, text="Contraseña:", font=("Segoe UI", 10), bg="#ffffff").pack(anchor="w", padx=20)
        self.entry_password = tk.Entry(self.form_frame, show="*", font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_password.pack(fill="x", padx=20, pady=(0, 15))

        # Botón para iniciar sesión
        self.btn_login = tk.Button(
            self.form_frame, text="Iniciar sesión", font=("Segoe UI", 10, "bold"),
            bg="#273c75", fg="#ffffff", activebackground="#40739e", activeforeground="#ffffff",
            bd=0, cursor="hand2", command=self.login  # Al hacer clic llama al método login()
        )
        self.btn_login.pack(pady=5, ipadx=10, ipady=3)

    # =======================
    # FUNCIÓN DE AUTENTICACIÓN
    # =======================
    def login(self):
        # Obtiene los valores ingresados en los campos de texto
        username = self.entry_usuario.get()
        password = self.entry_password.get()

        # Intenta obtener el objeto usuario desde el controlador
        usuario = self.controladorU.obtener_usuario(username)

        # Verifica si el usuario existe y si la contraseña es correcta
        if usuario and verificar_password(password, usuario.get_password()):
            # Si es correcto, muestra mensaje de bienvenida y abre el menú principal
            messagebox.showinfo("Éxito", f"Bienvenido {usuario.get_nombre()} ({usuario.get_rol()})")
            self.master.destroy()  # Cierra la ventana de login
            VistaMenu(usuario, self.controladorU, self.controladorP, self.controladorM, self.controladorS)  # Abre el menú
        else:
            # Si falla, muestra mensaje de error
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Importación de la biblioteca gráfica Tkinter para crear interfaces de usuario
import tkinter as tk

# Importación de los controladores responsables de la lógica del sistema
from Controladoras.ControladorUsuario import ControladorUsuario
from Controladoras.ControladorProducto import ControladorProducto
from Controladoras.ControladorMovimiento import ControladorMovimiento
from Controladoras.ControladorSolicitud import ControladorSolicitud

# Importación de la vista de inicio de sesión (interfaz de login)
from Vistas.VistaLogin import VistaLogin

# Función principal que inicializa todo el sistema
def main():
    # Instancia del controlador de usuarios
    controlador_usuarios = ControladorUsuario()
    
    # Instancia del controlador de productos
    controlador_producto = ControladorProducto()
    
    # Instancia del controlador de movimientos (ingresos y salidas de stock)
    controlador_movimiento = ControladorMovimiento()
    
    # Instancia del controlador de solicitudes de productos
    controlador_solicitudes = ControladorSolicitud()

    # Registro manual de usuarios de prueba para facilitar el ingreso al sistema
    controlador_usuarios.registrar_usuario("admin", "admin123", "Super", "Admin", "Root", 35, "999999999", "admin@empresa.com", "Av. Principal 123", "12345678", "admin")
    controlador_usuarios.registrar_usuario("juan", "clave456", "Juan", "Pérez", "Gómez", 30, "987654321", "juan@empresa.com", "Calle Falsa 456", "87654321", "responsable")
    controlador_usuarios.registrar_usuario("ana", "pass789", "Ana", "Torres", "Rojas", 25, "912345678", "ana@empresa.com", "Pasaje 123", "11223344", "empleado")

    # Se crea la ventana principal del sistema (interfaz gráfica raíz)
    root = tk.Tk()

    # Se lanza la vista de inicio de sesión, pasando todos los controladores al frontend
    login_app = VistaLogin(root, controlador_usuarios, controlador_producto, controlador_movimiento, controlador_solicitudes)

    # Se inicia el bucle principal de la interfaz gráfica (espera de eventos)
    root.mainloop()

# Verifica si este archivo está siendo ejecutado directamente (no importado) y llama a main()
if __name__ == "__main__":
    main()

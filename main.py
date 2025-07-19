import tkinter as tk
from Controladoras.ControladorUsuario import ControladorUsuario
from Controladoras.ControladorProducto import ControladorProducto
from Controladoras.ControladorMovimiento import ControladorMovimiento
from Controladoras.ControladorSolicitud import ControladorSolicitud
from Vistas.VistaLogin import VistaLogin

def main():
    
    controlador_usuarios = ControladorUsuario()
    controlador_producto = ControladorProducto()
    controlador_movimiento = ControladorMovimiento()
    controlador_solicitudes = ControladorSolicitud()
   

  
    controlador_usuarios.registrar_usuario("admin", "admin123", "Super", "Admin", "Root", 35, "999999999", "admin@empresa.com", "Av. Principal 123", "12345678", "admin")
    controlador_usuarios.registrar_usuario("juan", "clave456", "Juan", "Pérez", "Gómez", 30, "987654321", "juan@empresa.com", "Calle Falsa 456", "87654321", "responsable")
    controlador_usuarios.registrar_usuario("ana", "pass789", "Ana", "Torres", "Rojas", 25, "912345678", "ana@empresa.com", "Pasaje 123", "11223344", "empleado")

    
    root = tk.Tk()
    login_app = VistaLogin(root, controlador_usuarios,controlador_producto,controlador_movimiento, controlador_solicitudes)
    root.mainloop()

if __name__ == "__main__":
    main()

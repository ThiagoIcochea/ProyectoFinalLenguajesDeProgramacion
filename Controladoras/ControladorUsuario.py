from Entidades.Usuario import Usuario
from Utils.Seguridad import hash_password


class ControladorUsuario:
    def __init__(self):
        self.usuarios = {}  

    def registrar_usuario(self, username,password, nombre,apellidoP,apellidoM,edad,telefono,correo,direccion,dni, rol):
        if username in self.usuarios:
            print("Usuario ya registrado.")
            return False
        for u in self.usuarios.values():
         if u.get_dni() == dni:
            print("Ya existe un usuario con ese DNI.")
            return False
        
        hshpassword = hash_password(password)
        nuevo = Usuario(username,hshpassword, nombre,apellidoP,apellidoM,edad,telefono,correo,direccion,dni, rol)
        self.usuarios[username] = nuevo
        return True
    def actualizar_usuario(self, username, nombre, apellidoP, apellidoM, edad, telefono, correo, direccion, dni, rol):
     usuario = self.usuarios.get(username)
     if usuario:
        usuario.set_nombre(nombre)
        usuario.set_apellidoP(apellidoP)
        usuario.set_apellidoM(apellidoM)
        usuario.set_edad(edad)
        usuario.set_telefono(telefono)
        usuario.set_correo(correo)
        usuario.set_direccion(direccion)
        usuario.set_dni(dni)
        usuario.set_rol(rol)
        return True
     return False

    def obtener_usuario(self, username):
        return self.usuarios.get(username)

    def listar_usuarios(self):
        return list(self.usuarios.values())
    
    def verificar_dni(self, dni):
     return any(u.get_dni() == dni for u in self.usuarios.values())

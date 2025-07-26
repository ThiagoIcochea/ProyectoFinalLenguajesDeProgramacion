# Importamos la clase Usuario desde el módulo de Entidades
from Entidades.Usuario import Usuario
# Importamos la función de utilidad para hashear contraseñas
from Utils.Seguridad import hash_password


# ControladorUsuario es responsable de gestionar el registro y administración de usuarios
class ControladorUsuario:
    
    def __init__(self):
        # Diccionario que almacena los usuarios registrados con la clave: username
        self.usuarios = {}

    # Método para registrar un nuevo usuario
    def registrar_usuario(self, username, password, nombre, apellidoP, apellidoM, edad, telefono, correo, direccion, dni, rol):
        # Verificamos si ya existe un usuario con ese username
        if username in self.usuarios:
            print("Usuario ya registrado.")
            return False

        # Verificamos si ya existe un usuario con ese mismo DNI
        for u in self.usuarios.values():
            if u.get_dni() == dni:
                print("Ya existe un usuario con ese DNI.")
                return False

        # Hasheamos la contraseña antes de almacenarla por seguridad
        hshpassword = hash_password(password)

        # Creamos una nueva instancia de Usuario
        nuevo = Usuario(username, hshpassword, nombre, apellidoP, apellidoM, edad, telefono, correo, direccion, dni, rol)

        # Lo agregamos al diccionario de usuarios
        self.usuarios[username] = nuevo
        return True

    # Método para actualizar los datos de un usuario existente
    def actualizar_usuario(self, username, nombre, apellidoP, apellidoM, edad, telefono, correo, direccion, dni, rol):
        usuario = self.usuarios.get(username)  # Obtenemos el usuario por su username

        if usuario:
            # Actualizamos los campos con los nuevos valores
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

    # Devuelve un usuario dado su username
    def obtener_usuario(self, username):
        return self.usuarios.get(username)

    # Devuelve la lista de todos los usuarios registrados
    def listar_usuarios(self):
        return list(self.usuarios.values())
    
    # Verifica si un DNI ya está registrado (útil para validación al registrar)
    def verificar_dni(self, dni):
        return any(u.get_dni() == dni for u in self.usuarios.values())

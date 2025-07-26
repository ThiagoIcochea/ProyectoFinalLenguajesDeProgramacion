# Definición de la clase Usuario
class Usuario:
    
    # Método constructor que inicializa los atributos privados del usuario
    def __init__(self, username, password, nombre, apellidoP, apellidoM, edad, telefono, correo, direccion, dni, rol):
        self.__username = username        # Nombre de usuario
        self.__password = password        # Contraseña
        self.__nombre = nombre            # Primer nombre
        self.__apellidoP = apellidoP      # Apellido paterno
        self.__apellidoM = apellidoM      # Apellido materno
        self.__edad = edad                # Edad del usuario
        self.__telefono = telefono        # Número de teléfono
        self.__correo = correo            # Correo electrónico
        self.__direccion = direccion      # Dirección física
        self.__dni = dni                  # Documento Nacional de Identidad (DNI)
        self.__rol = rol                  # Rol del usuario (admin, empleado, etc.)

    # Métodos getter y setter para acceder/modificar los atributos privados

    # Username
    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    # Nombre
    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    # Apellido paterno
    def get_apellidoP(self):
        return self.__apellidoP

    def set_apellidoP(self, apellidoP):
        self.__apellidoP = apellidoP

    # Apellido materno
    def get_apellidoM(self):
        return self.__apellidoM

    def set_apellidoM(self, apellidoM):
        self.__apellidoM = apellidoM

    # Edad
    def get_edad(self):
        return self.__edad

    def set_edad(self, edad):
        self.__edad = edad

    # Teléfono
    def get_telefono(self):
        return self.__telefono

    def set_telefono(self, telefono):
        self.__telefono = telefono

    # Correo
    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        self.__correo = correo

    # Dirección
    def get_direccion(self):
        return self.__direccion

    def set_direccion(self, direccion):
        self.__direccion = direccion

    # DNI
    def get_dni(self):
        return self.__dni

    def set_dni(self, dni):
        self.__dni = dni

    # Rol
    def get_rol(self):
        return self.__rol

    def set_rol(self, rol):
        self.__rol = rol

    # Contraseña
    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

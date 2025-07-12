class Usuario:
    def __init__(self, username,password, nombre,apellidoP,apellidoM,edad,telefono,correo,direccion,dni, rol):
        self.__username = username
        self.__nombre = nombre
        self.__apellidoP = apellidoP
        self.__apellidoM = apellidoM
        self.__edad = edad
        self.__telefono = telefono
        self.__correo = correo 
        self.__direccion = direccion
        self.__dni = dni
        self.__rol = rol
        self.__password= password

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre
    
    def get_apellidoP(self):
        return self.__apellidoP

    def set_apellidoP(self, apellidoP):
        self.__apellidoP = apellidoP
    
    def get_apellidoM(self):
        return self.__apellidoM

    def set_apellidoM(self, apellidoM):
        self.__apellidoM = apellidoM

    def get_edad(self):
        return self.__edad

    def set_edad(self, edad):
        self.__edad = edad
    
    def get_telefono(self):
        return self.__telefono

    def set_telefono(self, telefono):
        self.__telefono = telefono
    
    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        self.__correo = correo
    def get_direccion(self):
        return self.__direccion

    def set_direccion(self, direccion):
        self.__direccion = direccion
    def get_dni(self):
        return self.__dni

    def set_dni(self, dni):
        self.__dni = dni
    def get_rol(self):
        return self.__rol

    def set_rol(self, rol):
        self.__rol = rol
    def get_password(self):
        return self.__password
    def set_password(self,password):
        self.__password = password

class Movimiento:
    def __init__(self, fecha, producto_codigo, tipo, cantidad, usuario, motivo=""):
        self.__fecha = fecha
        self.__producto_codigo = producto_codigo
        self.__tipo = tipo  
        self.__cantidad = cantidad
        self.__usuario = usuario 
        self.__motivo = motivo

    def get_fecha(self):
        return self.__fecha

    def set_fecha(self, fecha):
        self.__fecha = fecha

    def get_producto_codigo(self):
        return self.__producto_codigo

    def set_producto_codigo(self, codigo):
        self.__producto_codigo = codigo

    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, tipo):
        self.__tipo = tipo

    def get_cantidad(self):
        return self.__cantidad

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    def get_usuario(self):
        return self.__usuario

    def set_usuario(self, usuario):
        self.__usuario = usuario

    def get_motivo(self):
        return self.__motivo

    def set_motivo(self, motivo):
        self.__motivo = motivo

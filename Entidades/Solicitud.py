class Solicitud:
    def __init__(self, id, empleado, producto, cantidad, estado, fecha):
        self.__empleado = empleado     
        self.__producto = producto     
        self.__cantidad = cantidad
        self.__estado = estado          
        self.__fecha = fecha
        self.__id = id

    def get_id(self):
        return self.__id
    def set_id(self, id):
        self.__id = id

    def get_empleado(self):
        return self.__empleado

    def set_empleado(self, empleado):
        self.__empleado = empleado

    def get_producto(self):
        return self.__producto

    def set_producto(self, producto):
        self.__producto = producto

    def get_cantidad(self):
        return self.__cantidad

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    def get_estado(self):
        return self.__estado

    def set_estado(self, estado):
        self.__estado = estado

    def get_fecha(self):
        return self.__fecha

    def set_fecha(self, fecha):
        self.__fecha = fecha

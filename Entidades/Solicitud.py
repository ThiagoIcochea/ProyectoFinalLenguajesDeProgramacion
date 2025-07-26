# Definición de la clase Solicitud
class Solicitud:
    
    # Constructor que inicializa los atributos privados de la solicitud
    def __init__(self, id, empleado, producto, cantidad, estado, fecha):
        self.__empleado = empleado     # ID o referencia al empleado que realiza la solicitud
        self.__producto = producto     # ID o referencia al producto solicitado
        self.__cantidad = cantidad     # Cantidad del producto solicitado
        self.__estado = estado         # Estado actual de la solicitud (ej: Pendiente, Aprobado)
        self.__fecha = fecha           # Fecha en que se realizó la solicitud
        self.__id = id                 # ID único de la solicitud

    # Métodos getter y setter para acceder/modificar cada atributo

    # ID de la solicitud
    def get_id(self):
        return self.__id
    
    def set_id(self, id):
        self.__id = id

    # Empleado que realizó la solicitud
    def get_empleado(self):
        return self.__empleado

    def set_empleado(self, empleado):
        self.__empleado = empleado

    # Producto solicitado
    def get_producto(self):
        return self.__producto

    def set_producto(self, producto):
        self.__producto = producto

    # Cantidad solicitada
    def get_cantidad(self):
        return self.__cantidad

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    # Estado de la solicitud (Pendiente, Aprobado, Rechazado, etc.)
    def get_estado(self):
        return self.__estado

    def set_estado(self, estado):
        self.__estado = estado

    # Fecha de solicitud
    def get_fecha(self):
        return self.__fecha

    def set_fecha(self, fecha):
        self.__fecha = fecha

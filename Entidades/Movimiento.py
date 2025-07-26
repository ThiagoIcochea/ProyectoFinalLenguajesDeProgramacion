# Clase que representa un movimiento en el inventario (entrada o salida de productos)
class Movimiento:
    
    # Constructor que inicializa los atributos del movimiento
    def __init__(self, fecha, producto_codigo, tipo, cantidad, usuario, motivo=""):
        self.__fecha = fecha                     # Fecha del movimiento
        self.__producto_codigo = producto_codigo # Código del producto involucrado
        self.__tipo = tipo                       # Tipo de movimiento: "Entrada" o "Salida"
        self.__cantidad = cantidad               # Cantidad de productos movidos
        self.__usuario = usuario                 # Usuario responsable del movimiento
        self.__motivo = motivo                   # Motivo del movimiento (opcional)

    # Métodos getter y setter para cada atributo
    # Permiten acceder y modificar de forma controlada los datos del movimiento

    # Fecha del movimiento
    def get_fecha(self):
        return self.__fecha

    def set_fecha(self, fecha):
        self.__fecha = fecha

    # Código del producto afectado por el movimiento
    def get_producto_codigo(self):
        return self.__producto_codigo

    def set_producto_codigo(self, codigo):
        self.__producto_codigo = codigo

    # Tipo de movimiento (Entrada o Salida)
    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, tipo):
        self.__tipo = tipo

    # Cantidad de unidades que entran o salen del inventario
    def get_cantidad(self):
        return self.__cantidad

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    # Usuario que realiza o registra el movimiento
    def get_usuario(self):
        return self.__usuario

    def set_usuario(self, usuario):
        self.__usuario = usuario

    # Motivo asociado al movimiento (puede ser justificación, observación, etc.)
    def get_motivo(self):
        return self.__motivo

    def set_motivo(self, motivo):
        self.__motivo = motivo

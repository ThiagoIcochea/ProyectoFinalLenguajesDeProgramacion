class Producto:
    def __init__(self, codigo, nombre, descripcion, fechaActualizacion,proveedor, categoria, stock=0):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__categoria = categoria
        self.__stock = stock
        self.__fechaActualizacion = fechaActualizacion
        self.__proveedor = proveedor

    def get_codigo(self):
        return self.__codigo

    def set_codigo(self, codigo):
        self.__codigo = codigo

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_fechaActualizacion(self):
        return self.__fechaActualizacion

    def set_fechaActualizacion(self, fechaActualizacion):
        self.__fechaActualizacion = fechaActualizacion

    def get_proveedor(self):
        return self.__proveedor

    def set_proveedor(self, proveedor):
        self.__proveedor = proveedor
    def get_descripcion(self):
        return self.__descripcion

    def set_descripcion(self, descripcion):
        self.__descripcion = descripcion

    def get_categoria(self):
        return self.__categoria

    def set_categoria(self, categoria):
        self.__categoria = categoria

    def get_stock(self):
        return self.__stock

    def set_stock(self, stock):
        self.__stock = stock

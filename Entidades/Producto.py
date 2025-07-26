# Definición de la clase Producto
class Producto:
    
    # Constructor que inicializa los atributos del producto
    def __init__(self, codigo, nombre, descripcion, fechaActualizacion, proveedor, categoria, stock=0):
        self.__codigo = codigo                     # Código único del producto
        self.__nombre = nombre                     # Nombre del producto
        self.__descripcion = descripcion           # Descripción del producto
        self.__categoria = categoria               # Categoría del producto (ej. Electrónica, Ropa)
        self.__stock = stock                       # Cantidad en stock del producto (por defecto 0)
        self.__fechaActualizacion = fechaActualizacion   # Fecha de la última actualización del producto
        self.__proveedor = proveedor               # Proveedor del producto

    # Métodos getter y setter para cada atributo
    # Permiten obtener o modificar los valores de manera controlada

    # Código del producto
    def get_codigo(self):
        return self.__codigo

    def set_codigo(self, codigo):
        self.__codigo = codigo

    # Nombre del producto
    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    # Fecha de la última actualización
    def get_fechaActualizacion(self):
        return self.__fechaActualizacion

    def set_fechaActualizacion(self, fechaActualizacion):
        self.__fechaActualizacion = fechaActualizacion

    # Proveedor del producto
    def get_proveedor(self):
        return self.__proveedor

    def set_proveedor(self, proveedor):
        self.__proveedor = proveedor

    # Descripción del producto
    def get_descripcion(self):
        return self.__descripcion

    def set_descripcion(self, descripcion):
        self.__descripcion = descripcion

    # Categoría del producto
    def get_categoria(self):
        return self.__categoria

    def set_categoria(self, categoria):
        self.__categoria = categoria

    # Stock actual del producto
    def get_stock(self):
        return self.__stock

    def set_stock(self, stock):
        self.__stock = stock

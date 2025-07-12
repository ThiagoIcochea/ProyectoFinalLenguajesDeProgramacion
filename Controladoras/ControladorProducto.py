from Entidades.Producto import Producto
from datetime import datetime

class ControladorProducto:
    def __init__(self):
        self.productos = {}  

    def agregar_producto(self, codigo, nombre, descripcion, proveedor, categoria, stock):
        if codigo in self.productos:
            return False  

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuevo = Producto(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            fechaActualizacion=fecha_actual,
            proveedor=proveedor,
            categoria=categoria,
            stock=stock
        )
        self.productos[codigo] = nuevo
        return True

    def actualizar_stock(self, codigo, nuevo_stock):
        if codigo not in self.productos:
            return False

        producto = self.productos[codigo]
        producto.set_stock(nuevo_stock)
        producto.set_fechaActualizacion(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return True

    def listar_productos(self):
        return list(self.productos.values())

    def obtener_producto(self, codigo):
        return self.productos.get(codigo)

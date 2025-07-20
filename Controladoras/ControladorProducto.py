from Entidades.Producto import Producto
from datetime import datetime
import openpyxl
from openpyxl import Workbook

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
    
    def agregar_productoF(self, codigo, nombre, descripcion, proveedor, categoria, stock,fechaActualizacion):
        if codigo in self.productos:
            return False  

       
        nuevo = Producto(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            proveedor=proveedor,
            categoria=categoria,
            stock=stock,
            fechaActualizacion=fechaActualizacion
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
    
    def importar_desde_excel(self, ruta_archivo):
     try:
        wb = openpyxl.load_workbook(ruta_archivo)
        hoja = wb.active

        for fila in hoja.iter_rows(min_row=2, values_only=True):
            if fila is None:
                print("Fila vacía, se omitió.")
                continue

           
            fila_limpia = fila[:7]

           
            if len(fila_limpia) != 7 or any(campo is None for campo in fila_limpia):
                print("Fila incompleta o con campos vacíos, se omitió:", fila)
                continue

            tmpc, nombre, descripcion, proveedor, categoria, stock, fecha_actualizacion = fila_limpia

           
            if str(tmpc) not in self.productos:
                self.agregar_productoF(
                    str(tmpc),
                    nombre,
                    descripcion,
                    proveedor,
                    categoria,
                    int(stock),
                    fecha_actualizacion
                )
            else:
                print(f"Producto con código {tmpc} ya existe. Se omitió.")

        return True

     except Exception as e:
        print("Error al cargar productos desde Excel:", e)
        return False



    def exportar_a_excel(self, ruta_archivo):
        try:
            wb = Workbook()
            hoja = wb.active
            hoja.title = "Productos"

            hoja.append(["Código", "Nombre", "Descripción", "Proveedor", "Categoría", "Stock", "Fecha Actualización"])

            for producto in self.productos.values():
                hoja.append([
                    producto.get_codigo(),
                    producto.get_nombre(),
                    producto.get_descripcion(),
                    producto.get_proveedor(),
                    producto.get_categoria(),
                    producto.get_stock(),
                    producto.get_fechaActualizacion()
                ])

            wb.save(ruta_archivo)
            return True
        except Exception as e:
            print("Error al exportar productos a Excel:", e)
            return False

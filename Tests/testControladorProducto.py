# Importa módulos del sistema para trabajar con rutas y pruebas
import sys
import os
import unittest

# Agrega al path el directorio padre para poder importar módulos desde carpetas superiores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el controlador de productos a probar
from Controladoras.ControladorProducto import ControladorProducto

# Define una clase de pruebas para ControladorProducto, usando unittest
class TestControladorProducto(unittest.TestCase):

    def setUp(self):
        """
        Este método se ejecuta antes de cada prueba.
        Inicializa una instancia del controlador de productos.
        """
        self.controlador = ControladorProducto()

    def test_agregar_producto_valido(self):
        """
        Prueba si se puede agregar correctamente un producto válido.
        - Debe retornar True
        - El ID del producto debe quedar registrado
        """
        resultado = self.controlador.agregar_productoF(
            "P001", "Laptop", "Alta gama", "Dell", "Electrónica", 10, "2025-07-20"
        )
        self.assertTrue(resultado)  # Verifica que se haya agregado correctamente
        self.assertIn("P001", self.controlador.productos)  # Verifica que el ID esté en el diccionario

    def test_agregar_producto_duplicado(self):
        """
        Prueba que no se permita registrar un producto con un ID ya existente.
        El segundo intento debe devolver False.
        """
        self.controlador.agregar_productoF(
            "P001", "Laptop", "Alta gama", "Dell", "Electrónica", 10, "2025-07-20"
        )
        resultado = self.controlador.agregar_productoF(
            "P001", "Laptop", "Alta gama", "Dell", "Electrónica", 10, "2025-07-20"
        )
        self.assertFalse(resultado)  # No se debe permitir duplicados

    def test_agregar_producto_invalido_stock(self):
        """
        Prueba que no se permita agregar un producto con un stock inválido (no numérico).
        El método debe devolver False.
        """
        resultado = self.controlador.agregar_productoF(
            "P002", "Mouse", "Gaming", "Logitech", "Periféricos", "veinte", "2025-07-20"
        )
        self.assertFalse(resultado)  # "veinte" no es un número, debe fallar

    def test_agregar_producto_con_none(self):
        """
        Prueba que no se permita registrar un producto si algún campo importante es None.
        En este caso, el ID del producto es None.
        """
        resultado = self.controlador.agregar_productoF(
            None, "Teclado", "Mecánico", "Razer", "Periféricos", 15, "2025-07-20"
        )
        self.assertFalse(resultado)  # No se debe aceptar un ID None

# Si se ejecuta este archivo directamente, se correrán todas las pruebas
if __name__ == '__main__':
    unittest.main()

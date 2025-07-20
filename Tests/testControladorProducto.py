import sys
import os
import unittest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Controladoras.ControladorProducto import ControladorProducto
from Entidades.Producto import Producto

class TestControladorProducto(unittest.TestCase):

    def setUp(self):
        self.controlador = ControladorProducto()

    def test_agregar_producto_valido(self):
        resultado = self.controlador.agregar_productoF(
            "P001", "Laptop", "Alta gama", "Dell", "Electrónica", 10, "2025-07-20"
        )
        self.assertTrue(resultado)
        self.assertIn("P001", self.controlador.productos)

    def test_agregar_producto_duplicado(self):
        self.controlador.agregar_productoF(
            "P001", "Laptop", "Alta gama", "Dell", "Electrónica", 10, "2025-07-20"
        )
        resultado = self.controlador.agregar_productoF(
            "P001", "Laptop", "Alta gama", "Dell", "Electrónica", 10, "2025-07-20"
        )
        self.assertFalse(resultado)

    def test_agregar_producto_invalido_stock(self):
        resultado = self.controlador.agregar_productoF(
            "P002", "Mouse", "Gaming", "Logitech", "Periféricos", "veinte", "2025-07-20"
        )
        self.assertFalse(resultado)

    def test_agregar_producto_con_none(self):
        resultado = self.controlador.agregar_productoF(
            None, "Teclado", "Mecánico", "Razer", "Periféricos", 15, "2025-07-20"
        )
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()

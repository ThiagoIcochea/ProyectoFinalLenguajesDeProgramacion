import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Controladoras.ControladorMovimiento import ControladorMovimiento
from Entidades.Movimiento import Movimiento

class TestControladorMovimiento(unittest.TestCase):

    def setUp(self):
        self.controlador = ControladorMovimiento()

    def test_registrar_movimiento_valido(self):
        resultado = self.controlador.registrar_movimiento(
            "M001", "U001", "Entrada", 10, "2025-07-20"
        )
        self.assertTrue(resultado)
        self.assertIn("M001", self.controlador.movimientos)

    def test_registrar_movimiento_duplicado(self):
        self.controlador.registrar_movimiento("M001", "U001", "Entrada", 10, "2025-07-20")
        resultado = self.controlador.registrar_movimiento("M001", "U001", "Entrada", 10, "2025-07-20")
        self.assertFalse(resultado)

    def test_registrar_movimiento_invalido(self):
        resultado = self.controlador.registrar_movimiento(
            "", None, "Salida", "abc", "fecha"
        )
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()

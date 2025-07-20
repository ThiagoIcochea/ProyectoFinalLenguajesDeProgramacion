import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Controladoras.ControladorSolicitud import ControladorSolicitud
from Entidades.Solicitud import Solicitud

class TestControladorSolicitud(unittest.TestCase):

    def setUp(self):
        self.controlador = ControladorSolicitud()

    def test_crear_solicitud_valida(self):
        resultado = self.controlador.crear_solicitud(
            "S001", "U001", "P001", "2025-07-20", "Pendiente"
        )
        self.assertTrue(resultado)
        self.assertIn("S001", self.controlador.solicitudes)

    def test_crear_solicitud_duplicada(self):
        self.controlador.crear_solicitud("S001", "U001", "P001", "2025-07-20", "Pendiente")
        resultado = self.controlador.crear_solicitud("S001", "U001", "P001", "2025-07-20", "Pendiente")
        self.assertFalse(resultado)

    def test_crear_solicitud_invalida(self):
        resultado = self.controlador.crear_solicitud(
            None, "", "", "", None
        )
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()

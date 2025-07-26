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
        resultado = self.controlador.registrar_solicitudP(
            "S001", "U001", "P001",2,"Pendiente", "2025-07-20"
        )
        self.assertTrue(resultado)
        ids = [s.get_id() for s in self.controlador.solicitudes]
        self.assertIn("S001", ids)

    def test_crear_solicitud_duplicada(self):
        self.controlador.registrar_solicitudP("S001", "U001", "P001",2,"Pendiente", "2025-07-20")
        resultado = self.controlador.registrar_solicitudP("S001", "U001", "P001",2,"Pendiente", "2025-07-20")
        self.assertFalse(resultado)

    def test_crear_solicitud_invalida(self):
        resultado = self.controlador.registrar_solicitudP(
            None, "", "", "", None
        )
       
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Controladoras.ControladorUsuario import ControladorUsuario
from Entidades.Usuario import Usuario

class TestControladorUsuario(unittest.TestCase):

    def setUp(self):
        self.controlador = ControladorUsuario()

    def test_agregar_usuario_valido(self):
        resultado = self.controlador.agregar_usuario(
            "U001", "Thiago", "thiago@example.com", "admin"
        )
        self.assertTrue(resultado)
        self.assertIn("U001", self.controlador.usuarios)

    def test_agregar_usuario_duplicado(self):
        self.controlador.agregar_usuario("U001", "Thiago", "thiago@example.com", "admin")
        resultado = self.controlador.agregar_usuario("U001", "Thiago", "thiago@example.com", "admin")
        self.assertFalse(resultado)

    def test_agregar_usuario_invalido(self):
        resultado = self.controlador.agregar_usuario(
            None, "", "invalido.com", ""
        )
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()

# Importa módulos del sistema para manejar rutas de archivos y pruebas unitarias
import sys
import os
import unittest

# Agrega al path del sistema el directorio padre del archivo actual, para poder importar módulos de allí
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el controlador de usuarios desde el módulo correspondiente
from Controladoras.ControladorUsuario import ControladorUsuario
# Importa la clase Usuario, si se necesita para test más avanzados (aunque aquí no se usa directamente)
from Entidades.Usuario import Usuario

# Define una clase de prueba que hereda de unittest.TestCase
class TestControladorUsuario(unittest.TestCase):

    def setUp(self):
        """
        Este método se ejecuta antes de cada prueba individual.
        Inicializa una instancia del controlador de usuarios para usarla en los tests.
        """
        self.controlador = ControladorUsuario()

    def test_agregar_usuario_valido(self):
        """
        Verifica que se pueda registrar un usuario válido.
        Comprueba que la función devuelva True y que el usuario esté almacenado correctamente.
        """
        resultado = self.controlador.registrar_usuario(
            "U001", "pass123", "Thiago", "Icochea", "Rodriguez",
            19, 968085026, "thiago@example.com", "Jiron Puno 845", 79952523, "admin"
        )
        self.assertTrue(resultado)  # El registro debería ser exitoso
        self.assertIn("U001", self.controlador.usuarios)  # El ID debe estar en el diccionario de usuarios

    def test_agregar_usuario_duplicado(self):
        """
        Verifica que no se permita registrar dos veces un mismo usuario con el mismo ID.
        El segundo intento debe fallar (False).
        """
        # Primer registro (válido)
        self.controlador.registrar_usuario(
            "U001", "pass123", "Thiago", "Icochea", "Rodriguez",
            19, 968085026, "thiago@example.com", "Jiron Puno 845", 79952523, "admin"
        )
        # Segundo registro con mismo ID (debería fallar)
        resultado = self.controlador.registrar_usuario(
            "U001", "pass123", "Thiago", "Icochea", "Rodriguez",
            19, 968085026, "thiago@example.com", "Jiron Puno 845", 79952523, "admin"
        )
        self.assertFalse(resultado)  # El segundo intento no debe permitir duplicados

    def test_agregar_usuario_invalido(self):
        """
        Verifica que no se pueda registrar un usuario con datos inválidos o incompletos.
        """
        resultado = self.controlador.registrar_usuario(
            None, "", "invalido.com", ""  # Datos incompletos o incorrectos
        )
        self.assertFalse(resultado)  # El resultado debe ser False porque los datos no son válidos

# Punto de entrada del script. Si se ejecuta directamente, corre las pruebas.
if __name__ == '__main__':
    unittest.main()

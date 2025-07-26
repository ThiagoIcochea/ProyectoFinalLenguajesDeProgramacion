# Importación de librerías del sistema necesarias para manipular rutas y realizar pruebas
import sys
import os
import unittest

# Agrega el directorio padre al path para poder importar módulos desde niveles superiores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa la clase del controlador de movimientos
from Controladoras.ControladorMovimiento import ControladorMovimiento

# Importa la clase de entidad Movimiento (por si se utiliza en pruebas)
from Entidades.Movimiento import Movimiento

# Clase de prueba unitaria para el controlador de movimientos
class TestControladorMovimiento(unittest.TestCase):

    def setUp(self):
        """
        Este método se ejecuta automáticamente antes de cada test.
        Aquí se crea una nueva instancia del controlador para cada prueba.
        """
        self.controlador = ControladorMovimiento()

    def test_registrar_movimiento_valido(self):
        """
        Prueba si se puede registrar correctamente un movimiento válido.
        Se espera que:
        - El método devuelva True
        - El ID del movimiento quede registrado en el controlador
        """
        resultado = self.controlador.registrar_movimiento(
            "M001", "U001", "Entrada", 10, "2025-07-20"
        )
        self.assertTrue(resultado)  # Verifica que se haya registrado correctamente
        self.assertIn("M001", self.controlador.movimientos)  # Verifica que el ID esté en el diccionario

    def test_registrar_movimiento_duplicado(self):
        """
        Prueba que no se pueda registrar un movimiento con un ID ya existente.
        El segundo intento debe devolver False.
        """
        # Primer registro válido
        self.controlador.registrar_movimiento("M001", "U001", "Entrada", 10, "2025-07-20")
        # Segundo intento con el mismo ID
        resultado = self.controlador.registrar_movimiento("M001", "U001", "Entrada", 10, "2025-07-20")
        self.assertFalse(resultado)  # Debe fallar por duplicado

    def test_registrar_movimiento_invalido(self):
        """
        Prueba que no se registre un movimiento con datos inválidos:
        - ID vacío
        - Usuario None
        - Cantidad no numérica ("abc")
        - Fecha en formato incorrecto ("fecha")
        """
        resultado = self.controlador.registrar_movimiento(
            "", None, "Salida", "abc", "fecha"
        )
        self.assertFalse(resultado)  # Debe devolver False por datos inválidos

# Ejecuta las pruebas si se corre este archivo directamente
if __name__ == '__main__':
    unittest.main()

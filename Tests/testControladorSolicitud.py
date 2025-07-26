# Importa módulos del sistema necesarios para trabajar con rutas y pruebas unitarias
import sys
import os
import unittest

# Añade al path el directorio padre, permitiendo importar módulos desde la carpeta superior
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el controlador de solicitudes que se va a probar
from Controladoras.ControladorSolicitud import ControladorSolicitud
# Importa la entidad Solicitud, que puede usarse en las pruebas si se desea
from Entidades.Solicitud import Solicitud

# Clase de prueba unitaria que hereda de unittest.TestCase
class TestControladorSolicitud(unittest.TestCase):

    def setUp(self):
        """
        Este método se ejecuta antes de cada prueba.
        Inicializa una instancia del controlador de solicitudes.
        """
        self.controlador = ControladorSolicitud()

    def test_crear_solicitud_valida(self):
        """
        Prueba que se pueda crear correctamente una solicitud válida.
        Debe devolver True y el ID debe estar en la lista de solicitudes.
        """
        resultado = self.controlador.registrar_solicitudP(
            "S001", "U001", "P001", 2, "Pendiente", "2025-07-20"
        )
        self.assertTrue(resultado)  # La solicitud debería registrarse correctamente
        ids = [s.get_id() for s in self.controlador.solicitudes]  # Obtiene todos los IDs registrados
        self.assertIn("S001", ids)  # Verifica que el ID S001 esté presente

    def test_crear_solicitud_duplicada(self):
        """
        Prueba que el sistema rechace solicitudes duplicadas con el mismo ID.
        El segundo intento de registro debe devolver False.
        """
        # Primer registro (válido)
        self.controlador.registrar_solicitudP("S001", "U001", "P001", 2, "Pendiente", "2025-07-20")
        # Segundo registro con el mismo ID (debe fallar)
        resultado = self.controlador.registrar_solicitudP("S001", "U001", "P001", 2, "Pendiente", "2025-07-20")
        self.assertFalse(resultado)

    def test_crear_solicitud_invalida(self):
        """
        Prueba que el sistema no permita registrar solicitudes con datos incompletos o inválidos.
        """
        resultado = self.controlador.registrar_solicitudP(
            None, "", "", "", None  # Datos incompletos
        )
        self.assertFalse(resultado)  # El registro debe fallar

# Si se ejecuta directamente este archivo, se correrán todas las pruebas definidas
if __name__ == '__main__':
    unittest.main()

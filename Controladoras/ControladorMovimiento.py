# Importa la clase Movimiento desde el módulo Entidades
from Entidades.Movimiento import Movimiento

# Define la clase ControladorMovimiento, que gestiona una lista de movimientos
class ControladorMovimiento:
    def __init__(self):
        # Lista donde se almacenan todos los objetos Movimiento
        self.movimientos = []

    # Método para registrar un nuevo movimiento
    def registrar_movimiento(self, fecha, producto_codigo, tipo, cantidad, usuario, motivo=""):
        # Crea una nueva instancia de Movimiento con los datos recibidos
        mov = Movimiento(fecha, producto_codigo, tipo, cantidad, usuario, motivo)
        # Agrega el movimiento a la lista de movimientos
        self.movimientos.append(mov)

    # Devuelve la lista completa de movimientos registrados
    def listar_movimientos(self):
        return self.movimientos

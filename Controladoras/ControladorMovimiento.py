from Entidades.Movimiento import Movimiento


class ControladorMovimiento:
    def __init__(self):
        self.movimientos = []  

    def registrar_movimiento(self, fecha, producto_codigo, tipo, cantidad, usuario, motivo=""):
        mov = Movimiento(fecha, producto_codigo, tipo, cantidad, usuario, motivo)
        self.movimientos.append(mov)

    def listar_movimientos(self):
        return self.movimientos

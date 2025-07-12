from Entidades.Solicitud import Solicitud
from datetime import datetime

class ControladorSolicitud:
    def __init__(self):
        self.solicitudes = []

    def registrar_solicitud(self, empleado, producto, cantidad, estado, fecha):
        solicitud = Solicitud(empleado, producto, cantidad, estado, fecha)
        self.solicitudes.append(solicitud)

    def listar_solicitudes(self):
        return self.solicitudes

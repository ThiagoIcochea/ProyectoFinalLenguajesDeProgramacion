from Entidades.Solicitud import Solicitud
from datetime import datetime

class ControladorSolicitud:
    def __init__(self):
        self.solicitudes = []

    def generar_id_unico(self, lista_existente):
        """
        Genera un ID único tipo 'SOL001', 'SOL002', ..., basado en una lista de objetos Solicitud.
        """
        numero = 1
        ids_existentes = [s.get_id() for s in lista_existente]
        nuevo_id = f"SOL{numero:03d}"
        while nuevo_id in ids_existentes:
            numero += 1
            nuevo_id = f"SOL{numero:03d}"
        return nuevo_id

    def registrar_solicitudP(self,id, empleado, producto, cantidad, estado, fecha=None):
     if fecha is None:
        fecha = datetime.now()

    
     campos = [id,empleado, producto, cantidad, estado]
     if any(campo is None or str(campo).strip() == "" for campo in campos):
        return False

  
     try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            return False
     except ValueError:
        return False

   
     for s in self.solicitudes:
        if (s.get_id() == id and                                                                                                                                               
            s.get_empleado() == empleado and 
            s.get_producto() == producto and 
            s.get_fecha() == fecha):
            return False

    
    
     solicitud = Solicitud(id, empleado, producto, cantidad, estado, fecha)
     self.solicitudes.append(solicitud)
     return True

    def registrar_solicitud(self, empleado, producto, cantidad, estado, fecha=None):
     if fecha is None:
        fecha = datetime.now()

    
     campos = [empleado, producto, cantidad, estado]
     if any(campo is None or str(campo).strip() == "" for campo in campos):
        return False

  
     try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            return False
     except ValueError:
        return False

   
     for s in self.solicitudes:
        if (s.get_empleado() == empleado and 
            s.get_producto() == producto and 
            s.get_fecha().date() == fecha.date()):
            return False

    
     nuevo_id = self.generar_id_unico(self.solicitudes)
     solicitud = Solicitud(nuevo_id, empleado, producto, cantidad, estado, fecha)
     self.solicitudes.append(solicitud)
     return True


    def listar_solicitudes(self):
        return self.solicitudes

    def eliminar_solicitud(self, id_solicitud):
        self.solicitudes = [s for s in self.solicitudes if s.get_id() != id_solicitud]

    def buscar_por_empleado(self, nombre_empleado):
        return [s for s in self.solicitudes if nombre_empleado.lower() in s.get_empleado().lower()]

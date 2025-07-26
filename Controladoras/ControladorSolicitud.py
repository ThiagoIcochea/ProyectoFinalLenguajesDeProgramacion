# Importamos la clase Solicitud desde el módulo de entidades
from Entidades.Solicitud import Solicitud
# Importamos datetime para manejar fechas
from datetime import datetime

# Clase que maneja el control y la lógica relacionada con las solicitudes
class ControladorSolicitud:
    def __init__(self):
        # Lista donde se almacenan todas las solicitudes creadas
        self.solicitudes = []

    def generar_id_unico(self, lista_existente):
        """
        Genera un ID único del tipo 'SOL001', 'SOL002', etc., en base a los IDs ya existentes.
        """
        numero = 1
        # Extraemos todos los IDs ya existentes
        ids_existentes = [s.get_id() for s in lista_existente]
        # Creamos un nuevo ID con formato SOL###
        nuevo_id = f"SOL{numero:03d}"
        # Mientras el nuevo ID ya exista, seguimos incrementando el número
        while nuevo_id in ids_existentes:
            numero += 1
            nuevo_id = f"SOL{numero:03d}"
        return nuevo_id

    # Método para registrar una solicitud con ID manual
    def registrar_solicitudP(self, id, empleado, producto, cantidad, estado, fecha=None):
        # Si no se proporciona fecha, usamos la fecha actual
        if fecha is None:
            fecha = datetime.now()

        # Verificamos que los campos obligatorios no estén vacíos
        campos = [id, empleado, producto, cantidad, estado]
        if any(campo is None or str(campo).strip() == "" for campo in campos):
            return False

        # Validamos que la cantidad sea un número entero positivo
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                return False
        except ValueError:
            return False

        # Evita solicitudes duplicadas con mismo ID, empleado, producto y fecha
        for s in self.solicitudes:
            if (s.get_id() == id and
                s.get_empleado() == empleado and 
                s.get_producto() == producto and 
                s.get_fecha() == fecha):
                return False

        # Si todo es válido, creamos y agregamos la solicitud
        solicitud = Solicitud(id, empleado, producto, cantidad, estado, fecha)
        self.solicitudes.append(solicitud)
        return True

    # Método para registrar una solicitud sin necesidad de pasar el ID manualmente
    def registrar_solicitud(self, empleado, producto, cantidad, estado, fecha=None):
        if fecha is None:
            fecha = datetime.now()

        # Validamos que los campos requeridos no estén vacíos
        campos = [empleado, producto, cantidad, estado]
        if any(campo is None or str(campo).strip() == "" for campo in campos):
            return False

        # Validamos la cantidad como número positivo
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                return False
        except ValueError:
            return False

        # Verificamos si ya existe una solicitud similar para el mismo día
        for s in self.solicitudes:
            if (s.get_empleado() == empleado and 
                s.get_producto() == producto and 
                s.get_fecha().date() == fecha.date()):
                return False

        # Generamos automáticamente un ID único
        nuevo_id = self.generar_id_unico(self.solicitudes)
        # Creamos y registramos la nueva solicitud
        solicitud = Solicitud(nuevo_id, empleado, producto, cantidad, estado, fecha)
        self.solicitudes.append(solicitud)
        return True

    # Devuelve todas las solicitudes registradas
    def listar_solicitudes(self):
        return self.solicitudes

    # Elimina una solicitud según su ID
    def eliminar_solicitud(self, id_solicitud):
        # Filtramos la lista dejando solo las solicitudes con ID distinto al que se desea eliminar
        self.solicitudes = [s for s in self.solicitudes if s.get_id() != id_solicitud]

    # Busca solicitudes que contengan cierto nombre de empleado
    def buscar_por_empleado(self, nombre_empleado):
        # Devuelve todas las solicitudes que contengan el nombre del empleado (no sensible a mayúsculas)
        return [s for s in self.solicitudes if nombre_empleado.lower() in s.get_empleado().lower()]

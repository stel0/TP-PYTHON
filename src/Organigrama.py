from Database import Database
from Persona import Persona
from Dependencia import Dependencia

class Organigrama:
    id = None
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha

    def get_dict(self):
        dict = {
            "nombre": self.nombre,
            "fecha": self.fecha
        }

        return dict
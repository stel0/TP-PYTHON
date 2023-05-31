class Dependencia:
    id = None
    def __init__(self, nombre, manager_id):
        self.nombre = nombre
        self.manager_id = manager_id

    def cambioId(self, id):
        self.id = id
    
    def getDict(self):
        return {
            "nombre": self.nombre,
            "manager_id": self.manager_id
        }
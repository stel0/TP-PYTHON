class Persona:
    subordinados = []
    id = None
    def __init__(self, ci, apellido, nombre, telefono, direccion, dependencia, id_organigrama ,salario):
        self.ci = ci
        self.apellido = apellido
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.dependencia = dependencia
        self.id_organigrama = id_organigrama
        self.salario = salario

    def cambioId(self, id):
        self.id = id

    def getDict(self):
        return {
            "ci": self.ci,
            "apellido": self.apellido,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "id_dependencia": self.dependencia,
            "id_organigrama":self.id_organigrama,
            "salario": self.salario
        }
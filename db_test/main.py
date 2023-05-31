from Persona import Persona
from Dependencia import Dependencia
from Database import Database

dep_ceo = Dependencia("CEO", 1)
dep_ceo0 = Dependencia("Cesars",2)
dep_ceo1 = Dependencia("CEP",3)
jefe = Persona("6038491", "Riveros", "Marcelo", "0991916160", "Avda Nanawa C/ Los Pinos", 0, 5000000)

db = Database("base.db")
db.connect()

# db.insertarData("Persona", jefe.getDict())
# db.insertarData("Dependencia",dep_ceo0.getDict())
# db.insertarData("Dependencia",dep_ceo1.getDict())
# db.insertarData("Dependencia",dep_ceo.getDict())

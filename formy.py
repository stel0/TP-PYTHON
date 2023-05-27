import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from db_test import Database,Dependencia 

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        #Add a title
        self.setWindowTitle("Hello World!")
        

        nodo_form = qtw.QFormLayout()
        #formulario dependencia
        self.setLayout(nodo_form)

        #Add stuff/widgets para dependencia
        label_1 = qtw.QLabel("Creacion de una dependencia")
        label_1.setFont(qtg.QFont("Helvetica",24))

        dependencia_nombre = qtw.QLineEdit(self)
        manager_id = qtw.QLineEdit(self)
        manager_id.setValidator(qtg.QIntValidator())

        #add rows to the app para dependencia
        nodo_form.addRow(label_1)
        nodo_form.addRow("Nombre de la dependencia:",dependencia_nombre)
        nodo_form.addRow("Ingrese el id del manager",manager_id)
        nodo_form.addRow(qtw.QPushButton("Enviar",clicked=lambda:enviar_dependencia()))

        #Show the app
        self.show()

        def enviar_dependencia():
            db = Database.Database("base.db")
            db.connect()
            dependencia = Dependencia.Dependencia(dependencia_nombre.text(),manager_id.text())
            db.insertarData("Dependencia",dependencia.getDict())
            db.disconnect()
            manager_id.setText("")
            dependencia_nombre.setText("")

app = qtw.QApplication([])
mw = MainWindow()

#Run the app
app.exec_()
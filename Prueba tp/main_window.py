from PyQt5.QtWidgets import QApplication,QFileDialog, QMainWindow, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from Database import Database
from Organigrama import Organigrama
from Dependencia import Dependencia
from Persona import Persona

DATABASE = "base.db"
database = Database(DATABASE)
organigrama_activo = 1

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mi Aplicación")

        # Cargar el archivo .ui
        loadUi("main_window_1.ui", self)
        database.connect()
        rows = database.buscarData("Organigrama", f"id = {organigrama_activo}", ["nombre"])
        if len(rows) != 0:
            self.label_organigrama.setText(f"Organigrama: {rows[0][0]}")
        else:
            self.label_organigrama.setText("No ha seleccionado un organigrama")
        # Conectar señales y slots si es necesario
        self.crear_dependencia.clicked.connect(self.buttonClicked)
        self.crear_organigrama.clicked.connect(self.create_organigrama)
        self.abrir_organigrama.clicked.connect(self.open_organigrama)
        self.Add_Persona.clicked.connect(self.abrir_form_persona)
    def buttonClicked(self):
        # ...
        self.form_window = FormDependencia()  # Create an instance of FormDependencia
        self.form_window.show()  # Show the form window
    def create_organigrama(self):
        self.form_organigrama = FormOrganigrama()
        self.form_organigrama.show()
    def open_organigrama(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Abrir Organigrama", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
        if filename:
            print("Ruta del archivo seleccionado:", filename)

    def abrir_form_persona(self):
        self.form_persona = FormPersona()
        self.form_persona.show()
class FormOrganigrama(QWidget):
    enviar_organigrama = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FormOrganigrama, self).__init__(parent)
        self.setWindowTitle("Formulario Organigrama")

        loadUi("form_organigrama.ui", self)

        self.enviar_button.clicked.connect(self.enviar_organigrama)

    def enviar_organigrama(self):
        # TODO: validar que el campo fecha sea una fecha valida
        titulo = self.titulo_lineEdit.text()
        fecha = self.fecha_lineEdit.text()
        org = Organigrama(titulo, fecha)
        database.connect()
        database.insertarData("Organigrama", org.get_dict())
        self.close()
        database.disconnect()

class FormDependencia(QWidget):
    def __init__(self):
        super(FormDependencia, self).__init__()
        self.setWindowTitle("Formulario dependencia")

        loadUi("form_window.ui", self)

        self.enviar_dependencia.clicked.connect(self.e_dependencia)

    def e_dependencia(self):
        # TODO: validar que el lider ingresado exista
        nombre_dep = self.input_dependencia_nombre.text()
        nombre_lider = self.input_dependencia_nombre_lider.text()
        apellido_lider = self.input_dependencia_apellido_lider.text()
        
        database.connect()
        rows = database.buscarData("Persona", f"nombre = '{nombre_lider}' AND apellido = '{apellido_lider}'", ["id"])
        id_lider = rows[0][0]
        
        dependencia = Dependencia(nombre_dep, id_lider, organigrama_activo)
        database.insertarData("Dependencia", dependencia.getDict())

        database.disconnect()
        self.close()  # Cerrar la ventana de formulario

class FormPersona(QWidget):
    def __init__(self):
        super(FormPersona, self).__init__()
        self.setWindowTitle("Formulario Persona")

        loadUi("form_persona.ui", self)
        self.boton_enviar.clicked.connect(self.e_persona)

    def e_persona(self):
        self.close()
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

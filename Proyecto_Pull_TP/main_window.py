from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mi Aplicación")

        # Cargar el archivo .ui
        loadUi("main_window_1.ui", self)

        # Conectar señales y slots si es necesario
        self.crear_dependencia.clicked.connect(self.buttonClicked)
        self.crear_organigrama.clicked.connect(self.create_organigrama)
        self.abrir_organigrama.clicked.connect(self.open_organigrama)
        self.Add_Persona.clicked.connect(self.abrir_form_persona)

    def buttonClicked(self):
        self.form_window = FormDependencia()
        self.form_window.show()

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
        self.close()

class FormDependencia(QWidget):
    def __init__(self):
        super(FormDependencia, self).__init__()
        self.setWindowTitle("Formulario dependencia")

        loadUi("form_window.ui", self)

        self.enviar_dependencia.clicked.connect(self.e_dependencia)

    def e_dependencia(self):
        self.close()

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

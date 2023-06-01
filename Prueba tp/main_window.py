from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
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
    def buttonClicked(self):
        # ...
        self.form_window = FormDependencia()  # Create an instance of FormDependencia
        self.form_window.show()  # Show the form window
    def create_organigrama(self):
        self.form_organigrama = FormOrganigrama(self)
        self.form_organigrama.enviar_organigrama.connect(self.update_organigrama)
        self.form_organigrama.show()
    def update_organigrama(self, titulo):
        self.organigrama_label.setText(titulo)

class FormOrganigrama(QWidget):
    enviar_organigrama = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FormOrganigrama, self).__init__(parent)
        self.setWindowTitle("Formulario Organigrama")

        loadUi("form_organigrama.ui", self)

        self.enviar_button.clicked.connect(self.enviar_organigrama)

    def enviar_organigrama(self):
        titulo = self.titulo_lineEdit.text()
        self.enviar_organigrama.emit(titulo)
        self.close()

class FormDependencia(QWidget):
    def __init__(self):
        super(FormDependencia, self).__init__()
        self.setWindowTitle("Formulario dependencia")

        loadUi("form_window.ui", self)

        self.enviar_dependencia.clicked.connect(self.e_dependencia)

    def e_dependencia(self):
        # self.main_window = MainWindow()  # Create an instance of MainWindow
        # self.main_window.show()  # Show the main window
        self.close()  # Cerrar la ventana de formulario
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

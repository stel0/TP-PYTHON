# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
# from PyQt5.uic import loadUi

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setWindowTitle("Mi Aplicación")

#         # Cargar el archivo .ui
#         loadUi("main_window_1.ui", self)

#         # Agregar contenido adicional o conectar señales aquí

#         # Ejemplo: Conectar una señal al hacer clic en un botón
#         self.crear_dependencia.clicked.connect(self.button_clicked)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mi Aplicación")

        # Cargar el archivo .ui
        loadUi("main_window_1.ui", self)

        # Conectar señales y slots si es necesario
        self.crear_dependencia.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        # Función para manejar el evento de clic en el botón
        form_window = FormDependencia()  # Create an instance of FormDependencia
        form_window.show()  # Show the form window

class FormDependencia(QWidget):
    def __init__(self):
        super(FormDependencia, self).__init__()
        self.setWindowTitle("Formulario dependencia")

        loadUi("form_window.ui", self)

        self.enviar_dependencia.clicked.connect(self.e_dependencia)

    def e_dependencia(self):
        main_window = MainWindow()  # Create an instance of MainWindow
        main_window.show()  # Show the main window

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

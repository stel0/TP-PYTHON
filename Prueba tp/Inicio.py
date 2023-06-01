from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from main_window import MainWindow as mw
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mi Aplicación")
        self.setFixedSize(600, 600)  # Establecer tamaño fijo de 600x600 píxeles

        # Cargar el archivo .ui
        loadUi("inicio.ui", self)

        # Conectar señales y slots si es necesario
        self.Informes.clicked.connect(self.open_file_dialog)
        self.Salir.clicked.connect(self.salir)
        self.Ver_main_window.clicked.connect(self.ver)
    def open_file_dialog(self):
        # Abrir el diálogo de selección de archivos
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.exec_()

    def salir(self):
        QApplication.quit()

    def ver(self):
        # Cargar y mostrar la nueva ventana
        self.new_window = mw()
        self.new_window.show()
        mw.buttonClicked
        mw.create_organigrama
        mw.open_organigrama
        mw.abrir_form_persona

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

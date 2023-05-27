import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QLabel, QVBoxLayout, QPushButton

# Definir el formulario
class Formulario(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario")
        layout = QVBoxLayout()
        label = QLabel("¡Hola desde el formulario!")
        layout.addWidget(label)
        self.setLayout(layout)

# Definir la ventana principal
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú y formulario")
        self.setGeometry(200, 200, 300, 200)

        # Crear un menú
        menu = self.menuBar()
        archivo_menu = menu.addMenu("Archivo")

        # Crear una acción para abrir el formulario
        abrir_formulario_accion = QAction("Abrir formulario", self)
        abrir_formulario_accion.triggered.connect(self.abrir_formulario)
        archivo_menu.addAction(abrir_formulario_accion)

        # Crear un botón para abrir el formulario
        boton_formulario = QPushButton("Abrir formulario", self)
        boton_formulario.setGeometry(100, 100, 100, 30)
        boton_formulario.clicked.connect(self.abrir_formulario)

    def abrir_formulario(self):
        formulario = Formulario()
        formulario.exec_()

# Crear la aplicación
app = QApplication(sys.argv)

# Crear la ventana principal
ventana_principal = VentanaPrincipal()
ventana_principal.show()

# Ejecutar la aplicación
sys.exit(app.exec_())

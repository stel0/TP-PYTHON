from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

class GaleriaImagenes(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Configuración de la ventana principal
        self.setWindowTitle('Galería de Imágenes')
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Área de desplazamiento para contener las imágenes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Desactivar desplazamiento horizontal
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Habilitar desplazamiento vertical

        # Widget que contiene todas las imágenes
        image_widget = QWidget()
        image_layout = QVBoxLayout()  # Cambio en el tipo de layout

        # Agregar imágenes a la galería
        image_paths = ['clash.jpg', 'pepito.jpg']  # Rutas de las imágenes
        for path in image_paths:
            image_label = QLabel()
            pixmap = QPixmap(path)
            pixmap = pixmap.scaledToWidth(500)  # Escalar la imagen al ancho deseado
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_layout.addWidget(image_label)

        image_widget.setLayout(image_layout)
        scroll_area.setWidget(image_widget)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_galeria = GaleriaImagenes()
    ventana_galeria.show()
    sys.exit(app.exec_())

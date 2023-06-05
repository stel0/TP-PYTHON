import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear una escena y un QGraphicsView
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # Cargar la imagen
        image_path = "./dependency_graph.png.png"
        pixmap = QPixmap(image_path)

        # Agregar la imagen a la escena
        self.scene.addPixmap(pixmap)

        # Ajustar la vista al tamaño de la imagen
        self.view.fitInView(self.scene.sceneRect(), aspectRatioMode=Qt.KeepAspectRatio)

        # Establecer el QGraphicsView como widget central
        self.setCentralWidget(self.view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

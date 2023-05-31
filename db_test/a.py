import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter

class OrganigramaItem(QGraphicsRectItem):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setRect(0, 0, 100, 50)
        self.setBrush(QBrush(QColor(200, 200, 200)))
        self.setPen(QColor(0, 0, 0))

        self.text = QGraphicsTextItem(name, self)
        self.text.setDefaultTextColor(QColor(0, 0, 0))
        self.text.setFont(QFont("Arial", 10))
        self.text.setPos(5, 5)

class OrganigramaView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.setScene(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.scale(1, 1)
        self.setSceneRect(scene.sceneRect())

def main():
    app = QApplication(sys.argv)

    # Conexi贸n a la base de datos
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()

    # Obtenci贸n de los datos de la base de datos
    cursor.execute("SELECT id, nombre, manager_id FROM Dependencia")
    data = cursor.fetchall()

    conn.close()

    # Creaci贸n de la escena y vista
    scene = QGraphicsScene()
    view = OrganigramaView(scene)

    # Diccionario para almacenar los objetos OrganigramaItem
    items = {}

    # Creaci贸n de los elementos del organigrama
    for row in data:
        emp_id, nombre, jefe_id = row
        item = OrganigramaItem(nombre)
        items[emp_id] = item
        if jefe_id is not None:
            jefe_item = items[jefe_id]
            jefe_rect = jefe_item.rect()
            item_rect = item.rect()
            item.setPos(jefe_item.x() + (jefe_rect.width() - item_rect.width()) / 2, jefe_item.y() + jefe_rect.height() + 50)
        scene.addItem(item)

    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
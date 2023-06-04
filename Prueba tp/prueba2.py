import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from graphviz import Digraph
from Database import Database

DATABASE = "base1.db"
db = Database(DATABASE)
db.connect()
organigrama_activo = 1

def generate_graph():
    dot = Digraph()
    return dot

def generate_node(graph, nombre_dependencia):
    graph.node(nombre_dependencia, nombre_dependencia)

def connect_nodes(graph, node1_label, node2_label, edge_label):
    graph.edge(node1_label, node2_label, edge_label)

def generar_nodos(graph, id_dependencia):
    res_jefe = db.buscarData("Persona", f"id_dependencia = {id_dependencia}", ["id", "apellido", "nombre"])
    if len(res_jefe) != 0:
        id_jefe = res_jefe[0][0]
        apellido_jefe = res_jefe[0][1]
        nombre_jefe = res_jefe[0][2]
        if id_dependencia != 0:
            res_dep = db.buscarData("Dependencia", f"id = {id_dependencia}", ["nombre"])
            nombre_dep = res_dep[0][0]
        else:
            nombre_dep = "CEO"

        rows = db.buscarData("Dependencia", f"manager_id = {id_jefe}", ["id", "nombre"])
        if len(rows) > 0:
            for res in rows:
                generate_node(graph, f"Titulo: {res[1]}\nApellido: {apellido_jefe}\nNombre: {nombre_jefe}")
                connect_nodes(graph, nombre_dep, res[1], "")
                generar_nodos(graph, res[0])
        

class GraphWindow(QMainWindow):

    def __init__(self, graph, nombre_archivo):
        super().__init__()
        self.setWindowTitle('Graph Visualization')
        self.graph = graph
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.update_graph(nombre_archivo)

    def update_graph(self, nombre_archivo):
        image_path = f'grafos/{nombre_archivo}'  # Cambio de extensión a .png
        self.graph.format = 'png'  # Cambio de formato a png
        self.graph.render(filename=image_path, cleanup=True)
        image = QImage(image_path)
        pixmap = QPixmap.fromImage(image)
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)  # Ajuste de la vista
        self.resize(pixmap.width(), pixmap.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    graph = generate_graph()
    
    generar_nodos(graph, 0)
    
    
    window = GraphWindow(graph, 'graph')
    window.show()
    db.disconnect()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from graphviz import Digraph

def generate_graph():
    dot = Digraph()
    return dot

def generate_node(graph, nombre_dependencia):
    graph.node(nombre_dependencia, nombre_dependencia)

def connect_nodes(graph, node1_label, node2_label, edge_label):
    graph.edge(node1_label, node2_label, edge_label)

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
    generate_node(graph, 'Node 1')
    generate_node(graph, 'Node 2')
    connect_nodes(graph, 'Node 1', 'Node 2', 'Edge')
    
    window = GraphWindow(graph, 'graph')
    window.show()
    
    sys.exit(app.exec_())

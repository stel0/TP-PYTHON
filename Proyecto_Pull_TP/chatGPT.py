import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from graphviz import Digraph

def generate_graph():
    dot = Digraph()
    return dot

def generate_node(graph, nombre_dependencia):
    graph.node(nombre_dependencia, nombre_dependencia)

def generate_root(graph, root_label):
    graph.node('root', root_label)

def connect_root_to_node(graph, node_label, edge_label):
    graph.edge('root', node_label, edge_label)

def connect_nodes(graph, node1_label, node2_label, edge_label):
    graph.edge(node1_label, node2_label, edge_label)

class GraphWindow(QMainWindow):

    def __init__(self, graph, nombre_archivo):
        super().__init__()
        self.setWindowTitle('Graph Visualization')
        self.graph = graph
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self.update_graph(nombre_archivo)

    def update_graph(self, nombre_archivo):
        image_path = f'grafos\{nombre_archivo}'
        self.graph.format = 'svg'
        self.graph.render(filename=image_path, cleanup=True)
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

# prueba
# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     graph = generate_graph()

#     # Generador de nodos
#     generate_node(graph, 'Node A')
#     generate_node(graph, 'Node B')
#     generate_node(graph, 'Node C')

#     # Generador de raíces
#     generate_root(graph, 'Root Node')

#     # Conectar raíz a nodo
#     connect_root_to_node(graph, 'Node A', 'Root Edge')

#     # Conectar nodo a nodo
#     connect_nodes(graph, 'Node A', 'Node B', 'Edge A to B')
#     connect_nodes(graph, 'Node A', 'Node C', 'Edge A to C')

#     window = GraphWindow(graph,"grafico")
#     window.show()

#     sys.exit(app.exec_())

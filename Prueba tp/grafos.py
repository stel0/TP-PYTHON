import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from graphviz import Digraph
from Database import Database

DATABASE = "base1.db"
db = Database(DATABASE)
db.connect()
def generate_graph():
    dot = Digraph()
    return dot

def generate_node(graph, nombre_dependencia, label):
    graph.node(nombre_dependencia, label)

def connect_nodes(graph, node1_label, node2_label, edge_label):
    graph.edge(node1_label, node2_label, edge_label)

def generar_grafo(graph, id_dependencia, id_organigrama):
    res_jefe = db.buscarData("Persona", f"id_dependencia = {id_dependencia} AND id_organigrama = {id_organigrama}", ["id", "apellido", "nombre"])
    
    if len(res_jefe) != 0:
        
        if id_dependencia != 0:
            res_dep = db.buscarData("Dependencia", f"id = {id_dependencia} AND id_organigrama = {id_organigrama}", ["nombre"])
            nombre_dep = res_dep[0][0]
        else:
            nombre_dep = "CEO"

        for jefe in res_jefe:
            id = jefe[0]
            apellido = jefe[1]
            nombre = jefe[2]
            dependencias = db.buscarData("Dependencia", f"manager_id = {id} AND id_organigrama = {id_organigrama}", ["id", "nombre"])
            
            if len(dependencias) > 0:    
                for dependencia in dependencias:
                    generate_node(graph, dependencia[1], f"Titulo: {dependencia[1]}\nApellido: {apellido}\nNombre: {nombre}")
                    connect_nodes(graph, nombre_dep, dependencia[1], "")
                    generar_grafo(graph, dependencia[0], id_organigrama)
            else:
                generate_node(graph, f"{nombre} {apellido}", f"Apellido: {apellido}\nNombre: {nombre}")
                connect_nodes(graph, nombre_dep, f"{nombre} {apellido}", "")


#class GraphWindow(QMainWindow):
#
#    def __init__(self, graph, nombre_archivo):
#        super().__init__()
#        self.setWindowTitle('Graph Visualization')
#        self.graph = graph
#        self.scene = QGraphicsScene()
#        self.view = QGraphicsView(self.scene)
#        self.setCentralWidget(self.view)
#        self.update_graph(nombre_archivo)
#
#    def update_graph(self, nombre_archivo):
#        image_path = f'grafos/{nombre_archivo}'  # Cambio de extensión a .png
#        self.graph.format = 'png'  # Cambio de formato a png
#        self.graph.render(filename=image_path, cleanup=True)
#        image = QImage(image_path)
#        pixmap = QPixmap.fromImage(image)
#        self.scene.clear()
#        self.scene.addPixmap(pixmap)
#        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)  # Ajuste de la vista
#        self.resize(pixmap.width(), pixmap.height())
#
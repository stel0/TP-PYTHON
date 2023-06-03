from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsRectItem, QApplication,QFileDialog, QMainWindow, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from Database import Database
from Organigrama import Organigrama
from Dependencia import Dependencia
from Persona import Persona
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter
import prueba2 as qgs
from graphviz import Digraph
DATABASE = "base.db"
database = Database(DATABASE)
organigrama_activo = 1
from PyQt5.QtWidgets import QGraphicsView

class MyGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyGraphicsView, self).__init__(parent)
        self.qgv_scene = QGraphicsScene()
        self.setScene(self.qgv_scene)

    def add_rect_slot(self, titulo, fecha):
        rect = QGraphicsRectItem()
        rect.setRect(0, 0, 200, 100)
        rect.setPos(50, 50)
        rect.setFlag(QGraphicsRectItem.ItemIsMovable)

        rect.setBrush(Qt.white)

        text = QGraphicsTextItem(rect)
        text.setDefaultTextColor(Qt.black)
        text.setPlainText(f"Título: {titulo}\nFecha: {fecha}")
        text.setPos(rect.rect().topLeft() + QPointF(10, 10))

        self.qgv_scene.addItem(rect)
        self.qgv_scene.addItem(text)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mi Aplicación")
        self.qgv = MyGraphicsView()

        # Cargar el archivo .ui
        loadUi("main_window_1.ui", self)
        database.connect()
        rows = database.buscarData("Organigrama", f"id = {organigrama_activo}", ["nombre"])
        if len(rows) != 0:
            self.label_organigrama.setText(f"Organigrama: {rows[0][0]}")
        else:
            self.label_organigrama.setText("No ha seleccionado un organigrama")
        # Conectar señales y slots si es necesario
        self.crear_dependencia.clicked.connect(self.buttonClicked)
        self.crear_organigrama.clicked.connect(self.create_organigrama)
        self.abrir_organigrama.clicked.connect(self.open_organigrama)
        self.Add_Persona.clicked.connect(self.abrir_form_persona)
        self.exportar_PDF.clicked.connect(self.export_scene_to_pdf)
    #Ver El formulario de la dependencia
    def buttonClicked(self):
        # ...
        self.form_window = FormDependencia()
        self.form_window.enviar_dependencia_signal.connect(self.add_dependencia_rect)
        self.form_window.show()
    #ver el formulario de organigrama
    def create_organigrama(self):
        self.form_organigrama = FormOrganigrama()
        self.form_organigrama.enviar_organigrama_signal.connect(self.add_rect_slot)
        self.form_organigrama.show()
    #abrir el organigrama
    def open_organigrama(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Abrir Organigrama", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
        if filename:
            print("Ruta del archivo seleccionado:", filename)
    #abrir el formulario de persona
    def abrir_form_persona(self):
        self.form_persona = FormPersona()
        self.form_persona.show()
        
    def export_scene_to_pdf(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(self, "Guardar como PDF", "", "Archivos PDF (*.pdf)")

        if filename:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filename)

            # Establecer el tamaño de página en el objeto QPrinter
            printer.setPageSize(QPrinter.A4)

            painter = QPainter(printer)
            self.qgv_scene.render(painter)
            painter.end()
            
    def add_rect_slot(self, titulo, fecha):
        rect = QGraphicsRectItem()
        rect.setRect(0, 0, 200, 100)
        rect.setPos(50, 50)
        rect.setFlag(QGraphicsRectItem.ItemIsMovable)  # Hacer que el rectángulo sea movible

        rect.setBrush(Qt.white)  # Establecer el fondo del rectángulo como blanco

        text = QGraphicsTextItem(rect)  # Hacer que el rectángulo sea el padre del texto
        text.setDefaultTextColor(Qt.black)  # Establecer el color del texto como negro
        text.setPlainText(f"Título: {titulo}\nFecha: {fecha}")
        text.setPos(rect.rect().topLeft() + QPointF(10, 10))  # Posicionar el texto dentro del rectángulo

        self.qgv_scene.addItem(rect)
        self.qgv_scene.addItem(text)
        self.qgv.setScene(self.qgv_scene)

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
        
    # def add_dependencia_rect(self,depen,nombre,apellido):
    #     rect = QGraphicsRectItem()
    #     rect.setRect(0, 0, 200, 100)
    #     rect.setPos(50, 50)
    #     rect.setFlag(QGraphicsRectItem.ItemIsMovable)

    #     rect.setBrush(Qt.white)

    #     text = QGraphicsTextItem(rect)
    #     text.setDefaultTextColor(Qt.black)
    #     text.setPlainText(f"Título: {depen}\nApellid{apellido}\nNombre:{nombre}")
    #     text.setPos(rect.rect().topLeft() + QPointF(10, 10))

    #     self.qgv_scene.addItem(rect)
    #     self.qgv_scene.addItem(text)
    #     self.qgv.setScene(self.qgv_scene)
    


class FormOrganigrama(QWidget):
    enviar_organigrama_signal = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(FormOrganigrama, self).__init__(parent)
        self.setWindowTitle("Formulario Organigrama")

        loadUi("form_organigrama.ui", self)

        self.enviar_button.clicked.connect(self.enviar_organigrama)

    def enviar_organigrama(self):
        # TODO: validar que el campo fecha sea una fecha valida
        titulo = self.titulo_lineEdit.text()
        fecha = self.fecha_lineEdit.text()
        org = Organigrama(titulo, fecha)
        database.connect()
        database.insertarData("Organigrama", org.get_dict())
        self.enviar_organigrama_signal.emit(titulo, fecha)
        self.close()
        database.disconnect()

class FormDependencia(QWidget):
    enviar_dependencia_signal = pyqtSignal(str, str,str)
    def __init__(self,parent=None):
        super(FormDependencia, self).__init__(parent)
        self.setWindowTitle("Formulario dependencia")

        loadUi("form_window.ui", self)

        self.enviar_dependencia.clicked.connect(self.e_dependencia)

    def e_dependencia(self):
        # TODO: validar que el lider ingresado exista
        nombre_dep = self.input_dependencia_nombre.text()
        nombre_lider = self.input_dependencia_nombre_lider.text()
        apellido_lider = self.input_dependencia_apellido_lider.text()
        
        database.connect()
        rows = database.buscarData("Persona", f"nombre = '{nombre_lider}' AND apellido = '{apellido_lider}'", ["id"])
        
        if len(rows) == 0 or rows == -1:
            print("Error al crear la dependencia")
            return
        
        id_lider = rows[0][0] 
        
        dependencia = Dependencia(nombre_dep, id_lider, organigrama_activo)
        database.insertarData("Dependencia", dependencia.getDict())
        self.enviar_dependencia_signal.emit(nombre_dep,nombre_lider,apellido_lider)
        database.disconnect()
        self.close()  # Cerrar la ventana de formulario

class FormPersona(QWidget):
    def __init__(self):
        super(FormPersona, self).__init__()
        self.setWindowTitle("Formulario Persona")

        loadUi("form_persona.ui", self)
        self.boton_enviar.clicked.connect(self.e_persona)

    def e_persona(self):
        ci = self.campo_ci.text()
        nombre = self.campo_nombre.text()
        apellido = self.campo_apellido.text()
        telefono = self.campo_telefono.text()
        direccion = self.campo_direccion.text()
        dependencia = self.campo_dependencia.text()
        salario = self.campo_salario.text()

        database.connect()
        rows = database.buscarData("Dependencia", f"nombre = '{dependencia}'", ["id"])
        id_dep = rows[0][0]
        persona = Persona(ci, apellido, nombre, telefono, direccion, id_dep, int(salario))
        database.insertarData("Persona", persona.getDict())
        database.disconnect()
        self.close()
class GraphWindow(QMainWindow):

    def __init__(self, graph, nombre_archivo):
        super().__init__()
        self.setWindowTitle('Graph Visualization')
        self.graph = graph
        self.scene = MyGraphicsView()
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

def generate_graph():
    dot = Digraph()
    return dot

def generate_node(graph, nombre_dependencia):
    graph.node(nombre_dependencia, nombre_dependencia)

def connect_nodes(graph, node1_label, node2_label, edge_label):
    graph.edge(node1_label, node2_label, edge_label)
if __name__ == '__main__':
    app = QApplication([])
    graph = generate_graph()
    generate_node(graph, 'Node 1')
    generate_node(graph, 'Node 2')
    connect_nodes(graph, 'Node 1', 'Node 2', 'Edge')
    window = MainWindow()
    window.show()
    app.exec_()

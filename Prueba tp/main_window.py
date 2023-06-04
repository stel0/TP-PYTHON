import os
from PyQt5.QtCore import Qt, QPointF, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsRectItem,
    QFileDialog,
    QWidget,
)
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.uic import loadUi

import grafos
from Database import Database
from Organigrama import Organigrama
from Dependencia import Dependencia
from Persona import Persona
import sqlite3
import csv
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
DATABASE = "base1.db"
database = Database(DATABASE)
organigrama_activo = 1



class MyGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyGraphicsView, self).__init__(parent)
        self.qgv_scene = QGraphicsScene()
        self.setScene(self.qgv_scene)

    def display_image(self, image_path):
        image = QImage(image_path)
        if image.isNull():
            return

        pixmap = QPixmap.fromImage(image)
        pixmap_item = self.qgv_scene.addPixmap(pixmap)
        self.setSceneRect(pixmap_item.boundingRect())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mi Aplicación")
        self.graphics_view = MyGraphicsView()

        # Cargar el archivo .ui
        loadUi("main_window.ui", self)
        database.connect()
        rows = database.buscarData("Organigrama", f"id = {organigrama_activo}", ["nombre"])
        if len(rows) != 0:
            self.label_organigrama.setText(f"Organigrama: {rows[0][0]}")
        else:
            self.label_organigrama.setText("No ha seleccionado un organigrama")

        # Conectar señales y slots si es necesario
        self.crear_dependencia.clicked.connect(self.create_Dependencia)
        self.crear_organigrama.clicked.connect(self.create_organigrama)
        # self.abrir_organigrama.clicked.connect(self.open_organigrama)
        self.agregar_persona.clicked.connect(self.abrir_form_persona)
        self.action_PDF.triggered.connect(self.exportar_a_pdf)
        self.action_IMAGEN.triggered.connect(self.exportar_a_imagen)
        # self.actionInforme_por_dependencia.triggered.connect(self.Personal_Dependencia)
    #Ver El formulario de la dependencia
    def create_Dependencia(self):
        self.form_window = FormDependencia()
        self.form_window.enviar_dependencia_signal.connect(self.add_dependencia_rect)
        self.form_window.show()

    #ver el formulario de organigrama
    def create_organigrama(self):
        self.form_organigrama = FormOrganigrama()
        self.form_organigrama.enviar_organigrama_signal.connect(self.add_rect_slot)
        self.form_organigrama.show()

    # #abrir el organigrama
    # def open_organigrama(self):
    #     file_dialog = QFileDialog()
    #     filename, _ = file_dialog.getOpenFileName(self, "Abrir Organigrama", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
    #     if filename:
    #         print("Ruta del archivo seleccionado:", filename)

    #abrir el formulario de persona
    def abrir_form_persona(self):
        self.form_persona = FormPersona()
        self.form_persona.show()

    #exporta la escena de graphics view como PDF    
    def exportar_a_pdf(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(self, "Guardar como PDF", "", "Archivos PDF (*.pdf)")

        if filename:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filename)

            # Establecer el tamaño de página en el objeto QPrinter
            printer.setPageSize(QPrinter.A4)

            painter = QPainter(printer)
            self.graphics_view.render(painter)
            painter.end()

    #exporta la escena de graphics view como PNG         
    def exportar_a_imagen(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(self, "Guardar como imagen", "", "Archivos de imagen (*.png *.jpg *.jpeg)")

        if filename:
            image = QImage(self.graphics_view.viewport().size(), QImage.Format_ARGB32)
            image.fill(Qt.transparent)

            painter = QPainter(image)
            self.graphics_view.render(painter)
            painter.end()

            image.save(filename)
    #cambiar a cuadro de texto 
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

    # def update_graph(self, nombre_archivo):
    #     image_path = f'grafos/{nombre_archivo}'  # Cambio de extensión a .png
    #     self.graph.format = 'png'  # Cambio de formato a png
    #     self.graph.render(filename=image_path, cleanup=True)
    #     image = QImage(image_path)
    #     pixmap = QPixmap.fromImage(image)
    #     self.scene.clear()
    #     self.scene.addPixmap(pixmap)
    #     self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)  # Ajuste de la vista
    #     self.resize(pixmap.width(), pixmap.height())
    
    #abre el formulario de dependencias y crea los nodos
    def add_dependencia_rect(self):
        graph = grafos.generate_graph()
        grafos.generar_nodos(graph, 0)

        # Generar el gráfico y guardar la imagen en un archivo
        graph_file = 'INTERFAZ\dependency_graph.png'
        graph.format = 'png'
        graph.render(graph_file)

        # Mostrar la imagen en la vista gráfica
        self.display_image(graph_file)

        # Obtener la ruta completa del archivo generado
        file_path = os.path.abspath(graph_file)
        return file_path
    # def Personal_Dependencia(nombre_dependencia):
    #     # Conexión a la base de datos
    #     conn = sqlite3.connect('base.db')
    #     cursor = conn.cursor()

    #     # Ejecutar una consulta SQL
    #     cursor.execute("SELECT * FROM Persona WHERE dependencia = ? ORDER BY apellido, nombre", (nombre_dependencia,))

    #     # Obtener los resultados de la consulta
    #     resultados = cursor.fetchall()

    #     # Cerrar la conexión a la base de datos
    #     conn.close()

    #     # Especificar el nombre del archivo de texto
    #     nombre_archivo = 'informe.txt'

    #     # Escribir los resultados en el archivo de texto
    #     with open(nombre_archivo, 'w') as archivo:
    #         escritor = csv.writer(archivo, delimiter='\t')
    #         escritor.writerows(resultados)

    #     print("Informe generado y guardado en", nombre_archivo)

    # Personal_Dependencia("Dependencia A")
    
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

        loadUi("form_dependencia.ui", self)

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


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    # Crear una instancia de MyGraphicsView
    graphics_view = MyGraphicsView()

# Llamar al método display_image y proporcionar la ruta de la imagen
    file_path = 'dependency_graph.png.png'
    graphics_view.display_image(file_path)

    # Mostrar la ventana principal que contiene el QGraphicsView
    # graphics_view.show()

    window.show()
    app.exec_()

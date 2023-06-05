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
    QGraphicsPixmapItem
)
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.uic import loadUi
from PyQt5 import uic

import grafos
from Database import Database
from Organigrama import Organigrama
from Dependencia import Dependencia
from Persona import Persona
import sqlite3
import csv
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices,QIcon
DATABASE = "base2.db"
database = Database(DATABASE)

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
    
class formulario_informe(QWidget):
    def __init__(self, parent=None):
        super(formulario_informe, self).__init__(parent)
        uic.loadUi("form_informe_dependencia.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_dependencia_2.clicked.connect(self.enviar_dato_dependencia)
    def enviar_dato_dependencia(self):
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
        self.close()

class MainWindow(QMainWindow):
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mi Aplicación")
        
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        # Cargar el archivo .ui
        uic.loadUi("main_window.ui", self)
        self.scene = QGraphicsScene()

        """Id del organigrama activo"""    
        self.organigrama_activo = 0

        #Botones del main window y call de funciones
        self.crear_dependencia.clicked.connect(self.create_Dependencia)
        self.crear_organigrama.clicked.connect(self.create_organigrama)
        # self.abrir_organigrama.clicked.connect(self.open_organigrama)
        self.lista_organigramas.currentIndexChanged.connect(self.organigrama_seleccionado)
        
        self.agregar_persona.clicked.connect(self.abrir_form_persona)
        self.action_PDF.triggered.connect(self.exportar_a_pdf)
        self.action_IMAGEN.triggered.connect(self.exportar_a_imagen)
        self.actionInforme_por_dependencia.triggered.connect(self.Personal_Dependencia)
        self.editar_persona.clicked.connect(self.abrir_form_editar_persona)
        #despliega los nombres de los organigramas en el combox
        self.despliega_organigramas()
        

        # # Agregar imagen 
        # # Crear un QPixmap y cargar una imagen en él
        # pixmap =  QPixmap("INTERFAZ\dependency_graph.png.png")
        # # pixmap = QPixmap("INTERFAZ\dependency_graph.png.png")
        
        # # Crear un QGraphicsPixmapItem con el QPixmap
        # pixmap_item = QGraphicsPixmapItem(pixmap)

        # # Agregar el QGraphicsPixmapItem a la escena
        # self.scene.addItem(pixmap_item) 

        # # Establecer la escena en el QGraphicsView
        # """qgv es el nombre del la ventana qgraphics view en el main_window.ui"""
        # self.qgv.setScene(self.scene)

    # def organigrama_abierto(self):
    #     database.connect()
    #     rows = database.buscarData("Organigrama", f"id = {self.organigrama_activo}", ["nombre"])
    #     if len(rows) != 0:
    #         self.label_organigrama.setText(f"Organigrama: {rows[0][0]}")
    #     else:
    #         self.label_organigrama.setText("No ha seleccionado un organigrama")


    # Genera un png vacio para el organigrama creado
    def generar_imagen(self,titulo):
        
        # Genero un grafo en blanco
        graph = grafos.generate_graph()

        # Crea una direccion para guardar la imagen
        image_path = f'INTERFAZ\{titulo}'

        # Convierte a png
        graph.format = 'png'

        # Y renderiza dicha imagen
        graph.render(filename=image_path, cleanup=True)
        
        
    # Agregar imagen 
    def agregar_imagen(self,nombre):

        # Crear un QPixmap y cargar una imagen en él
        pixmap =  QPixmap(f"INTERFAZ\{nombre}.png")

        # Crear un QGraphicsPixmapItem con el QPixmap
        pixmap_item = QGraphicsPixmapItem(pixmap)

        # Elimina la anterio imagen y agrega el QGraphicsPixmapItem a la escena
        self.scene.clear()
        self.scene.addItem(pixmap_item) 

        # Establecer la escena en el QGraphicsView
        """qgv es el nombre del la ventana qgraphics view en el main_window.ui"""
        self.qgv.setScene(self.scene) 

    # Despliega todos los organigramas para ser seleccionado
    def despliega_organigramas(self):

        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Organigrama", None,["nombre"])

        # Agregar los datos al combo box
        for item in data:
            self.lista_organigramas.addItem(item[0])

        # Cerrar la conexión a la base de datos
        database.disconnect()

    # Agrega los organigramas al inicio del combo box
    def agregar_organigrama(self,titulo):
        self.lista_organigramas.addItem(titulo)

    #Despliega toda la informacion del organigrama seleccionado
    def organigrama_seleccionado(self, index):
        
        # Obtener el nombre de la opción seleccionada
        selected_option = self.lista_organigramas.currentText()
        
        # Conectamos a la base de datos
        database.connect()

        # Obtengo el id del organigrama
        rows = database.buscarData("Organigrama",f"nombre='{selected_option}'",["id"])
        id_option = rows[0][0]
        self.organigrama_activo = id_option
        # print(id_option)

        # Obtengo todas las dependencias del organigrama
        data_depencencias = database.buscarData("Dependencia",f"id_organigrama='{id_option}'",["nombre"])
        print("Nombre de las dependencias")
        # for dependencia in data_depencencias:
        #     print(f"Nombre dependencia:{dependencia[0]}")

        # Obtengo todas las personas del organigrama
        data_personas = database.buscarData("Persona",f"id_organigrama='{id_option}'",["nombre"])
        print("Nombre de las personas")
        # for persona in data_personas:
        #     print(f"Nombre persona:{persona[0]}")

        # agregamos la imagen del organigrama
        self.agregar_imagen(selected_option)  

    #Ver El formulario de la dependencia
    def create_Dependencia(self):
        self.form_window = FormDependencia(self.organigrama_activo)
        # self.form_window.enviar_dependencia_signal.connect(self.add_dependencia_rect)
        self.form_window.show()

    #ver el formulario de organigrama
    def create_organigrama(self):
        self.form_organigrama = FormOrganigrama()
        self.form_organigrama.enviar_organigrama_signal.connect(self.agregar_organigrama)
        self.form_organigrama.enviar_organigrama_signal.connect(self.generar_imagen)
        self.form_organigrama.show()

    # #abrir el organigrama
    # def open_organigrama(self):
    #     file_dialog = QFileDialog()
    #     filename, _ = file_dialog.getOpenFileName(self, "Abrir Organigrama", "", "Archivos de Imagen (*.png *.jpg *.jpeg)")
    #     if filename:
    #         print("Ruta del archivo seleccionado:", filename)

    #abrir el formulario de persona
    def abrir_form_persona(self):
        self.form_persona = FormPersona(self.organigrama_activo)
        self.form_persona.show()
    #abrir el formulario de editar persona    
    def abrir_form_editar_persona(self):
        self.form_persona = FormEditarPersona(self.organigrama_activo)
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
            self.qgv.render(painter)
            painter.end()

    #exporta la escena de graphics view como PNG         
    def exportar_a_imagen(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(self, "Guardar como imagen", "", "Archivos de imagen (*.png *.jpg *.jpeg)")

        if filename:
            image = QImage(self.graphics_view.viewport().size(), QImage.Format_ARGB32)
            image.fill(Qt.transparent)

            painter = QPainter(image)
            self.qgv.render(painter)
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
        grafos.generar_grafo(graph, 0, 1)

        # Generar el gráfico y guardar la imagen en un archivo
        graph_file = 'INTERFAZ\Tilines SA.png'
        graph.format = 'png'
        graph.render(graph_file)

        # Mostrar la imagen en la vista gráfica
        self.graphics_view.display_image(graph_file)

        # Obtener la ruta completa del archivo generado
        file_path = os.path.abspath(graph_file)
        return file_path
    
    def Personal_Dependencia(self):
        self.formulario=formulario_informe()
        self.formulario.show()
    
class FormOrganigrama(QWidget):
    enviar_organigrama_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FormOrganigrama, self).__init__(parent)
        self.setWindowTitle("Formulario Organigrama")


        loadUi("form_organigrama.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_button.clicked.connect(self.enviar_organigrama)

    def enviar_organigrama(self):
        # TODO: validar que el campo fecha sea una fecha valida
        titulo = self.titulo_lineEdit.text()
        fecha = self.fecha_lineEdit.text()
        org = Organigrama(titulo, fecha)
        database.connect()
        database.insertarData("Organigrama", org.get_dict())
        self.enviar_organigrama_signal.emit(titulo)
        database.disconnect()
        #cierra ventana
        self.close()


class FormDependencia(QWidget):
    enviar_dependencia_signal = pyqtSignal(str, str,str)
    # def __init__(self,parent=None):
    #     super(FormDependencia, self).__init__(parent)
    def __init__(self,organigrama_id):
        super(FormDependencia, self).__init__()
        self.setWindowTitle("Formulario dependencia")

        loadUi("form_dependencia.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_dependencia.clicked.connect(self.e_dependencia)

        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        self.organigrama_id = organigrama_id

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
        dependencia = Dependencia(nombre_dep, id_lider,self.organigrama_id)
        database.insertarData("Dependencia", dependencia.getDict())
        self.enviar_dependencia_signal.emit(nombre_dep,nombre_lider,apellido_lider)
        database.disconnect()
        self.close()  # Cerrar la ventana de formulario


class FormPersona(QWidget):
    def __init__(self,id_organigrama):
        super(FormPersona, self).__init__()
        self.setWindowTitle("Formulario Persona")

        loadUi("form_persona.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.boton_enviar.clicked.connect(self.e_persona)

        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        self.id_organigrama = id_organigrama
        
        self.despliega_dependencias()
        


    def e_persona(self):
        ci = self.campo_ci.text()
        nombre = self.campo_nombre.text()
        apellido = self.campo_apellido.text()
        telefono = self.campo_telefono.text()
        direccion = self.campo_direccion.text()
        dependencia = self.lista_dependencias.currentText()
        salario = self.campo_salario.text()

        #Conexion a la base de datos
        database.connect()

        rows = database.buscarData("Dependencia", f"nombre = '{dependencia}'", ["id"])
        id_dep = rows[0][0]
        print(id_dep)
        persona = Persona(ci, apellido, nombre, telefono, direccion, id_dep,self.id_organigrama, int(salario))

        # Envio de los datos del formulario persona a la base de datos
        database.insertarData("Persona", persona.getDict())

        # Desconexion a la base de datos
        database.disconnect()

        self.close()


    # Depliega las dependencias en el formulario persona
    def despliega_dependencias(self):

        #print(self.id_organigrama)
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.lista_dependencias.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()

class FormEditarPersona(QWidget):
    def __init__(self, id_organigrama):
        super(FormEditarPersona, self).__init__()
        self.setWindowTitle("Editar Persona")
        self.id_organigrama = id_organigrama
        loadUi("form_editar_persona.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.boton_editar.clicked.connect(self.e_persona)
        self.despliega_personas()
        self.despliega_dependencias()
        self.lista_personas.currentIndexChanged.connect(self.persona_seleccionada)

    def persona_seleccionada(self, index):
        
        # Obtener el nombre de la opción seleccionada
        selected_option = self.lista_personas.currentText()
        
        # Conectamos a la base de datos
        database.connect()

        # Obtengo el id del organigrama
        rows = database.buscarData("Personas",f"nombre='{selected_option}'",["ci","apellido","nombre","telefono","direccion","salario"])
        print(rows)
    def e_persona(self):
        database.connect()

        ci = self.campo_ci.text()
        nombre = self.campo_nombre.text()
        apellido = self.campo_apellido.text()
        telefono = self.campo_telefono.text()
        direccion = self.campo_direccion.text()
        dependencia = self.lista_dependencias.currentText()
        salario = self.campo_salario.text()

        #Conexion a la base de datos
        
        rows = database.buscarData("Dependencia", f"nombre = '{dependencia}'", ["id"])
        id_dep = rows[0][0]
        persona = Persona(ci, apellido, nombre, telefono, direccion, id_dep, int(salario))

        # Envio de los datos del formulario persona a la base de datos
        database.insertarData("Persona", persona.getDict())

        # Desconexion a la base de datos
        database.disconnect()

        # self.close()
        # Este self close no esta de mas? ya que en database.disconnect() ya desconecta

    # Depliega las personas en el formulario persona
    def despliega_personas(self):
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_personas
        for item in data:
            self.lista_personas.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()

    # Depliega las dependencias en el formulario persona
    def despliega_dependencias(self):
        #database.buscarData("Organigrama", f"id = {organigrama_activo}", ["nombre"])
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama= {self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.lista_dependencias.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()


        
           
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

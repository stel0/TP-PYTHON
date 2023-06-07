from reportlab.pdfgen import canvas
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
    QDialog,
    QGraphicsPixmapItem,
    QLabel,
    QMessageBox
)
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.uic import loadUi
from PyQt5 import uic
import subprocess
import grafos
from Database import Database
from Organigrama import Organigrama
from Dependencia import Dependencia
from Persona import Persona
import sqlite3
import csv
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices,QIcon
from datetime import datetime
import re
DATABASE = "base.db"
database = Database(DATABASE)

class eliminar_dependencia_form(QWidget):
    actualizarOrganigrama = pyqtSignal(str) #actua como actualizador del qgv
    def __init__(self, id_organigrama):
        super(eliminar_dependencia_form, self).__init__()
        self.id_organigrama=id_organigrama
        uic.loadUi("eliminar_dependencia.ui",self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.btn_eliminar_dependencia.clicked.connect(self.eliminar_dependencia)
        self.despliega_dependencias()

    def despliega_dependencias(self):
        #print(self.id_organigrama)
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.elige_dependencia.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()

    def eliminar_dependencia(self):
        dependencia = self.elige_dependencia.currentText()

        database.connect()
        dependenciaData = database.buscarData("Dependencia",f"nombre = '{dependencia}'",["manager_id"])
        manager_id = dependenciaData[0][0]
        if manager_id:
            database.deleteRecord("Dependencia",f"manager_id = {manager_id}")
        else:
            print("No se puede eliminar dependencia del lider")

        self.actualizarOrganigrama.emit("a")
        database.disconnect()

        self.close()

class eliminar_persona_form(QWidget):
    actualizarOrganigrama = pyqtSignal(str)
    def __init__(self, id_organigrama):
        super(eliminar_persona_form, self).__init__()
        self.id_organigrama=id_organigrama
        uic.loadUi("eliminar_persona.ui",self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.btn_eliminar_persona.clicked.connect(self.eliminar_persona)
        self.despliega_personas()
        self.mw = MainWindow()

    def eliminar_persona(self):
        database.connect()
        nombre = self.elige_persona.currentText()
        personaId = ''.join(filter(str.isdigit,nombre))

        if personaId != 0:
            database.deleteRecord("Persona",f"id = {personaId}")
            print(f"Se ha eliminado con exito {nombre} :)")
        else:
            print("No se puede eliminar el jefe")

        database.disconnect()

        self.actualizarOrganigrama.emit("a")
        self.close()

    def despliega_personas(self):
        #print(self.id_organigrama)
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama={self.id_organigrama}",["id","nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.elige_persona.addItem(f"{item[0]} - {item[1]}")
        # Cerrar la conexión a la base de datos
        database.disconnect()

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
        self.lista_organigramas.currentIndexChanged.connect(self.organigrama_seleccionado)
        self.agregar_persona.clicked.connect(self.abrir_form_persona)
        self.action_PDF.triggered.connect(self.exportar_a_pdf)
        self.action_IMAGEN.triggered.connect(self.exportar_a_imagen)
        self.actionInforme_por_dependencia.triggered.connect(self.Personal_Dependencia)
        self.actionPersonal_por_Dependencia_extendido.triggered.connect(self.Personal_Dependencia_Sucesoras)
        self.actionSalario_por_Dependencia.triggered.connect(self.Salario_Dependencia)
        self.actionSalario_por_Dependencia_extendido.triggered.connect(self.Salario_Dependencia_Sucesoras)
        self.boton_editar_dependencia.clicked.connect(self.editar_dependencia)
        self.editar_persona.clicked.connect(self.abrir_form_editar_persona)
        self.color_button.clicked.connect(self.cambiar_color_menu)

        self.eliminar_dependencia.clicked.connect(self.openEliminarDependencia)
        self.eliminar_persona.clicked.connect(self.openEliminarPersona)

        #despliega los nombres de los organigramas en el combox
        self.despliega_organigramas()


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
    def agregar_organigrama(self, titulo, id_org):
        self.lista_organigramas.addItem(titulo)
        self.lista_organigramas.setCurrentText(titulo)
        self.organigrama_activo = id_org
        # Obtengo todas las dependencias del organigrama
        data_depencencias = database.buscarData("Dependencia",f"id_organigrama='{id_org}'",["nombre"])
        #print("Nombre de las dependencias")
        # for dependencia in data_depencencias:
        #     print(f"Nombre dependencia:{dependencia[0]}")
        # Obtengo todas las personas del organigrama
        data_personas = database.buscarData("Persona",f"id_organigrama='{id_org}'",["nombre"])
        #print("Nombre de las personas")
        # for persona in data_personas:
        #     print(f"Nombre persona:{persona[0]}")
        # agregamos la imagen del organigrama
        self.agregar_imagen(titulo) 

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
        # Obtengo todas las dependencias del organigrama
        data_depencencias = database.buscarData("Dependencia",f"id_organigrama='{id_option}'",["nombre"])
        print("Nombre de las dependencias")
        # Obtengo todas las personas del organigrama
        data_personas = database.buscarData("Persona",f"id_organigrama='{id_option}'",["nombre"])
        print("Nombre de las personas")

        self.agregar_imagen(selected_option)  

    #Ver El formulario de la dependencia
    def create_Dependencia(self):
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.organigrama_activo} ",["id", "nombre"])
        database.disconnect()

        if data != -1:
            self.form_window = FormDependencia(self.organigrama_activo)
            self.form_window.enviar_dependencia_signal.connect(self.generar_grafo)
            self.form_window.show()
        else:
            return

    def editar_dependencia(self):
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.organigrama_activo} ",["id", "nombre"])
        database.disconnect()

        if data != -1:
            self.form_dependencia = FormEditarDependencia(self.organigrama_activo)
            self.form_dependencia.editar_dependencia_signal.connect(self.generar_grafo)
            self.form_dependencia.show()
        else:
            return
        

    def crear_jefe(self):
        self.form_jefe = FormJefe(self.organigrama_activo)
        self.form_jefe.show()
   
    def openEliminarDependencia(self):
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.organigrama_activo} ",["id", "nombre"])
        database.disconnect()
        if data != -1:
            self.formWindow = eliminar_dependencia_form(self.organigrama_activo)
            self.formWindow.actualizarOrganigrama.connect(self.generar_grafo)
            self.formWindow.show()
        else:
            return
        
   
    #ver el formulario de organigrama
    def create_organigrama(self):
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.organigrama_activo} ",["id", "nombre"])
        database.disconnect()

        if data != -1:
            self.form_organigrama = FormOrganigrama()
            self.form_organigrama.enviar_organigrama_signal.connect(self.agregar_organigrama)
            self.form_organigrama.enviar_organigrama_signal.connect(self.generar_imagen)
            self.form_organigrama.enviar_organigrama_signal.connect(self.crear_jefe)
            self.form_organigrama.show()
        else:
            return
        
        

    def openEliminarPersona(self):
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.organigrama_activo} ",["id", "nombre"])
        database.disconnect()

        if data != -1:
            self.formWindow = eliminar_persona_form(self.organigrama_activo)
            self.formWindow.actualizarOrganigrama.connect(self.generar_grafo)
            self.formWindow.show()
        else:
            return
        
    
    #abrir el formulario de persona
    def abrir_form_persona(self):
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.organigrama_activo} ",["id", "nombre"])
        database.disconnect()
        if data != -1:
            self.form_persona = FormPersona(self.organigrama_activo)
            self.form_persona.show()
        else:
            self.crear_jefe()
        

    #abrir el formulario de editar persona    
    def abrir_form_editar_persona(self):
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.organigrama_activo} ",["id", "nombre"])
        database.disconnect()
        if data != -1:
            self.form_persona = FormEditarPersona(self.organigrama_activo)
            self.form_persona.show()
        else:
            return
    
    #exporta la escena de graphics view como PDF    
    def exportar_a_pdf(self):
    # Obtener el nombre del archivo y la ruta de la imagen
        nombre = self.lista_organigramas.currentText()
        ruta_imagen = f"INTERFAZ\{nombre}.png"
        ruta_pdf = f"INTERFAZ\{nombre}.pdf"
        # Abrir la imagen con QImage
        imagen = QImage(ruta_imagen)

        # Crear un objeto canvas de ReportLab para generar el PDF
        c = canvas.Canvas(ruta_pdf)
        # Definir las dimensiones del PDF basado en las dimensiones de la imagen
        ancho = imagen.width()
        alto = imagen.height()
        c.setPageSize((ancho, alto))

        # Dibujar la imagen en el PDF
        c.drawImage(ruta_imagen, 0, 0, ancho, alto)
        # Guardar el PDF y cerrar el objeto canvas
        c.save()
        #abrir directamente el pdf
        QDesktopServices.openUrl(QUrl.fromLocalFile(f"INTERFAZ\{nombre}.pdf"))
              
    def exportar_a_imagen(self):
        nombre = self.lista_organigramas.currentText()
        QDesktopServices.openUrl(QUrl.fromLocalFile(f"INTERFAZ\{nombre}.png"))

    def generar_grafo(self):
        graph = grafos.generate_graph()
        nombre = self.lista_organigramas.currentText()
        grafos.generar_grafo(graph, 0, self.organigrama_activo, nombre)
        
        # Generar el gráfico y guardar la imagen en un archivo
        graph_file = f'INTERFAZ\{nombre}'
        graph.format = 'png'
        graph.render(graph_file)
        
        self.agregar_imagen(nombre)
    
    def Personal_Dependencia(self):
        self.formulario=formulario_informe(self.organigrama_activo)
        self.formulario.show()

    def Personal_Dependencia_Sucesoras(self):
        self.formulario=formulario_informe_dependencia_sucesoras(self.organigrama_activo)
        self.formulario.show()

    def Salario_Dependencia(self):
        self.formulario=formulario_informe_salario_dependencia(self.organigrama_activo)
        self.formulario.show()

    def Salario_Dependencia_Sucesoras(self):
        self.formulario=formulario_informe_salario_dependencia_sucesoras(self.organigrama_activo)
        self.formulario.show()

    def cambiar_color_menu(self):
        # Verificar el estado actual del menú
        if self.menuBar().styleSheet() == "":
            # Cambiar el color del menú y las palabras en el menú
            self.menuBar().setStyleSheet("background-color: rgb(170, 170, 255); color: black; ")

            # Cambiar el color de label_organigrama
            label_organigrama = self.findChild(QLabel, "label_organigrama")
            if label_organigrama:
                label_organigrama.setStyleSheet("background-color: white; color: black;")

            # Cambiar el color del centralwidget
            self.centralwidget.setStyleSheet("background-color: white; color: black;")
        else:
            # Restaurar los colores originales del menú y las palabras en el menú
            self.menuBar().setStyleSheet("")

            # Restaurar los colores originales de label_organigrama
            label_organigrama = self.findChild(QLabel, "label_organigrama")
            if label_organigrama:
                label_organigrama.setStyleSheet("background-color: #27263c; color: white;")

            # Restaurar los colores originales del centralwidget
            self.centralwidget.setStyleSheet("")

class formulario_informe(QWidget):
    def __init__(self, id_organigrama):
        super(formulario_informe, self).__init__()
        self.id_organigrama=id_organigrama
        uic.loadUi("form_informe_dependencia.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_dependencia_2.clicked.connect(self.enviar_dato_dependencia)
        self.despliega_dependenciass()
    
    # Depliega las dependencias en el formulario persona
    def despliega_dependenciass(self):
        #print(self.id_organigrama)
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.dependencia_select.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()
    
    def enviar_dato_dependencia(self):
        database.connect()
        selected_option=self.dependencia_select.currentText()
        dep=database.buscarData("Dependencia",f"nombre='{selected_option}' AND id_organigrama={self.id_organigrama}",["id"])
        id_dep=dep[0][0]

          # Obtengo el id del organigrama
        personas = database.buscarData("Persona", f"id_dependencia='{id_dep}' AND id_organigrama={self.id_organigrama}", ["nombre", "apellido"])
        nombres = []
        for persona in personas:
            nombres.append(f"{persona[1]} {persona[0]}")
        nombres_normalizados = []

        for nombre in nombres:
            nombre_normalizado = nombre.strip().title()
            nombres_normalizados.append(nombre_normalizado)

        nombres_ordenados = sorted(nombres_normalizados)

        with open("Personal_Por_Dependencia.txt", "w") as file:
            for nombre in nombres_ordenados:
                file.write(nombre + "\n")

        database.disconnect()

        informe = "Personal_Por_Dependencia.txt"
        QDesktopServices.openUrl(QUrl.fromLocalFile(informe))
        self.close()

class formulario_informe_dependencia_sucesoras(QWidget):
    def __init__(self, id_organigrama):
        super(formulario_informe_dependencia_sucesoras, self).__init__()
        self.id_organigrama=id_organigrama
        uic.loadUi("form_informe_dependencia_sucesoras.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_dependencia_3.clicked.connect(self.enviar_dato_dependencia)
        self.despliega_dependenciass()

    # Depliega las dependencias en el formulario persona
    def despliega_dependenciass(self):
        #print(self.id_organigrama)
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.elige_dependencia.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()
    
    def enviar_dato_dependencia(self):
        # TODO: muestra las personas de la dependencia y también a las personas que estan debajo
        database.connect()
        selected_option=self.elige_dependencia.currentText()
        dep=database.buscarData("Dependencia",f"nombre='{selected_option}' AND id_organigrama={self.id_organigrama}",["id"])
        id_dep=dep[0][0]

        # Obtengo el id del organigrama
        personas = database.buscarData("Persona", f"id_dependencia='{id_dep}' AND id_organigrama={self.id_organigrama}", ["id", "nombre", "apellido"])
        nombres = []
        id_personas = []
        for persona in personas:
            nombres.append(f"{persona[2]} {persona[1]}")
            id_personas.append(persona[0])

        nombres_normalizados = []
        personas_dict = {}

        for nombre in nombres:
            nombre_normalizado = nombre.strip().title()
            nombres_normalizados.append(nombre_normalizado)
        
        for i in range(len(nombres_normalizados)):
            personas_dict[nombres_normalizados[i]] = id_personas[i]
        print(personas_dict)
        nombres_ordenados = sorted(nombres_normalizados)

        with open("Personal_Por_Dependencia_Sucesoras.txt", "w") as file:
            for nombre in nombres_ordenados:
                file.write(nombre + "\n")
                id_persona = personas_dict[nombre]
                dependencias = database.buscarData("Dependencia", f"manager_id = {id_persona} AND id_organigrama = {self.id_organigrama}", ["nombre"])
                print(dependencias)
                for dependencia in dependencias:
                    file.write("\t" + dependencia[0] + "\n")
        
        database.disconnect()

        informe = "Personal_Por_Dependencia_Sucesoras.txt"
        QDesktopServices.openUrl(QUrl.fromLocalFile(informe))
        self.close()

class formulario_informe_salario_dependencia(QWidget):
    def __init__(self, id_organigrama):
        super(formulario_informe_salario_dependencia, self).__init__()
        self.id_organigrama=id_organigrama
        uic.loadUi("form_informe_salario_dependencia.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_dependencia_4.clicked.connect(self.enviar_dato_dependencia)
        self.despliega_dependenciass()

    # Depliega las dependencias en el formulario persona
    def despliega_dependenciass(self):
        #print(self.id_organigrama)
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.selecionador_depende.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()
    
    def enviar_dato_dependencia(self):
        # TODO: mostrar salario por dependencia
        '''
        Salario por Dependencia: Para una dependencia, presenta la cantidad de 
        personal y el total de salarios para la dependencia. 
        No incluye a las dependencias sucesoras.   
        '''
        database.connect()
        selected_option=self.selecionador_depende.currentText()
        dep=database.buscarData("Dependencia",f"nombre='{selected_option}' AND id_organigrama={self.id_organigrama}",["id"])
        id_dep=dep[0][0]

          # Obtengo el id del organigrama
        personas = database.buscarData("Persona", f"id_dependencia='{id_dep}' AND id_organigrama={self.id_organigrama}", ["nombre", "apellido", "salario"])
        nombres = []
        personas_dict = {}
        for persona in personas:
            nombres.append(f"{persona[1]} {persona[0]}")
        nombres_normalizados = []
        for i in range(len(nombres)):
            nombre_normalizado = nombres[i].strip().title()
            nombres_normalizados.append(nombre_normalizado)
            personas_dict[nombre_normalizado] = personas[i][2]

        nombres_ordenados = sorted(nombres_normalizados)

        with open("Salario_Por_Dependencia.txt", "w") as file:
            for nombre in nombres_ordenados:
                file.write(f"{nombre}: {personas_dict[nombre]}\n")

        database.disconnect()
        informe = "Salario_Por_Dependencia.txt"
        QDesktopServices.openUrl(QUrl.fromLocalFile(informe))
        self.close()

class formulario_informe_salario_dependencia_sucesoras(QWidget):
    def __init__(self, id_organigrama):
        super(formulario_informe_salario_dependencia_sucesoras, self).__init__()
        self.id_organigrama=id_organigrama
        uic.loadUi("form_informe_salario_dependencia_extendido.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_dependencia_5.clicked.connect(self.enviar_dato_dependencia)
        self.despliega_dependenciass()

    # Depliega las dependencias en el formulario persona
    def despliega_dependenciass(self):
        #print(self.id_organigrama)
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.selecionador_dependencia.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()
    
    def enviar_dato_dependencia(self):
        # TODO: mostrar salario por dependencia extendido, personas por debajo
        '''
        Salario por Dependencia extendido: Para una dependencia, presenta la 
        cantidad de personal y el total de salarios para la dependencia. 
        Incluye el detalle de las dependencias sucesoras.
        '''
        database.connect()
        selected_option = self.selecionador_dependencia.currentText()
        dep = database.buscarData("Dependencia",f"nombre='{selected_option}' AND id_organigrama={self.id_organigrama}",["id"])
        id_dep = dep[0][0]
        informe = "Salario_Por_Dependencia_Extendido.txt"
        # Obtengo el id del organigrama
        personas = database.buscarData("Persona", f"id_dependencia='{id_dep}' AND id_organigrama={self.id_organigrama}", ["id", "nombre", "apellido", "salario"])
        nombres = []
        for persona in personas:
            nombres.append(f"{persona[2]} {persona[1]}")
        nombres_normalizados = []
        # id_dict contiene el id como value
        # y el nombre como key
        id_dict = {}
        # salario_dict contiene el salario como value
        # y el nombre como key
        salario_dict = {}
        for i in range(len(nombres)):
            nombre_normalizado = nombres[i].strip().title()
            nombres_normalizados.append(nombre_normalizado)
            id_dict[nombre_normalizado] = personas[i][0]
            salario_dict[nombre_normalizado] = personas[i][3]
        nombres_ordenados = sorted(nombres_normalizados)

        with open(informe, "w") as file:
            for nombre in nombres_ordenados:
                file.write(f"{nombre}: {salario_dict[nombre]}\n")
                id_persona = id_dict[nombre]
                dependencias = database.buscarData("Dependencia", f"manager_id = {id_persona} AND id_organigrama = {self.id_organigrama}", ["id", "nombre"])
                for dependencia in dependencias:
                    id_dep = dependencia[0]
                    personas = database.buscarData("Persona", f"id_dependencia='{id_dep}' AND id_organigrama={self.id_organigrama}", ["id", "nombre", "apellido", "salario"])
                    print(personas)
                    nombres1 = []
                    for persona in personas:
                        nombres1.append(f"{persona[2]} {persona[1]}")
                    nombres_normalizados = []
                    salario_dict1 = {}
                    if len(personas) > 0:
                        file.write(f"\t{dependencia[1]}\n")
                        for i in range(len(nombres1)):
                            nombre_normalizado = nombres1[i].strip().title()
                            nombres_normalizados.append(nombre_normalizado)
                            salario_dict1[nombre_normalizado] = personas[i][3]
                        nombres_ordenados1 = sorted(nombres_normalizados)
                        for nombre in nombres_ordenados1:
                            file.write(f"\t\t{nombre}: {salario_dict1[nombre]}\n")
        database.disconnect()

        QDesktopServices.openUrl(QUrl.fromLocalFile(informe))
        self.close()

class FormOrganigrama(QWidget):
    enviar_organigrama_signal = pyqtSignal(str, int)

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
        if len(titulo)>0 and len(fecha)>0 :
            database.connect()
            database.insertarData("Organigrama", org.get_dict())
            organigramas = database.buscarData("Organigrama", f"nombre = '{titulo}'", ["id"])
            # org id tomara el id del ultimo organigrama ingresado con el nombre titulo, lo que nos permite tener mas de un org con
            # el mismo nombre
            for org in organigramas:
                org_id = org[0]

            self.enviar_organigrama_signal.emit(titulo, org_id)
            database.disconnect()
            #cierra ventana
            self.close()
        else:
            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()


class FormDependencia(QWidget):
    enviar_dependencia_signal = pyqtSignal(str)
    def __init__(self,id_organigrama):
        super(FormDependencia, self).__init__()
        self.setWindowTitle("Formulario dependencia")
        self.id_organigrama = id_organigrama
        self.lista_id = []
        self.selected_id = 1
        loadUi("form_dependencia.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_dependencia.clicked.connect(self.e_dependencia)
        self.despliega_personas()
        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        
        self.elegir_lider.currentIndexChanged.connect(self.persona_seleccionada)

    def despliega_personas(self):
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.id_organigrama} ",["id", "nombre"])
        # si no desplegamos el combobox al crear la dependencia, no se cambia el selected_id ya que no se llama a persona_seleccionada
        # por lo tanto, hacemos que se seleccione por default a la primera persona del combo_box
        self.selected_id = data[0][0]
        # Agregar los datos al combo box lista_personas
        for item in data:
            self.elegir_lider.addItem(item[1])
            self.lista_id.append(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()

    def persona_seleccionada(self):
        
        # Obtener el nombre de la opción seleccionada
        selected_index = self.elegir_lider.currentIndex()
        self.selected_id = self.lista_id[selected_index]
        

    def e_dependencia(self):
        # TODO: validar que el lider ingresado exista
        nombre_dep = self.input_dependencia_nombre.text()
        if len(nombre_dep)>0:
            database.connect()

            rows = database.buscarData("Persona", f"id = {self.selected_id}", ["nombre","apellido"])


            if len(rows) == 0 or rows == -1:
                print("Error al crear la dependencia")
                return
            
            id_lider = self.selected_id

            dependencia = Dependencia(nombre_dep, id_lider,self.id_organigrama)

            database.insertarData("Dependencia", dependencia.getDict())
            self.enviar_dependencia_signal.emit(nombre_dep)
            database.disconnect()
            self.close()  
            # Cerrar la ventana de formulario
        else:
            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

class FormEditarDependencia(QWidget):
    editar_dependencia_signal = pyqtSignal(str)
    def __init__(self,id_organigrama):
        super(FormEditarDependencia, self).__init__()
        self.setWindowTitle("Formulario editar dependencia")
        self.id_organigrama = id_organigrama
        self.lista_id = []
        self.selected_id = 1
        loadUi("form_editar_dependencia.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.enviar_dependencia.clicked.connect(self.edit_dependencia)
        self.despliega_dependencias()
        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        
        self.elegir_dependencia.currentIndexChanged.connect(self.dependencia_seleccionada)
    def dependencia_seleccionada(self):
        
        # Obtener el nombre de la opción seleccionada
        selected_index = self.elegir_dependencia.currentIndex()
        self.selected_id = self.lista_id[selected_index]
    
    def despliega_dependencias(self):
        #print(self.id_organigrama)
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre", "id"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.elegir_dependencia.addItem(item[0])
            self.lista_id.append(item[1])
        # Cerrar la conexión a la base de datos
        database.disconnect()

    def edit_dependencia(self):
        # TODO: validar que el lider ingresado exista
        nombre_dep = self.input_dependencia_nombre.text()
        if len(nombre_dep)>0:
            database.connect()

            database.updateData("Dependencia", ["nombre"], [nombre_dep], f"id = {self.selected_id}")
            self.editar_dependencia_signal.emit(nombre_dep)
            database.disconnect()
            self.close()  
            # Cerrar la ventana de formulario
        else:
            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

        
class FormJefe(QWidget):
    def __init__(self,id_organigrama):
        super(FormJefe, self).__init__()
        self.setWindowTitle("Formulario Jefe")
        self.cerrar = False
        loadUi("form_jefe.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.boton_enviar.clicked.connect(self.e_jefe)

        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        self.id_organigrama = id_organigrama
    
    def closeEvent(self, event):
        if self.cerrar:
            event.accept()
        else:
            event.ignore()

    def e_jefe(self):
        ci = self.campo_ci.text()
        nombre = self.campo_nombre.text()
        apellido = self.campo_apellido.text()
        telefono = self.campo_telefono.text()
        direccion = self.campo_direccion.text()
        salario = self.campo_salario.text()
        if ci.isdigit() and telefono.isdigit() and salario.isdigit() and len(nombre)>0 and len(apellido)>0  and len(direccion)>0 and len(ci)>0 and len(telefono)>0 and len(salario)>0:
            #Conexion a la base de datos
            database.connect()
            persona = Persona(ci, apellido, nombre, telefono, direccion, 0 ,self.id_organigrama, int(salario))

            # Envio de los datos del formulario persona a la base de datos
            database.insertarData("Persona", persona.getDict())
            # Desconexion a la base de datos
            database.disconnect()
            # cerramos el form
            self.cerrar = True
            self.close()
        else:
            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()
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
        if ci.isdigit() and telefono.isdigit() and salario.isdigit() and len(ci)>0 and len(telefono)>0 and len(salario)>0 and len(nombre)>0 and len(apellido)>0 and len(dependencia)>0 and len(direccion)>0:
        # Continuar con el procesamiento de los datos
                    #Conexion a la base de datos
            database.connect()

            rows = database.buscarData("Dependencia", f"nombre = '{dependencia}' AND id_organigrama = {self.id_organigrama}", ["id"])
            id_dep = rows[0][0]
            print(id_dep)
            persona = Persona(ci, apellido, nombre, telefono, direccion, id_dep,self.id_organigrama, int(salario))

            # Envio de los datos del formulario persona a la base de datos
            database.insertarData("Persona", persona.getDict())

            # Desconexion a la base de datos
            database.disconnect()
            self.close()
        else:
            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

        


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
        self.lista_id = []
        self.selected_id = 0
        loadUi("form_editar_persona.ui", self)
        self.setWindowIcon(QIcon("INTERFAZ\ICONOS\icono_superior.png"))
        self.boton_editar.clicked.connect(self.e_persona)
        self.despliega_personas()
        #self.despliega_dependencias()
        self.lista_personas.currentIndexChanged.connect(self.persona_seleccionada)

    def persona_seleccionada(self, index):
        
        # Obtener el nombre de la opción seleccionada
        selected_index = self.lista_personas.currentIndex()
        self.selected_id = self.lista_id[selected_index]
        
        # Conectamos a la base de datos
        database.connect()

        # Obtengo el id del organigrama
        rows = database.buscarData("Persona",f"id={self.selected_id}",["ci","apellido","nombre","telefono","direccion","salario"])
        self.campo_ci.setText(rows[0][0])
        self.campo_apellido.setText(rows[0][1])
        self.campo_nombre.setText(rows[0][2])
        self.campo_telefono.setText(rows[0][3])
        self.campo_direccion.setText(rows[0][4])
        self.campo_salario.setText(str(rows[0][5]))
        #print(rows)
    def e_persona(self):
        database.connect()

        ci = self.campo_ci.text()
        nombre = self.campo_nombre.text()
        apellido = self.campo_apellido.text()
        telefono = self.campo_telefono.text()
        direccion = self.campo_direccion.text()
        salario = self.campo_salario.text()
        if ci.isdigit() and telefono.isdigit() and salario.isdigit() and len(nombre)>0 and len(apellido)>0  and len(direccion)>0:
        # Continuar con el procesamiento de los datos
            #Conexion a la base de datos
            database.updateData("Persona", ["ci", "apellido", "nombre", "telefono", "direccion", "salario"], 
                                [ci, apellido, nombre, telefono, direccion, int(salario)], f"id = {self.selected_id}")
            # Desconexion a la base de datos
            database.disconnect()

            self.close()
            # Este self close no esta de mas? ya que en database.disconnect() ya desconecta
            # Se usa para cerrar el form
        else:
            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

    # Depliega las personas en el formulario persona
    def despliega_personas(self):
        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.id_organigrama}",["id", "nombre"])
        # Agregar los datos al combo box lista_personas
        for item in data:
            self.lista_personas.addItem(item[1])
            self.lista_id.append(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()

    # Depliega las dependencias en el formulario persona
    # def despliega_dependencias(self):
    #     #database.buscarData("Organigrama", f"id = {organigrama_activo}", ["nombre"])
    #     # Ejecutar una consulta para obtener los datos de la base de datos
    #     database.connect()
    #     data = database.buscarData("Dependencia", f"id_organigrama= {self.id_organigrama}",["nombre"])
    #     # Agregar los datos al combo box lista_dependencias
    #     for item in data:
    #         self.lista_dependencias.addItem(item[0])
    #     # Cerrar la conexión a la base de datos
    #     database.disconnect()
            
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

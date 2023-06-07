from reportlab.pdfgen import canvas
from PyQt5.QtCore import  pyqtSignal
from PyQt5.QtGui import  QPixmap, QImage, QPainter
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QWidget,
    QGraphicsPixmapItem,
    QLabel,
    QMessageBox,
    QGraphicsView
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
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices,QIcon
import re
import os
DATABASE = "base.db" # Base de datos 
database = Database(DATABASE)

"""
    Ventana principal
"""

class MainWindow(QMainWindow):
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mi Aplicación")
        
        self.setWindowTitle("Mi Aplicación")
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        uic.loadUi("static\\ui\\main_window.ui", self)# Cargar el archivo .ui
        self.setupUi()
        self.scene = QGraphicsScene() #Utilizamos esto?
        """Id del organigrama activo"""    
        self.organigrama_activo = 0

        #Botones del main window y call de funciones

        # Boton crear dependencia
        self.crear_dependencia.clicked.connect(self.create_Dependencia) 
        # Boton crear organigrama
        self.crear_organigrama.clicked.connect(self.create_organigrama) 
        # lista de organigrama abierto
        self.lista_organigramas.currentIndexChanged.connect(self.organigrama_seleccionado) 
        # Boton crear persona
        self.agregar_persona.clicked.connect(self.abrir_form_persona) 
        # Boton exportar a pdf
        self.action_PDF.triggered.connect(self.exportar_a_pdf) 
        # Boton exportar a imagen
        self.action_IMAGEN.triggered.connect(self.exportar_a_imagen) 
        # Boton Informe personal por dependencia
        self.actionInforme_por_dependencia.triggered.connect(self.Personal_Dependencia) 
        # Boton Informe Personal por Dependencia extendido 
        self.actionPersonal_por_Dependencia_extendido.triggered.connect(self.Personal_Dependencia_Sucesoras) 
        # Boton Informe Salario por dependencia
        self.actionSalario_por_Dependencia.triggered.connect(self.Salario_Dependencia)
        # Boton Informe Salario por dependencia extendido
        self.actionSalario_por_Dependencia_extendido.triggered.connect(self.Salario_Dependencia_Sucesoras)
        # Boton editar dependencia
        self.boton_editar_dependencia.clicked.connect(self.editar_dependencia)
        # Boton editar persona
        self.editar_persona.clicked.connect(self.abrir_form_editar_persona)
        # Boton switch dark/white
        self.color_button.clicked.connect(self.cambiar_color_menu)
        # Boton eliminar dependencia
        self.eliminar_dependencia.clicked.connect(self.openEliminarDependencia)
        # Boton eliminar persona
        self.eliminar_persona.clicked.connect(self.openEliminarPersona)

        #despliega los nombres de los organigramas en el combox
        self.despliega_organigramas()

    def setupUi(self):
        # Encuentra el QGraphicsView por su nombre
        self.graphicsView = self.findChild(QGraphicsView, "qgv")

        # Habilita el desplazamiento con el cursor
        self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)  # Opcional, para mejorar la calidad de la representación
    def generar_imagen(self,titulo):# Genera un png vacio para el organigrama creado
        
        graph = grafos.generate_graph() # Genero un grafo en blanco
        image_path = f'static\images\{titulo}' # Crea una direccion para guardar la imagen
        graph.format = 'png' # Convierte a png
        graph.render(filename=image_path, cleanup=True) # Y renderiza dicha imagen
        
    def agregar_imagen(self,nombre):# Agregar imagen 

        pixmap =  QPixmap(f"static\images\{nombre}.png") # Crear un QPixmap y cargar una imagen en él
        pixmap_item = QGraphicsPixmapItem(pixmap) # Crear un QGraphicsPixmapItem con el QPixmap
        self.scene.clear() # Elimina la imagen anterior 
        self.scene.addItem(pixmap_item) # Agrega el QGraphicsPixmapItem a la escena
        """qgv es el nombre del la ventana qgraphics view en el main_window.ui"""
        self.qgv.setScene(self.scene)  # Establecer la escena en el QGraphicsView

    def despliega_organigramas(self):# Despliega todos los organigramas para ser seleccionado
        
        database.connect() # Conexion a base.db
        data = database.buscarData("Organigrama", None,["nombre"]) # Query a base.db
        for item in data: # Agrega los datos al combo box
            self.lista_organigramas.addItem(item[0]) 
        database.disconnect()# Desconexión a base.db

    def agregar_organigrama(self, titulo, id_org): # Agrega los organigramas al combo box

        self.lista_organigramas.addItem(titulo)  # Agrega el titulo
        self.lista_organigramas.setCurrentText(titulo)  # Agrega el titulo
        self.organigrama_activo = id_org # Set del id del organigrama actual
        self.agregar_imagen(titulo) # Agrega la imagen a la ventana principal

    # Despliega toda la informacion del organigrama seleccionado
    def organigrama_seleccionado(self, index):

        selected_option = self.lista_organigramas.currentText() # Nombre del organigrama seleccionado
        database.connect()
        rows = database.buscarData("Organigrama",
                                   f"nombre='{selected_option}'",
                                   ["id"])
        database.disconnect()
        id_option = rows[0][0] # Obtengo el id del organigrama
        self.organigrama_activo = id_option # Set del id del organigrama actual
        self.agregar_imagen(selected_option)  # Agrega la imagen a la ventana principal 

    def create_Dependencia(self):# Ver El formulario de la dependencia

        # Llama la clase formulario dependencia
        # print(self.organigrama_activo)
        self.form_window = FormDependencia(self.organigrama_activo) 
        # Muestra formulario dependencia
        self.form_window.show() 
        # Señal para que actualice la ventana
        self.form_window.enviar_dependencia_signal.connect(self.generar_grafo) 

    def editar_dependencia(self): # Ver formulario editar dependencia
    
        # llama la clase formulario editar dependencia
        self.form_dependencia = FormEditarDependencia(self.organigrama_activo) 
        # Muestra formulario editar dependencia 
        self.form_dependencia.show() 
        # Señal para que actualice la ventana
        self.form_dependencia.editar_dependencia_signal.connect(self.generar_grafo)
        
    def abrir_form_editar_persona(self): # Abrir el formulario de editar persona

        # Llama a la clase FormEditarPersona
        self.form_persona = FormEditarPersona(self.organigrama_activo)
        # Muestra el formulario
        self.form_persona.show()
        self.form_persona.editar_persona_signal.connect(self.generar_grafo)

    def crear_jefe(self): # Ver formulario crear jefe

        # llama la clase formulario crear jefe
        self.form_jefe = FormJefe(self.organigrama_activo) 
        # Muestra formulario crear jefe
        self.form_jefe.show() 
   
    def openEliminarDependencia(self): # Ver fomulario eliminar dependencia

        # Llama la clase fomulario eliminar dependencia
        self.formWindow = eliminar_dependencia_form(self.organigrama_activo) 
        # Muestr el formulario
        self.formWindow.show()
        # Señal para que actualice la ventana
        self.formWindow.actualizarOrganigrama.connect(self.generar_grafo)
   
    def create_organigrama(self):  #ver el formulario de organigrama

        # Llama la clase formulario de organigrama
        self.form_organigrama = FormOrganigrama()
        # Muestra el formulario
        self.form_organigrama.show()
        # Señales para que actualice la ventana
        self.form_organigrama.enviar_organigrama_signal.connect(self.agregar_organigrama)
        self.form_organigrama.enviar_organigrama_signal.connect(self.generar_imagen)
        self.form_organigrama.enviar_organigrama_signal.connect(self.crear_jefe)
        
        

    def openEliminarPersona(self): #ver el formulario eliminar persona

        # Llama la clase eliminar_persona_form
        self.formWindow = eliminar_persona_form(self.organigrama_activo)
        # Muestra el formulario
        self.formWindow.show()
        # Señal para que actualice la ventana
        self.formWindow.actualizarOrganigrama.connect(self.generar_grafo)
        
    
    def abrir_form_persona(self):# Abrir el formulario de persona

        # Llama la clase FormPersona
        self.form_persona = FormPersona(self.organigrama_activo)
        # Muestra el formulario
        self.form_persona.show()
        
    
    def exportar_a_pdf(self): # Exporta la escena de graphics view como PDF 
    
        # Obtener el nombre del archivo y la ruta de la imagen
        nombre = self.lista_organigramas.currentText()
        ruta_imagen = f"static\images\{nombre}.png"
        ruta_pdf = f"static\informes\PDF\{nombre}.pdf"
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
        QDesktopServices.openUrl(QUrl.fromLocalFile(f"static\informes\PDF\{nombre}.pdf"))
              
    def exportar_a_imagen(self): # Exporta como imagen el organigrama

        # Nombre del organigrama
        nombre = self.lista_organigramas.currentText()
        # Abre una ventana con la imagen exportada
        QDesktopServices.openUrl(QUrl.fromLocalFile(f"static\images\{nombre}.png"))

    def generar_grafo(self): # Genera el organigrama

        # Inicializamos la clase generate_graph
        graph = grafos.generate_graph()
        # Nombre del organigrama 
        nombre = self.lista_organigramas.currentText()
        # Generamos el organigrama
        grafos.generar_grafo(graph, 0, self.organigrama_activo, nombre)
    
        # Generar el gráfico y guardar la imagen en un archivo
        graph_file = f'static\images\{nombre}'
        graph.format = 'png'
        graph.render(graph_file)
        
        # Agregamos la imagen en la ventana
        self.agregar_imagen(nombre)
    
    def Personal_Dependencia(self): # Informe de personal por dependencia
        self.formulario=formulario_informe(self.organigrama_activo)
        self.formulario.show()

    def Personal_Dependencia_Sucesoras(self): # Informe de personal por dependencia extendido

        self.formulario=formulario_informe_dependencia_sucesoras(self.organigrama_activo)
        self.formulario.show()

    def Salario_Dependencia(self): # Informe de salario por dependencia
        
        self.formulario=formulario_informe_salario_dependencia(self.organigrama_activo)
        self.formulario.show()

    def Salario_Dependencia_Sucesoras(self): # Informe de salario por dependencia extendido
        self.formulario=formulario_informe_salario_dependencia_sucesoras(self.organigrama_activo)
        self.formulario.show()

    def cambiar_color_menu(self): # Cambiar colo del menu
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

"""
    Fomulario para informe
"""

class formulario_informe(QWidget):

    def __init__(self, id_organigrama):

        super(formulario_informe, self).__init__()
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        uic.loadUi("static\\ui\\form_informe_dependencia.ui", self)

        # Id del organigrama activo
        self.id_organigrama=id_organigrama 
        # Despliega las dependencias
        self.despliega_dependenciass()
        # Boton enviar dependencia que llama al metodo enviar_dato_dependencia
        self.enviar_dependencia_2.clicked.connect(self.enviar_dato_dependencia)
    
    def despliega_dependenciass(self): # Depliega las dependencias en el formulario persona

        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.dependencia_select.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()
    
    
    def enviar_dato_dependencia(self): # Envia los datos a la base de datos

        database.connect()
        # Nombre de la dependencia seleccionada
        selected_option=self.dependencia_select.currentText()
        dep=database.buscarData("Dependencia",f"nombre='{selected_option}' AND id_organigrama={self.id_organigrama}",["id"])
        # Id de la dependencia
        id_dep=dep[0][0]
        # Nombres de las personas de esa dependencia
        personas = database.buscarData("Persona", f"id_dependencia='{id_dep}' AND id_organigrama={self.id_organigrama}", ["nombre", "apellido"])
        nombres = []
        for persona in personas:
            nombres.append(f"{persona[1]} {persona[0]}")
        nombres_normalizados = []
        for nombre in nombres:
            nombre_normalizado = nombre.strip().title()
            nombres_normalizados.append(nombre_normalizado)
        nombres_ordenados = sorted(nombres_normalizados)
        # Abrimos el txt para escribir
        informe = 'static\informe\Personal_Por_Dependencia.txt'

        os.makedirs(os.path.dirname(informe), exist_ok=True)

        with open(informe, "w") as file:
            for nombre in nombres_ordenados:
                file.write(nombre + "\n")
        database.disconnect()

        QDesktopServices.openUrl(QUrl.fromLocalFile(informe))
        self.close()

"""
    Fomulario para informe dependencias sucesoras
"""

class formulario_informe_dependencia_sucesoras(QWidget):

    def __init__(self, id_organigrama):
        super(formulario_informe_dependencia_sucesoras, self).__init__()
        
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        uic.loadUi("static\\ui\\form_informe_dependencia_sucesoras.ui", self)

        self.id_organigrama=id_organigrama
        self.despliega_dependenciass()
        self.enviar_dependencia_3.clicked.connect(self.enviar_dato_dependencia)

    def despliega_dependenciass(self): # Depliega las dependencias en el formulario persona

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
        # Nombre de la dependencia seleccionada
        selected_option=self.elige_dependencia.currentText()
        dep=database.buscarData("Dependencia",f"nombre='{selected_option}' AND id_organigrama={self.id_organigrama}",["id"])
        id_dep=dep[0][0]
        # Nombres de las personas de esa dependencia
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

        informe = "static/informes/Personal_Por_Dependencia_Sucesoras.txt"

        # Ostia tu hola ivan :D
        os.makedirs(os.path.dirname(informe), exist_ok=True)

        with open(informe, "w") as file:
            for nombre in nombres_ordenados:
                file.write(nombre + "\n")
                id_persona = personas_dict[nombre]
                dependencias = database.buscarData("Dependencia", f"manager_id = {id_persona} AND id_organigrama = {self.id_organigrama}", ["nombre"])
                print(dependencias)
                for dependencia in dependencias:
                    file.write("\t" + dependencia[0] + "\n")
        
        database.disconnect()

        QDesktopServices.openUrl(QUrl.fromLocalFile(informe))
        self.close()

"""
    Fomulario para informe salario dependencia
"""

class formulario_informe_salario_dependencia(QWidget):

    def __init__(self, id_organigrama):
        super(formulario_informe_salario_dependencia, self).__init__()
        self.id_organigrama=id_organigrama
        uic.loadUi("static\\ui\\form_informe_salario_dependencia.ui", self)
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
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

        informe = "static/informes/Salario_Por_Dependencia.txt"

        # Ostia tu hola ivan :D
        os.makedirs(os.path.dirname(informe), exist_ok=True)

        with open(informe, "w") as file:
            for nombre in nombres_ordenados:
                file.write(f"{nombre}: {personas_dict[nombre]}\n")

        database.disconnect()
        QDesktopServices.openUrl(QUrl.fromLocalFile(informe))
        self.close()

"""
    Fomulario para informe salario dependencia extendido
"""

class formulario_informe_salario_dependencia_sucesoras(QWidget):
    
    def __init__(self, id_organigrama):

        super(formulario_informe_salario_dependencia_sucesoras, self).__init__()

        uic.loadUi("static\\ui\\form_informe_salario_dependencia_extendido.ui", self)
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        
        self.enviar_dependencia_5.clicked.connect(self.enviar_dato_dependencia)
        self.id_organigrama=id_organigrama
        self.despliega_dependenciass()

    # Depliega las dependencias en el formulario persona
    def despliega_dependenciass(self):

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
        informe = "static\informes\Salario_Por_Dependencia_Extendido.txt"
        os.makedirs(os.path.dirname(informe), exist_ok=True)
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

"""
    Formulario Organigrama
"""

class FormOrganigrama(QWidget):
    enviar_organigrama_signal = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(FormOrganigrama, self).__init__(parent)

        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        self.setWindowTitle("Formulario Organigrama")
        loadUi("static\\ui\\form_organigrama.ui", self)

        self.enviar_button.clicked.connect(self.enviar_organigrama)

    def enviar_organigrama(self):

        titulo = self.titulo_lineEdit.text()
        fecha = self.fecha_lineEdit.text()
        org = Organigrama(titulo, fecha)

        if len(titulo) > 0 and len(fecha) > 0:
            if re.match(r'^\d{2}/\d{2}/\d{4}$', fecha):
                org = Organigrama(titulo, fecha)
                database.connect()
                database.insertarData("Organigrama", org.get_dict())
                organigramas = database.buscarData("Organigrama", f"nombre = '{titulo}'", ["id"])
                for org in organigramas:
                    org_id = org[0]
                self.enviar_organigrama_signal.emit(titulo, org_id)
                database.disconnect()
                self.close()
            else:
                # Mostrar cuadro de diálogo de error de fecha inválida
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText("La fecha debe tener el formato dd/mm/aaaa.")
                msg.setIconPixmap(QPixmap("static\\icons\\error.png"))
                msg.setStyleSheet("background-color: #27263c; color: white;")
                msg.exec_()
        else:
            # Mostrar cuadro de diálogo de error de campos vacíos
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, revisa tus campos.")
            msg.setIconPixmap(QPixmap("static\\icons\\error.png"))
            msg.setStyleSheet("background-color: #27263c; color: white;")
            msg.exec_()

"""
    Formulario dependencia
"""

class FormDependencia(QWidget):

    enviar_dependencia_signal = pyqtSignal(str)

    def __init__(self,id_organigrama):
        super(FormDependencia, self).__init__()

        loadUi("static\\ui\\form_dependencia.ui", self)
        self.setWindowTitle("Formulario dependencia")
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))

        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        self.id_organigrama = id_organigrama
        self.lista_id = []
        self.selected_id = 1
        self.despliega_personas()

        self.enviar_dependencia.clicked.connect(self.e_dependencia)
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

        # Nombre de la dependencia
        nombre_dep = self.input_dependencia_nombre.text()
        if len(nombre_dep)>0:
            database.connect()
            # Verifica que persona no este vacio
            rows = database.buscarData("Persona", f"id = {self.selected_id}", ["nombre","apellido"])
            if len(rows) == 0 or rows == -1:
                print("Error al crear la dependencia")
                return
            # Id del lider
            id_lider = self.selected_id
            dependencia = Dependencia(nombre_dep, id_lider,self.id_organigrama)
            # Envia los datos de la dependencia
            database.insertarData("Dependencia", dependencia.getDict())
            # Señal para actualizar la ventana
            self.enviar_dependencia_signal.emit(nombre_dep)
            database.disconnect()
            self.close()  # Cerrar la ventana de formulario

        else:

            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            msg.setIconPixmap(QPixmap("static\\icons\\error.png"))
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

"""
    Formulario editar dependencia
"""

class FormEditarDependencia(QWidget):

    editar_dependencia_signal = pyqtSignal(str)

    def __init__(self,id_organigrama):
        super(FormEditarDependencia, self).__init__()

        loadUi("static\\ui\\form_editar_dependencia.ui", self)
        self.setWindowTitle("Formulario editar dependencia")
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))

        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        self.id_organigrama = id_organigrama
        self.lista_id = []
        self.selected_id = 1
        self.enviar_dependencia.clicked.connect(self.edit_dependencia)
        self.despliega_dependencias()
        
        self.elegir_dependencia.currentIndexChanged.connect(self.dependencia_seleccionada) # ?

    def dependencia_seleccionada(self): # Que hace este metodo ?
        # Obtener el nombre de la opción seleccionada
        selected_index = self.elegir_dependencia.currentIndex()
        self.selected_id = self.lista_id[selected_index]
    
    def despliega_dependencias(self):

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
            # Actualiza los datos de esa dependencia
            database.updateData("Dependencia", ["nombre"], [nombre_dep], f"id = {self.selected_id}")
            # Señal para actualizar la ventana
            self.editar_dependencia_signal.emit(nombre_dep)
            database.disconnect()
            self.close() # Cerrar la ventana de formulario
            
        else:
            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            msg.setIconPixmap(QPixmap("static\\icons\\error.png"))
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

"""
    Formulario Jefe
"""

class FormJefe(QWidget):

    def __init__(self,id_organigrama):
        super(FormJefe, self).__init__()

        self.setWindowTitle("Formulario Jefe")
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        loadUi("static\\ui\\form_jefe.ui", self)

        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        self.id_organigrama = id_organigrama
        self.cerrar = False

        self.boton_enviar.clicked.connect(self.e_jefe)
    
    def closeEvent(self, event):

        if self.cerrar:
            event.accept()
        else:
            event.ignore()

    def e_jefe(self):
        
        # Datos del jefe
        ci = self.campo_ci.text()
        nombre = self.campo_nombre.text()
        apellido = self.campo_apellido.text()
        telefono = self.campo_telefono.text()
        direccion = self.campo_direccion.text()
        salario = self.campo_salario.text()

        #Verifica los campos
        if apellido.isalpha() and nombre.isalpha() and ci.isdigit() and telefono.isdigit() and salario.isdigit() and len(nombre)>0 and len(apellido)>0  and len(direccion)>0 and len(ci)>0 and len(telefono)>0 and len(salario)>0:

            #Conexion a la base de datos
            database.connect()
            persona = Persona(ci, apellido, nombre, telefono, direccion, 0 ,self.id_organigrama, int(salario))
            # Envio de los datos del formulario persona a la base de datos
            database.insertarData("Persona", persona.getDict())
            # Desconexion a la base de datos
            database.disconnect()
            # cerramos el form
            self.cerrar = True
            self.close() # Que hace aca el close()?

        else:

            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            msg.setIconPixmap(QPixmap("static\\icons\\error.png"))
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

"""
    Formulario agregar persona
"""    

class FormPersona(QWidget):
   
    def __init__(self,id_organigrama):
        super(FormPersona, self).__init__()

        self.setWindowTitle("Formulario Persona")
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        loadUi("static\\ui\\form_persona.ui", self)

        """ id_organigrama: es el id del organigrama al que pertenece esa persona """
        self.id_organigrama = id_organigrama
        self.despliega_dependencias()

        self.boton_enviar.clicked.connect(self.e_persona)
        
    def e_persona(self): # Metodo enviar datos a la base.db

        # Datos de la persona
        ci = self.campo_ci.text()
        nombre = self.campo_nombre.text()
        apellido = self.campo_apellido.text()
        telefono = self.campo_telefono.text()
        direccion = self.campo_direccion.text()
        dependencia = self.lista_dependencias.currentText()
        salario = self.campo_salario.text()
        #Verifica los campos
        if apellido.isalpha() and nombre.isalpha() and ci.isdigit() and telefono.isdigit() and salario.isdigit() and len(ci)>0 and len(telefono)>0 and len(salario)>0 and len(nombre)>0 and len(apellido)>0 and len(dependencia)>0 and len(direccion)>0:

            #Conexion a la base de datos
            database.connect()
            rows = database.buscarData("Dependencia", f"nombre = '{dependencia}' AND id_organigrama = {self.id_organigrama}", ["id"])
            # Id de la dependencia del que pertenece la persona
            id_dep = rows[0][0]
            # Envio de los datos del formulario persona a la base de datos
            persona = Persona(ci, apellido, nombre, telefono, direccion, id_dep,self.id_organigrama, int(salario))
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
            msg.setIconPixmap(QPixmap("static\\icons\\error.png"))
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

        

    def despliega_dependencias(self): # Depliega las dependencias en el formulario persona

        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Dependencia", f"id_organigrama={self.id_organigrama}",["nombre"])
        # Agregar los datos al combo box lista_dependencias
        for item in data:
            self.lista_dependencias.addItem(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()

"""
    Formulario editar persona
"""

class FormEditarPersona(QWidget):

    editar_persona_signal = pyqtSignal(str)

    def __init__(self, id_organigrama):

        super(FormEditarPersona, self).__init__()

        self.setWindowTitle("Editar Persona")
        loadUi("static\\ui\\form_editar_persona.ui", self)
        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))

        self.lista_id = []
        self.selected_id = 0
        self.id_organigrama = id_organigrama
        self.despliega_personas()

        self.boton_editar.clicked.connect(self.e_persona)
        self.lista_personas.currentIndexChanged.connect(self.persona_seleccionada)

    def persona_seleccionada(self, index):  # Despliega la informacion de la  persona
        
        # Obtener el nombre de la opción seleccionada
        selected_index = self.lista_personas.currentIndex()
        self.selected_id = self.lista_id[selected_index]
        # Conectamos a la base de datos
        database.connect()
        # Datos de la persona
        rows = database.buscarData("Persona",f"id={self.selected_id}",["ci","apellido","nombre","telefono","direccion","salario"])
        self.campo_ci.setText(rows[0][0])
        self.campo_apellido.setText(rows[0][1])
        self.campo_nombre.setText(rows[0][2])
        self.campo_telefono.setText(rows[0][3])
        self.campo_direccion.setText(rows[0][4])
        self.campo_salario.setText(str(rows[0][5]))
        database.disconnect()

    def e_persona(self): # Metodo enviar persona

        # Conexion a la base de datos
        database.connect()
        # Datos de la persona
        ci = self.campo_ci.text()
        nombre = self.campo_nombre.text()
        apellido = self.campo_apellido.text()
        telefono = self.campo_telefono.text()
        direccion = self.campo_direccion.text()
        salario = self.campo_salario.text()
        # Verificacion de los datos
        if apellido.isalpha() and nombre.isalpha() and ci.isdigit() and telefono.isdigit() and salario.isdigit() and len(nombre)>0 and len(apellido)>0  and len(direccion)>0:
            # Enviamos a la base.db
            database.updateData("Persona", ["ci", "apellido", "nombre", "telefono", "direccion", "salario"], 
                                [ci, apellido, nombre, telefono, direccion, int(salario)], f"id = {self.selected_id}")
            # Desconexion a la base de datos
            self.editar_persona_signal.emit('a')
            database.disconnect()
            self.close()

        else:
            # Mostrar cuadro de diálogo de error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Error, Revisa tus campos.")
            msg.setIconPixmap(QPixmap("static\\icons\\error.png"))
            # Cambiar el color del texto a blanco
            msg.setStyleSheet("background-color: #27263c; color: white;")
            # Mostrar el cuadro de diálogo de manera no modal
            msg.exec_()

    def despliega_personas(self):  # Depliega las personas en el formulario persona

        # Ejecutar una consulta para obtener los datos de la base de datos
        database.connect()
        data = database.buscarData("Persona", f"id_organigrama= {self.id_organigrama}",["id", "nombre"])
        # Agregar los datos al combo box lista_personas
        for item in data:
            self.lista_personas.addItem(item[1])
            self.lista_id.append(item[0])
        # Cerrar la conexión a la base de datos
        database.disconnect()


"""
    Clase eliminar dependencia
"""

class eliminar_dependencia_form(QWidget):

    actualizarOrganigrama = pyqtSignal(str) # Actua como actualizador de la ventana principal

    def __init__(self, id_organigrama):
        super(eliminar_dependencia_form, self).__init__()

        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        uic.loadUi("static\\ui\\eliminar_dependencia.ui",self) # Invoca el formuilario.ui

        self.btn_eliminar_dependencia.clicked.connect(self.eliminar_dependencia) # Invoca a la funcion eliminar
        self.id_organigrama=id_organigrama # ID del organigrama actual abierto
        self.despliega_dependencias() # Despliega las dependencias

    # Despliega las dependencias en el formulario eliminar dependencia
    def despliega_dependencias(self):
        database.connect()

        # Ejecutar una consulta para obtener los datos de la base de datos
        data = database.buscarData("Dependencia", 
                                   f"id_organigrama={self.id_organigrama}",
                                   ["nombre","manager_id"])
        for item in data:# Agregar los datos al combo box lista_dependencias
            if item[1] != 1: # Verifica que no sea la dependencia de mayor rango
                self.elige_dependencia.addItem(item[0]) 

        database.disconnect()# Cerrar la conexión a la base de datos

    def eliminar_dependencia(self):
        dependencia = self.elige_dependencia.currentText() # Nombre de la dependencia
        
        database.connect() # Conecta a la base de datos
        # Consulta a la base de datos
        dependenciaData = database.buscarData("Dependencia",
                                              f"nombre = '{dependencia}'",
                                              ["manager_id"]) 
        manager_id = dependenciaData[0][0] # Obtener el manager id 
        database.deleteRecord("Dependencia",f"manager_id = {manager_id}") # Elimina la dependencia y sus hijos
        database.disconnect()

        self.actualizarOrganigrama.emit('a') # Envia una señal para que la ventana se actualice
        self.close() # Cierra el formulario

"""
    Clase eliminar persona
""" 

class eliminar_persona_form(QWidget):
    actualizarOrganigrama = pyqtSignal(str) # Actua como actualizador de la ventana principal

    def __init__(self, id_organigrama):
        super(eliminar_persona_form, self).__init__()

        self.setWindowIcon(QIcon("static\\icons\\icono_superior.png"))
        uic.loadUi("static\\ui\\eliminar_persona.ui",self) # Invoca el formuilario.ui

        self.btn_eliminar_persona.clicked.connect(self.eliminar_persona) # Llama al metodo eliminar persona
        self.id_organigrama=id_organigrama # ID del organigrama actual abierto
        self.despliega_personas() # Despliega las personas en el formulario

    # Metodo eliminar persona
    def eliminar_persona(self):

        nombre = self.elige_persona.currentText() # Nombre de la persona
        personaId = ''.join(filter(str.isdigit,nombre)) # Id de la persona

        database.connect() # Conecta a la base de datos
        database.deleteRecord("Persona",f"id = {personaId}") # Elimina la persona seleccionada
        database.disconnect() # Desconexion a la base de datos

        self.actualizarOrganigrama.emit("a") # Envia una señal para que la ventana se actualice
        self.close() # Cierra el formulario

    # Despliega las personas en el formulario eliminar persona
    def despliega_personas(self):

        database.connect() # Conecta a la base de datos
        # Consulta a la base de datos
        data = database.buscarData("Persona", 
                                   f"id_organigrama={self.id_organigrama}",
                                   ["id","nombre","id_dependencia"])
        for item in data:# Agregar los datos al combo box lista_dependencias
            if item[2] != 0: # Despliega solo si es distinto a la persona jefe
                self.elige_persona.addItem(f"{item[0]} - {item[1]}")
        database.disconnect() # Desconexión a la base de datos

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

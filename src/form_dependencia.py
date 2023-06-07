from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import chatGPT as gpt
from ..db_test import Database as db
from ..db_test import Dependencia
from PyQt5.uic import loadUi

class Ui_form_window(object):
    def setupUi(self, form_window):
        form_window.setObjectName("form_window")
        form_window.resize(320, 240)
        self.window = None
        self.centralwidget = QtWidgets.QWidget(form_window)
        self.centralwidget.setObjectName("centralwidget")
        self.input_dependencia_nombre = QtWidgets.QLineEdit(self.centralwidget)
        self.input_dependencia_nombre.setGeometry(QtCore.QRect(30, 80, 181, 20))
        self.input_dependencia_nombre.setObjectName("input_dependencia_nombre")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 191, 16))
        self.label_2.setObjectName("label_2")
        self.input_dependencia_ci_lider = QtWidgets.QLineEdit(self.centralwidget)
        self.input_dependencia_ci_lider.setGeometry(QtCore.QRect(30, 130, 181, 20))
        self.input_dependencia_ci_lider.setObjectName("input_dependencia_ci_lider")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 110, 231, 16))
        self.label_3.setObjectName("label_3")
        self.enviar_dependencia = QtWidgets.QPushButton(self.centralwidget,clicked=lambda:self.e_dependencia())
        self.enviar_dependencia.setGeometry(QtCore.QRect(30, 160, 75, 23))
        self.enviar_dependencia.setObjectName("enviar_dependencia")
        form_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(form_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 22))
        self.menubar.setObjectName("menubar")
        form_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(form_window)
        self.statusbar.setObjectName("statusbar")
        form_window.setStatusBar(self.statusbar)

        self.retranslateUi(form_window)
        QtCore.QMetaObject.connectSlotsByName(form_window)

    def retranslateUi(self, form_window):
        _translate = QtCore.QCoreApplication.translate
        form_window.setWindowTitle(_translate("form_window", "MainWindow"))
        self.label.setText(_translate("form_window", "Crear dependencia"))
        self.label_2.setText(_translate("form_window", "Ingrese el nombre de la dependencia:"))
        self.label_3.setText(_translate("form_window", "Ingrese el CI del lider de la dependencia:"))
        self.enviar_dependencia.setText(_translate("form_window", "Enviar"))

    def e_dependencia(self):
        database = db.Database("base.db")

        nombre_dep = self.input_dependencia_nombre.text()
        ci_lider = self.input_dependencia_ci_lider.text()

        database.connect()

        graph = gpt.generate_graph()
        gpt.generate_node(graph,self.input_dependencia_nombre.text())

        self.window = gpt.GraphWindow(graph,"holaMundo")
        self.window.show()      

        loadUi("main_window_1.ui", self)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form_window = QtWidgets.QMainWindow()
    ui = Ui_form_window()
    ui.setupUi(form_window)
    form_window.show()
    sys.exit(app.exec_())

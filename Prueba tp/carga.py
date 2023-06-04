import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QCoreApplication, QBasicTimer
from Inicio import MainWindow as mw


class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("carga.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.timer = QBasicTimer()
        self.step = 0

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            self.close()
            self.loadMainWindow()
        else:
            self.progressBar.setValue(self.step)
            self.step += 1

    def startProgress(self):
        self.timer.start(10, self)

    def loadMainWindow(self):
        self.new_window = mw()
        self.new_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    QCoreApplication.processEvents()  # Permitir que se muestre la pantalla de carga

    splash.startProgress()
    sys.exit(app.exec_())

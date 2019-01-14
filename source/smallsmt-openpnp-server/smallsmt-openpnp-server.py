from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5 import uic

import sys
import openpnp

from mainwindow import Ui_MainWindow


#Ui_MainWindow, QtBaseClass = uic.loadUiType("mainwindow.ui")

class SmallSmtDriverApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.openpnp = openpnp.OpenPnp()
        self.openpnp.openPnpLog.connect(self.logMessages)

    def enableComm(self):
        pass

    def disableComm(self):
        pass

    def listPorts(self):
        available_ports = QSerialPortInfo.availablePorts()
        self.comboBoxSerialPorts.clear()
        for port in available_ports:
            self.comboBoxSerialPorts.addItems(port.portName())

    @pyqtSlot(str)
    def logMessages(self,msg):
        self.loggerWindow.appendPlainText(msg)




def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = SmallSmtDriverApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

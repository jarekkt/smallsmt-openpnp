from PyQt5.QtCore import QObject,QIODevice,pyqtSignal,pyqtSlot
from PyQt5.QtSerialPort import QSerialPort


class CommSerial(QObject):

    getFromSmallSmt = pyqtSignal(bytearray)

    opened = False

    def __init__(self):
        QObject.__init__(self)

    def disable(self):
        if self.opened == True:
            self.qport.close()

    def enable(self,name):

        try:
            self.qport = QSerialPort()
            self.qport.setObjectName(name)
            self.qport.setBaudRate(QSerialPort.Baud115200)
            self.qport.setDataBits(QSerialPort.Data8)
            self.qport.setParity(QSerialPort.NoParity)
            self.qport.setFlowControl(QSerialPort.NoFlowControl)
            if self.qport.open(QIODevice.ReadWrite)== True:
                result = 1
                opened = True
        except:
            result = 0

        if opened == True:
            self.qport.readyRead.connect(self.received)

        return result

    @pyqtSlot()
    def  received(self):
        chars = self.qport.readAll()
        #
        # TODO
        #
        self.getFromSmallSmt.emit(chars)


    def sendToSmallSmt(self, message):
        if self.opened == True:
            self.qport.write(message)

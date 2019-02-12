from PyQt5.QtCore import QObject,QIODevice,pyqtSignal,pyqtSlot,QTimer
from PyQt5.QtSerialPort import QSerialPort
import time



class CommSerial(QObject):

    getFromSmallSmt = pyqtSignal(bool,bytearray)

    def __init__(self,timeout = 1000):
        QObject.__init__(self)
        self.opened = False
        self.timeout = timeout
        self.inBuffer = bytearray()
        self.frameIsValid = False
        self.frameTimestamp = self.millis()
        self.qport = None

    def millis(self):
        return int(round(time.time()*1000))

    def disable(self):
        if self.opened == True:
            self.qport.close()

    def enable(self,name):
        if self.opened == True:
            self.disable()
        try:
            result = False
            self.qport = QSerialPort()
            self.qport.setObjectName(name)
            self.qport.setBaudRate(QSerialPort.Baud115200)
            self.qport.setDataBits(QSerialPort.Data8)
            self.qport.setParity(QSerialPort.NoParity)
            self.qport.setFlowControl(QSerialPort.NoFlowControl)
            if self.qport.open(QIODevice.ReadWrite)== True:
                result = True
                self.opened = True
        except:
            pass

        if self.opened == True:
            self.qport.readyRead.connect(self.received)

        return result

    def disable(self):
        if self.qport:
            self.qport.close()
            self.qport = None
            self.opened = False

    @pyqtSlot()
    def received(self):
        chars = self.qport.readAll()
        idx = 0

        # There was too large time gap between reads
        if self.millis() - self.frameTimestamp > 100:
            self.frameIsValid = False
            self.inBuffer.clear()

        # If frame not valid - look for start character
        if self.frameIsValid == False:
            for ii in range(0,len(chars)):
               if chars[ii] == 0xEE:
                   idx = ii
                   self.frameIsValid = True
                   break
        # For valid frame - take remaining characters
        if self.frameIsValid == True:
            for ii in range(idx, len(chars)):
                self.inBuffer.append(chars[ii])

        # Check for end characters
        idx = 0
        done = False
        if len(self.inBuffer) >= 8:
            for ii in range(3, self.inBuffer):
                if (self.inBuffer(ii) == 0xFF) and (self.inBuffer(ii+1) == 0xFC) and (self.inBuffer(ii) == 0xFF+2) and (self.inBuffer(ii+3) == 0xFF):
                    self.inBuffer = self.inBuffer[:(ii+3)]
                    done = True
                    break
        # If frame found, report it
        if done:
            self.getFromSmallSmt.emit(chars)
            self.frameIsValid = False
            self.inBuffer.clear()

        self.frameTimestamp = self.millis()

    def sendToSmallSmt(self, message):
        if self.opened == True:
            self.qport.write(message)

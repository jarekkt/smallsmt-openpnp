from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtCore import QObject,QEventLoop,QTimer
import commsockets
import smallsmtprotocol


class OpenPnp(QObject):

    PROTOCOL_VERSION = "V1"
    status = 1
    value  = 0
    X = 0
    Y = 0
    Z1 = 0
    C1 = 0
    Z2 = 0
    C2 = 0
    Z3 = 0
    C3 = 0
    Z4 = 0
    C4 = 0

    timer = QTimer()


    openPnpLog = pyqtSignal([str])

    def __init__(self,machine,serial):
        QObject.__init__(self)
        self.comm = commsockets.CommSockets()
        self.comm.getFromOpenPnp.connect(self.processRequest)
        self.machine = machine
        self.serial = serial

        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.executeRequestTimeout)
        self.serial.getFromSmallSmt.connect(self.executeRequestResponse)

    def logInfo(self,logText):
        self.openPnpLog.emit(logText)


    def executeResponse(self,msgId):
        response = str.format("[:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:]", \
                              self.PROTOCOL_VERSION,msgId,self.status,self.value,\
                              self.X,self.Y,\
                              self.Z1,self.C1,\
                              self.Z2,self.C2,\
                              self.Z3,self.C3,\
                              self.Z4,self.C4)

        self.comm.sendToOpenPnp(response)
        self.logInfo(str.format("Request response: {} ", response))

    def executeRequest(self,msgId,command):
        result = -1
        self.msgId = msgId
        if command.startswith("home("):
            result = self.cmd__home()
        elif command.startswith("moveTo("):
            result = self.cmd__moveTo(command)
        elif command.startswith("setEnabled("):
            result = self.cmd__setEnabled(command)
        elif command.startswith("pick("):
            result = self.cmd__pick(command)
        elif command.startswith("place("):
            result = self.cmd__place(command)
        elif command.startswith("actuate("):
            result = self.cmd__actuate(command)
        elif command.startswith("actuateRead("):
            result = self.cmd__actuateRead(command)
        else:
            pass

        if result == -1:
            # The code comes here only in case of wrong command
            # Otherwise it is being processed in commands itself
            self.logInfo(str.format("Command unrecognized or not sent: {} ", command))
            self.status = -1
            self.executeResponse(self.msgId)


    def cmd__home(self):
        return 0

    def cmd__moveTo(self,command):
        return 0

    def cmd__setEnabled(self,command):
        return 0

    def cmd__actuate(self,command):
        return 0

    def cmd__pick(self,command):
        return 0

    def cmd__place(self,command):
        return 0

    def cmd__setEnabled(self,command):

        self.openPnpLog.emit("Executed: setEnabled")

        self.packet = smallsmtprotocol.SmallSmtCmd__Online()
        return self.cmd__execute(self.packet,1000)

    def cmd__execute(self,packet,timeout):

        result = self.serial.sendToSmallSmt(self.packet.bytes)
        result = 0
        if result == 0:
            #Send succesfull
            if timeout!= 0:
                self.timer.start(timeout)
            else:
                self.timer.stop()
            return 0
        else:
            return  result


    @pyqtSlot()
    def executeRequestResponse(self):
        self.timer.stop()

        self.status = 0
        self.executeResponse(self.msgId)

    @pyqtSlot()
    def executeRequestTimeout(self):
        self.logInfo(str.format("Command timeout - no machine response "))
        self.status = -1
        self.executeResponse(self.msgId)





    def cmd__actuateRead(self,command):
        return 0

    @pyqtSlot(str)
    def processRequest(self,request):
        msgOk = 0
        parts = request.split(":")
        if len(parts) == 5:
            if (parts[0] == '<') and (parts[4] == '>') and (parts[1] == self.PROTOCOL_VERSION):
               self.logInfo(str.format("Request received: {} ", request))
               msgId = parts[2]
               msgCommand = parts[3]
               msgOk =1
               self.executeRequest(msgId,msgCommand)
        if msgOk == 0:
            self.logInfo(str.format("Request faulty: {} ",request) )




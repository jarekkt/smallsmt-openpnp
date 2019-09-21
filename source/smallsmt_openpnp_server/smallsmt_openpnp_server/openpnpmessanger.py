from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QObject,  QTimer, Qt
import commsockets


class OpenPnpMessanger(QObject):
    PROTOCOL_VERSION = "V1"
    status = 1
    value = 0
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

    openPnpLogMessanger = pyqtSignal([str])
    openPnpRequest = pyqtSignal([str])

    def __init__(self):
        QObject.__init__(self)
        self.comm = commsockets.CommSockets()
        self.comm.getFromOpenPnp.connect(self.processRequest)

    def logInfo(self, logText):
        self.openPnpLogMessanger.emit(logText)

    def executeResponse(self):
        response = str.format("[:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:]", \
                              self.PROTOCOL_VERSION, self.msgId, self.status, self.value, \
                              self.X, self.Y, \
                              self.Z1, self.C1, \
                              self.Z2, self.C2, \
                              self.Z3, self.C3, \
                              self.Z4, self.C4)

        self.comm.sendToOpenPnp(response)
        self.logInfo(str.format("Request response: {} ", response))

    @pyqtSlot(str)
    def processRequest(self, request):
        msgOk = 0
        parts = request.split(":")
        if len(parts) == 5:
            if (parts[0] == '<') and (parts[4] == '>') and (parts[1] == self.PROTOCOL_VERSION):
                self.logInfo(str.format("Request received: {} ", request))
                self.msgId = parts[2]
                self.msgCommand = parts[3]
                msgOk = 1
                self.openPnpRequest.emit(self.msgCommand)
        if msgOk == 0:
            self.logInfo(str.format("Request faulty: {} ", request))











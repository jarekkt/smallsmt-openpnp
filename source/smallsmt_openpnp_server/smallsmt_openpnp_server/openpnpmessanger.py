from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QObject,  QTimer, Qt
import commsockets
import openpnpcoords


class OpenPnpMessanger(QObject):
    PROTOCOL_VERSION = "V1"
    status = 1
    value = 0

    openPnpLogMessanger = pyqtSignal([str])
    openPnpRequest = pyqtSignal([str])

    def __init__(self,coords):
        QObject.__init__(self)
        self.coords = coords
        self.comm = commsockets.CommSockets()
        self.comm.getFromOpenPnp.connect(self.processRequest)

    def logInfo(self, logText):
        self.openPnpLogMessanger.emit(logText)

    def executeResponse(self):
        response = str.format("[:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:]", \
                              self.PROTOCOL_VERSION, self.msgId, self.status, self.value, \
                              self.coords.X.value, self.coords.Y.value, \
                              self.coords.Z12.value, self.coords.C1.value, \
                              -self.coords.Z12.value, self.coords.C2.value, \
                              self.coords.Z34.value, self.coords.C3.value, \
                              -self.coords.Z34.value, self.coords.C4.value)

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











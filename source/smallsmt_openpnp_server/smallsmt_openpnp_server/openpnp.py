from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtCore import QObject,QEventLoop,QTimer,Qt

import smallsmtprotocol
import smallsmtmessanger
import openpnpmessanger
import openpnpcoords


class OpenPnp(QObject):

    openPnpLog = pyqtSignal([str])

    def __init__(self,machineConfig,serial):
        QObject.__init__(self)

        # Machine configuration
        self.machineConfig = machineConfig

        # Machine global coordinates
        self.coords = openpnpcoords.OpenPnpCoords(self.machineConfig)

        # Connection  to OpenPnp
        self.openpnp = openpnpmessanger.OpenPnpMessanger(self.coords)
        self.openpnp.openPnpRequest.connect(self.executeRequestProlog)

        # Connection to the SmallSmt machine
        self.smallsmt = smallsmtmessanger.SmallSmtMessanger(serial)
        self.smallsmt.messageDone.connect(self.executeRequestEpilog,Qt.QueuedConnection)



    def logInfo(self,logText):
        self.openPnpLog.emit(logText)

    @pyqtSlot(str)
    def executeRequestProlog(self,command):
        if command.startswith("home("):
            self.cmd__home()
        elif command.startswith("moveTo("):
            self.cmd__moveTo(command)
        elif  command.startswith("setEnabled("):
            self.cmd__setEnabled(command)
        elif command.startswith("pick("):
            self.cmd__pick(command)
        elif command.startswith("place("):
            self.cmd__place(command)
        elif command.startswith("actuate("):
            self.cmd__actuate(command)
        elif command.startswith("actuateRead("):
            self.cmd__actuateRead(command)
        else:
            # The code comes here only in case of wrong command
            # Otherwise it is being processed in commands itself
            self.logInfo(str.format("Command unrecognized or not sent: {} ", command))
            self.openpnp.status = -1
            self.openpnp.executeResponse()

    @pyqtSlot(bool)
    def executeRequestEpilog(self, result):
        if result:
            self.openpnp.status = 0
        else:
            self.openpnp.status = -1
        self.openpnp.executeResponse()


    def cmd__home(self):
        self.openPnpLog.emit("EXE: home")
        self.smallsmt.prepare()
        self.smallsmt.add({"tout": 30000, "packet": smallsmtprotocol.SmallSmtCmd__Reset("XYZ1Z2W1W2W3")})
        self.smallsmt.send()

    def cmd__moveTo(self,command):
        cmd = openpnpcoords.OpenPnpCoordsSplitter(command)
        cmd.toMove()




        pass

    def cmd__actuate(self,command):
        pass

    def cmd__pick(self,command):
        pass

    def cmd__place(self,command):
        pass

    def cmd__setEnabled(self,command):

        self.openPnpLog.emit("EXE: setEnabled")
        self.smallsmt.prepare()
        self.smallsmt.add({"tout": 1000, "packet": smallsmtprotocol.SmallSmtCmd__Online()})
        self.smallsmt.add({"tout":  0, "packet": smallsmtprotocol.SmallSmtCmd__SmtMode(smallsmtprotocol.SmallSmtCmd__SmtMode.MODE_BEGIN)})
        self.smallsmt.send()

    def cmd__actuateRead(self,command):
        return 0






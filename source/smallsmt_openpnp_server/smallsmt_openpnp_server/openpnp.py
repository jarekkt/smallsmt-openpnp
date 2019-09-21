from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtCore import QObject,QEventLoop,QTimer,Qt
import commsockets
import smallsmtprotocol
import smallsmtmessanger
import openpnpmessanger


class OpenPnp(QObject):

    openPnpLog = pyqtSignal([str])

    def __init__(self,machine,serial):
        QObject.__init__(self)
        self.machine = machine

        self.openpnp = openpnpmessanger.OpenPnpMessanger()
        self.openpnp.openPnpRequest.connect(self.executeRequestProlog)

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
        pass

    def cmd__moveTo(self,command):
        pass

    def cmd__setEnabled(self,command):
        pass

    def cmd__actuate(self,command):
        pass

    def cmd__pick(self,command):
        pass

    def cmd__place(self,command):
        pass

    def cmd__setEnabled(self,command):

        self.openPnpLog.emit("Executing: setEnabled")
        self.smallsmt.prepare()
        self.smallsmt.add({"tout": 1000, "packet": smallsmtprotocol.SmallSmtCmd__Online()})
        self.smallsmt.send()

    def cmd__actuateRead(self,command):
        return 0






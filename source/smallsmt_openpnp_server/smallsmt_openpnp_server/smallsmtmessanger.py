from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtCore import QObject,QTimer,Qt

import smallsmtprotocol


class SmallSmtMessanger(QObject):

    SmallSmtMessangerLog = pyqtSignal([str])
    messageDone = pyqtSignal([bool])

    timer = QTimer()

    requests = []
    requests_id = 0
    timeout = 0

    def __init__(self,  serial):
        QObject.__init__(self)

        self.serial = serial
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.executeRequestTimeout,Qt.QueuedConnection)
        self.serial.getFromSmallSmt.connect(self.sendLoop, Qt.QueuedConnection)

    def logInfo(self, logText):
        self.SmallSmtMessangerLog.emit(logText)

    def prepare(self):
        self.requests.clear()
        self.requests_id = 0

    def add(self,item):
        self.requests.append(item)

    def send(self):
        # Triggers sending
        self.sendNextPacket()

    def sendNextPacket(self):
        packet = self.requests[self.self.requests_id]["packet"]
        self.timeout = self.requests[self.self.requests_id]["tout"]

        if not self.serial.sendToSmallSmt(packet.bytes):
            self.logInfo(str.format("Command sending error"))
            self.messageDone.emit(False)
        else:
            if self.timeout != 0:
                # Command with timeout - we assume response is expected
                self.timer.start(self.timeout)
            else:
                # Some commands do no provide response
                # We use small delay anyway
                self.timer.start(10)

    @pyqtSlot(bytearray)
    def sendLoop(self,in_bytes):
        self.timer.stop()
        # Preserve incoming packet
        self.requests[self.self.requests_id]["result_bytes"] = in_bytes
        self.self.requests_id = self.self.requests_id + 1
        if self.self.requests_id < len(self.requests):
            self.sendNextPacket()
        else:
            # All packages sent
            self.messageDone.emit(True)

    @pyqtSlot()
    def executeRequestTimeout(self):
        if self.timeout == 0:
            # This was packet without response - timeout as expected
            # Execute next request
            self.sendLoop(bytearray())
        else:
            # Unexpected timeout
            self.logInfo(str.format("Command timeout - no machine response"))
            self.messageDone.emit(False)

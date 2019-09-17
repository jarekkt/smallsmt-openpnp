from PyQt5.QtNetwork import QUdpSocket,QHostAddress,QNetworkDatagram
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
import sys

class CommSockets(QObject):
    SOCKET_NR_OUR   = 9070
    SOCKET_NR_THEIR = 9072

    getFromOpenPnp = pyqtSignal(str)

    def __init__(self):
        super(CommSockets, self).__init__()

        self.ourSocket = QUdpSocket(self)
        self.ourSocket.bind(QHostAddress.LocalHost, self.SOCKET_NR_OUR);

        self.theirSocket = QUdpSocket(self)
        self.ourSocket.readyRead.connect(self.readPendingDatagrams)

    def sendToOpenPnp(self,message):
        self.theirSocket.writeDatagram(message.encode('utf-8'),QHostAddress.LocalHost, self.SOCKET_NR_THEIR)

    def processDatagram(self,datagram):
        self.getFromOpenPnp.emit(str(datagram.data(), encoding='utf-8'))

    @pyqtSlot()
    def readPendingDatagrams(self):

        while(self.ourSocket.hasPendingDatagrams()):
            datagram = self.ourSocket.receiveDatagram()
            self.processDatagram(datagram)


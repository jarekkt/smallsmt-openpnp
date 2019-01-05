#include "commsockets.h"

int CommSockets::initSockets()
{

    ourSocket = new QUdpSocket(this);
    ourSocket->bind(QHostAddress::LocalHost, SOCKET_NR_OUR);

    theirSocket = new QUdpSocket(this);

    connect(ourSocket, SIGNAL(readyRead()),this, SLOT(readPendingDatagrams()));

    return 0;
}


void CommSockets::sendToOpenPnp(QString msg)
{
  theirSocket->writeDatagram(msg.toUtf8(), QHostAddress::LocalHost,SOCKET_NR_THEIR);
}


void CommSockets::readPendingDatagrams()
{
    while (ourSocket->hasPendingDatagrams())
    {
        QNetworkDatagram datagram = ourSocket->receiveDatagram();
        processTheDatagram(datagram);
    }
}

void CommSockets::processTheDatagram(QNetworkDatagram datagram)
{
    emit recevieLog(QString(datagram.data()));
    sendToOpenPnp("ok");
}


CommSockets::CommSockets()
{
    initSockets();
}

#ifndef COMMSOCKETS_H
#define COMMSOCKETS_H

#define SOCKET_NR_OUR   9070
#define SOCKET_NR_THEIR 9072

#include <QWidget>
#include <QUdpSocket>
#include <QNetworkDatagram>
#include <QString>




class CommSockets : public QObject
{
   Q_OBJECT

   QUdpSocket * ourSocket;
   QUdpSocket * theirSocket;

   int  initSockets();
   void processTheDatagram(QNetworkDatagram datagram);

private slots:

   void readPendingDatagrams();

signals:

   void recevieLog(QString log);
   void receiveFromOpenPnp(QString msg);

public:

    CommSockets();

public slots:

    void sendToOpenPnp(QString msg);

};

#endif // COMMSOCKETS_H

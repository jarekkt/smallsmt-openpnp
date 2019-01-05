#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    commSockets = new CommSockets();

    connect(commSockets, SIGNAL(recevieLog(QString)),this, SLOT(logMessages(QString)));
}


void MainWindow::logMessages(QString msg)
{
    ui->loggerWindow->appendPlainText(msg);
}


void MainWindow::enableComm()
{
    commSockets->sendToOpenPnp("Test\r\n");

}

MainWindow::~MainWindow()
{
    delete ui;
}

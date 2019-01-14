# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonDisconnect = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonDisconnect.setObjectName("pushButtonDisconnect")
        self.gridLayout.addWidget(self.pushButtonDisconnect, 1, 3, 1, 1)
        self.comboBoxSerialPorts = QtWidgets.QComboBox(self.centralWidget)
        self.comboBoxSerialPorts.setObjectName("comboBoxSerialPorts")
        self.gridLayout.addWidget(self.comboBoxSerialPorts, 1, 0, 1, 1)
        self.pushButtonConnect = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonConnect.setObjectName("pushButtonConnect")
        self.gridLayout.addWidget(self.pushButtonConnect, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.loggerWindow = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.loggerWindow.setObjectName("loggerWindow")
        self.verticalLayout.addWidget(self.loggerWindow)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.pushButtonConnect.clicked.connect(MainWindow.enableComm)
        self.pushButtonConnect.clicked.connect(MainWindow.disableComm)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SmallSmt Machine Server for OpenPnp"))
        self.pushButtonDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.pushButtonConnect.setText(_translate("MainWindow", "Connect"))


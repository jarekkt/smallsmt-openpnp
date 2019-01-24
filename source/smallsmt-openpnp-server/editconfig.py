# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editconfig.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EditConfig(object):
    def setupUi(self, EditConfig):
        EditConfig.setObjectName("EditConfig")
        EditConfig.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditConfig)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hLabel = QtWidgets.QLabel(EditConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.hLabel.setFont(font)
        self.hLabel.setObjectName("hLabel")
        self.verticalLayout.addWidget(self.hLabel)
        self.treeView = ConfigTreeView(EditConfig)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.buttonBox = QtWidgets.QDialogButtonBox(EditConfig)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EditConfig)
        self.buttonBox.accepted.connect(EditConfig.accept)
        self.buttonBox.rejected.connect(EditConfig.reject)
        QtCore.QMetaObject.connectSlotsByName(EditConfig)

    def retranslateUi(self, EditConfig):
        _translate = QtCore.QCoreApplication.translate
        EditConfig.setWindowTitle(_translate("EditConfig", "Modify settings"))
        self.hLabel.setText(_translate("EditConfig", "Configuration editor"))

from configtreeview import ConfigTreeView

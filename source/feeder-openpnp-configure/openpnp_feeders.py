

#  Author: jaroslaw.karwik@gmail.com

from PyQt5.QtWidgets import QApplication, QMainWindow,  QFileDialog, QAbstractItemView, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt

from optparse import OptionParser
from lxml import etree
from copy import deepcopy

import sys
import re
import shutil
import datetime


from feederwindow import Ui_MainWindow

class FeederApp(QMainWindow, Ui_MainWindow):


    def saveFile(self,fileName,rootNodes,backup):
        if fileName == "":
            return
        if backup:
            try:
                shutil.copy(fileName, fileName + "." + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M."))
            except:
                pass  # This is only best efort case. The file may not exist at all
        try:
            rootNodes.write(fileName)
        except:
            QMessageBox.warning(self, "Warning", str.format("The config file {} could not be written!",fileName))


    def loadFeeders(self,tableView,rootNodes):
        tableView.clear()
        tableView.setRowCount(0)
        if not rootNodes:
            return
        for e in rootNodes.iter():
            path = rootNodes.getpath(e)
            if re.fullmatch("\/openpnp-machine\/machine\/feeders\/feeder\[[0-9]+\]",path):
                txtId = e.get("id","Id?")
                txtName = e.get("name", "Name?")
                txtPartId = e.get("part-id", "PartId?")
                txtAttr = str(e.attrib)
                rowPosition = tableView.rowCount()
                tableView.insertRow(rowPosition)
                widget1 = QTableWidgetItem(txtId)
                widget1.setData(Qt.UserRole, path)
                widget1.setFlags(widget1.flags() ^ Qt.ItemIsEditable)
                tableView.setItem(rowPosition, 0, widget1)
                widget2 = QTableWidgetItem(txtName)
                widget2.setFlags(widget2.flags() ^ Qt.ItemIsEditable)
                tableView.setItem(rowPosition, 1, widget2)
                widget3 = QTableWidgetItem(txtPartId)
                widget3.setFlags(widget3.flags() ^ Qt.ItemIsEditable)
                tableView.setItem(rowPosition, 2, widget3)
                widget4 = QTableWidgetItem(txtAttr)
                widget4.setFlags(widget4.flags() ^ Qt.ItemIsEditable)
                tableView.setItem(rowPosition, 3, widget4)
        tableView.setHorizontalHeaderLabels(self.hlabels)

    def delSelected(self,tableView,rootNodes):
        rows = []
        for idx in tableView.selectionModel().selectedRows():
            row = idx.row()
            rows.append(row)
        # Need reverse order, otherwise indexs are messed when deleting items and
        # path are not valid anymore
        rows.sort(reverse=True)
        for row in rows:
            item = tableView.item(row,0)
            path = item.data(Qt.UserRole)
            nodes = rootNodes.xpath(path)
            for node in nodes:
                parent = node.getparent()
                parent.remove(node)
        self.loadFeeders(tableView,rootNodes)

    def copyFromTo(self,fromTV,fromNodes,toTV,toNodes):
        rows = []
        for idx in fromTV.selectionModel().selectedRows():
            row = idx.row()
            rows.append(row)
        rows.sort(reverse=False)
        for row in rows:
            item = fromTV.item(row, 0)
            path = item.data(Qt.UserRole)
            nodes = fromNodes.xpath(path)
            for node in nodes:
                fromparent = node.getparent()
                fromparentPath = fromNodes.getpath(fromparent)
                nodeCopy = deepcopy(node)
                toparents = toNodes.xpath(fromparentPath)
                if toparents:
                   toparent = toparents[0]
                   toparent.append(nodeCopy)
        self.loadFeeders(toTV, toNodes)

    @pyqtSlot()
    def loadLeft(self):
        self.leftFilePath, _ = QFileDialog.getOpenFileName(self, "Open File", self.leftXmlPath, "XML files (*.xml)")
        if self.leftFilePath:
            self.leftXmlPath = self.leftFilePath
            self.leftLE.setText(self.leftFilePath)
            with open(self.leftFilePath, 'rt') as f:
                self.rootLeft = etree.parse(f)
                self.loadFeeders(self.tableWidgetLeft,self.rootLeft)
        else:
            self.leftXmlPath = ""
            self.rootLeft = None



    @pyqtSlot()
    def loadRight(self):
        self.rightFilePath, _ = QFileDialog.getOpenFileName(self, "Open File",self.rightXmlPath, "XML files (*.xml)")
        if self.rightFilePath:
            self.rightXmlPath = self.rightFilePath
            self.rightLE.setText(self.rightFilePath)
            with open(self.rightFilePath, 'rt') as f:
                self.rootRight = etree.parse(f)
                self.loadFeeders(self.tableWidgetRight, self.rootRight)
        else:
            self.rightXmlPath = ""
            self.rootRight = None




    @pyqtSlot()
    def deleteLeft(self):
        self.delSelected(self.tableWidgetLeft,self.rootLeft)


    @pyqtSlot()
    def deleteRight(self):
        self.delSelected(self.tableWidgetRight,self.rootRight)

    @pyqtSlot()
    def copyLeft(self):
        if self.rootLeft and self.rootRight:
            self.copyFromTo(self.tableWidgetLeft, self.rootLeft, self.tableWidgetRight, self.rootRight)


    @pyqtSlot()
    def copyRight(self):
        if self.rootLeft and self.rootRight:
            self.copyFromTo(self.tableWidgetRight, self.rootRight, self.tableWidgetLeft, self.rootLeft)


    @pyqtSlot()
    def saveQuit(self):
        if self.rootLeft:
            self.saveFile(self.leftXmlPath,self.rootLeft,self.copyLeftCB.isChecked())
        if self.rootRight:
            self.saveFile(self.rightXmlPath, self.rootRight, self.copyRightCB.isChecked())
        self.close()

    @pyqtSlot()
    def quit(self):
        self.close()

    @pyqtSlot()
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.leftXmlPath = ""
        self.rootLeft = None
        self.rightXmlPath = ""
        self.rootRight = None
        self.hlabels = ["Id", "Name", "Part Id", "Feeder"]
        self.tableWidgetLeft.setHorizontalHeaderLabels(self.hlabels)
        self.tableWidgetLeft.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetLeft.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetLeft.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidgetRight.setHorizontalHeaderLabels(self.hlabels)
        self.tableWidgetRight.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetRight.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetRight.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

def main():
    parser = OptionParser()
    (options, args) = parser.parse_args(sys.argv)
    app = QApplication(sys.argv)
    form = FeederApp()
    form.show()
    app.exec()



if __name__ == '__main__':
    main()


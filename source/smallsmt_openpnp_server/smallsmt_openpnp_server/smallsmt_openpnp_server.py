from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot,QCoreApplication,QStandardPaths, QDirIterator, QDir,QFileInfo
from PyQt5.QtSerialPort import QSerialPortInfo
from optparse import OptionParser

import sys
import re
import os
import openpnp
import smallsmtconfig
import smallsmtprotocol
import configtreeview
import commserial

from mainwindow import Ui_MainWindow
from dialogplayground import Ui_DialogPlayground
from editconfig import Ui_EditConfig
from aboutdialog import Ui_AboutDialog

class About(QDialog, Ui_AboutDialog):
    def __init__(self):
        QDialog.__init__(self)
        Ui_AboutDialog.__init__(self)
        self.setupUi(self)


class Configure(QDialog, Ui_EditConfig):

    def __init__(self):
        QDialog.__init__(self)
        Ui_EditConfig.__init__(self)
        self.setupUi(self)
        self.configModel = configtreeview.ConfigModel()

    def setData(self,obj):
        self.configModel.putTreeData(obj)
        self.treeView.setModel(self.configModel)

    def getData(self):
        return  self.configModel.getTreeData()


class Playground(QDialog, Ui_DialogPlayground):

    def executePacket(self,packet):
        self.frameOutLE.setText(packet.toString())
        self.plainTextEdit.appendPlainText(packet.toString())
        self.frameInLE.clear()
        self.serial.sendToSmallSmt(packet.bytes)

    @pyqtSlot(bytearray)
    def receivePacket(self,msg):
        recvPacket = smallsmtprotocol.SmallSmtCmd_Response(msg)
        recvDecoded = recvPacket.toString()
        self.frameInLE.setText(recvDecoded)
        self.plainTextEdit.appendPlainText(recvDecoded)

    def parseHexHint(self,text):
        value_hex = re.match("\s*0x([a-fA-F0-9]*)\s*.*$", text)
        if value_hex:
            return int(value_hex.group(1),16)
        else:
            return 0

    def pbBaseOnline(self):
        packet = smallsmtprotocol.SmallSmtCmd__Online()
        self.executePacket(packet)

    def pbBaseReset(self):
        axes=""
        if self.xCB.isChecked():
            axes += "X"
        if self.yCB.isChecked():
            axes += "Y"
        if self.Z12CB.isChecked():
            axes += "Z1"
        if self.z34CB.isChecked():
            axes += "Z2"
        if self.w1CB.isChecked():
            axes += "W1"
        if self.w2CB.isChecked():
            axes += "W2"
        if self.w3CB.isChecked():
            axes += "W3"
        packet = smallsmtprotocol.SmallSmtCmd__Reset(axes)
        self.executePacket(packet)

    def pbBaseResetValves(self):
        if self.resetValueCBX.currentIndex() == 0:
            resetValue = self.rasetValveRawSB.value()
        else:
            resetValue = self.parseHexHint(self.resetValueCBX.currentText())
        packet = smallsmtprotocol.SmallSmtCmd__ResetValves(resetValue)
        self.executePacket(packet)

    def pbBaseSolenoid(self):
        if self.solenoidCBX.currentIndex() == 0:
            ioValue = self.solenoidSB.value()
        else:
            ioValue = self.parseHexHint(self.solenoidCBX.currentText())
        ioSet = self.solenoidEnableCB.isChecked()
        packet = smallsmtprotocol.SmallSmtCmd__Solenoid(ioValue,ioSet)
        self.executePacket(packet)

    def pbBaseCamera(self):
        camIdx = self.parseHexHint(self.camCBX.currentText())
        camBrightness = self.brightnessSX.value()
        packet = smallsmtprotocol.SmallSmtCmd__CameraMux(camIdx,camBrightness)
        self.executePacket(packet)

    def pbBaseSpeedCoeff(self):
        speedCoeff = self.speedSX.value()
        packet = smallsmtprotocol.SmallSmtCmd__SpeedCoefficient(speedCoeff)
        self.executePacket(packet)

    def pbBaseReadVacuum(self):
        vacIdx = self.parseHexHint(self.readVacuumCBX.currentText())
        packet = smallsmtprotocol.SmallSmtCmd__ReadVacum(vacIdx)
        self.executePacket(packet)

    def pbBaseSmtMode(self):
        vacIdx = self.parseHexHint(self.smtModeCBX.currentText())
        packet = smallsmtprotocol.SmallSmtCmd__SmtMode(vacIdx)
        self.executePacket(packet)

    def pbMoveAxis(self):
        steps = self.moveSteps.value()
        startSpeed = self.moveStartSpeed.value()
        runSpeed = self.moveRunSpeed.value()
        motor = self.parseHexHint(self.buttonGroup.checkedButton().text())
        packet = smallsmtprotocol.SmallSmtCmd__Move(motor,steps,startSpeed,runSpeed)
        self.executePacket(packet)
        pass

    def pbHeadMove(self):
        stepsX = self.hmStepsX.value()
        startSpeedX = self.hmSsX.value()
        runSpeedX = self.hmRsX.value()
        stepsY= self.hmStepsY.value()
        startSpeedY = self.hmSsY.value()
        runSpeedY= self.hmRsY.value()
        stepsA1 = self.hmStepsA1.value()
        startSpeedA1 = self.hmSsA1.value()
        runSpeedA1= self.hmRsA1.value()
        stepsA2 = self.hmStepsA2.value()
        startSpeedA2= self.hmSsA2.value()
        runSpeedA2= self.hmRsA2.value()
        stepsA3= self.hmStepsA3.value()
        startSpeedA3= self.hmSsA3.value()
        runSpeedA3= self.hmRsA3.value()
        stepsA4= self.hmStepsA4.value()
        startSpeedA4= self.hmSsA4.value()
        runSpeedA4= self.hmRsA4.value()
        returnEarly=self.waitCB.isChecked()
        packet = smallsmtprotocol.SmallSmtCmd__MultiMove(
            stepsX, startSpeedX, runSpeedX,
            stepsY, startSpeedY, runSpeedY,
            stepsA1, startSpeedA1, runSpeedA1,
            stepsA2, startSpeedA2, runSpeedA2,
            stepsA3, startSpeedA3, runSpeedA3,
            stepsA4, startSpeedA4, runSpeedA4,
            returnEarly)
        self.executePacket(packet)

    def pbFeeder(self):
        feederId = self.parseHexHint(self.feedersCBX.currentText())
        steps = self.fSteps.value()
        startupSpeed = self.fSs.value()
        runSpeed = self.fRs.value()
        openLength = self.fOl.value()
        closedLength = self.fCl.value()
        ocStartSpeed = self.ocSs.value()
        ocRunSpeed = self.ocRs.value()
        feedTime = self.fFt.value()
        pushCount = self.fPc.value()
        unknown = self.flast.value()
        packet = smallsmtprotocol.SmallSmtCmd__FeederControl(
            feederId,steps, startupSpeed, runSpeed,
            openLength, closedLength, ocStartSpeed, ocRunSpeed,
            feedTime,pushCount,unknown
        )
        self.executePacket(packet)


    def pbClFeeder(self):
        feederId = self.fCli.value()
        feederTime = self.fClt.value()
        packet = smallsmtprotocol.SmallSmtCmd__FeederControlYamaha(feederId,feederTime)
        self.executePacket(packet)

    def pbPick(self):
        zAxis = self.parseHexHint(self.pickAxeCBX.currentText())
        steps = self.piZ.value()
        startSpeed = self.piSs.value()
        runSpeed = self.piRs.value()
        nozzleId = self.piN.value()
        putDelay = self.piPd.value()
        vacuumTestLvl = self.piVtl.value()
        packet = smallsmtprotocol.SmallSmtCmd__Pick(zAxis,startSpeed,runSpeed,steps,nozzleId,putDelay,vacuumTestLvl)
        self.executePacket(packet)

    def pbPlace(self):
        zAxis = self.parseHexHint(self.placeAxeCBX.currentText())
        steps = self.plZ.value()
        startSpeed = self.plSs.value()
        runSpeed = self.plRs.value()
        stepsVacShut = self.plZsvs.value()
        putDelay = self.plPd.value()
        vacuumTestLvl = self.plVtl.value()
        packet = smallsmtprotocol.SmallSmtCmd__Place(zAxis,startSpeed,runSpeed,steps,stepsVacShut,putDelay,vacuumTestLvl)
        self.executePacket(packet)



    def __init__(self,serial):
        QDialog.__init__(self)
        Ui_DialogPlayground.__init__(self)
        self.setupUi(self)
        self.serial = serial
        self.serial.getFromSmallSmt.connect(self.receivePacket)


class SmallSmtDriverApp(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.smallSmtMachine = smallsmtconfig.SmallSmtConfig()
        self.smallSmtMachine.smallSmtLog.connect(self.logMessages)
        self.listPorts()
        self.serial = commserial.CommSerial()
        self.openPnp = openpnp.OpenPnp(self.smallSmtMachine,self.serial)
        self.openPnp.openPnpLog.connect(self.logMessages)

        self.dataProgramDir = os.path.dirname(__file__)
        self.dataConfigDir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        # Make sure our data path exists
        os.makedirs(self.dataConfigDir,exist_ok=True)


        self.actionPlayground.setEnabled(False)
        self.statusBar.showMessage(QCoreApplication.translate("App","Connect to machine serial port first"))

    def listPorts(self):
        available_ports = QSerialPortInfo.availablePorts()
        self.comboBoxSerialPorts.clear()
        for port in available_ports:
            self.comboBoxSerialPorts.addItem(port.portName())

    def updateFileNames(self):
        self.fileNameGlobal = os.path.join(self.dataConfigDir, self.machineTypesCB.currentText() + ".machine.json")
        self.fileNameGlobalDefault = os.path.join(self.dataProgramDir, self.machineTypesCB.currentText() + ".machine.json")
        self.fileNameCalibrationFile = os.path.join(self.dataConfigDir, self.machineConfigCB.currentText() + ".cfg.json")

    def configure(self,machineType,machineConfig,machinePort,machineStart):
        it = QDirIterator(self.dataConfigDir, ['*.cfg.json'])
        while it.hasNext():
            fileInfo = QFileInfo(it.next())
            basename = fileInfo.baseName()
            self.machineConfigCB.addItem(basename)

        self.reloadSettings()

    @pyqtSlot(str)
    def logMessages(self,msg):
        self.loggerWindow.appendPlainText(msg)

    @pyqtSlot()
    def enableComm(self):
        if self.serial.opened == True:
            self.actionPlayground.setEnabled(False)
            self.serial.disable()
            self.pushButtonConnect.setText(QCoreApplication.translate("App","Connect"))
        else:
            if self.serial.enable(self.comboBoxSerialPorts.currentText()) == True:
                self.pushButtonConnect.setText(QCoreApplication.translate("App","Disonnect"))
                self.logMessages(QCoreApplication.translate("App","Opening serial port succeded"))
                self.actionPlayground.setEnabled(True)
                self.statusBar.showMessage(str.format("App","Connected to {}",self.comboBoxSerialPorts.currentText()))
            else:
                self.logMessages(QCoreApplication.translate("App","Opening serial port failed!"))
                self.statusBar.showMessage(QCoreApplication.translate("App","Disconnected"))

    @pyqtSlot()
    def configGlobal(self):
        configDia = Configure()
        configDia.setData(self.smallSmtMachine.globalConfig)
        if configDia.exec() == QDialog.Accepted :
            self.smallSmtMachine.globalConfig = configDia.getData()

    @pyqtSlot()
    def configMachine(self):
        configDia = Configure()
        configDia.setData(self.smallSmtMachine.machineConfig)
        if configDia.exec() == QDialog.Accepted :
            self.smallSmtMachine.machineConfig = configDia.getData()

    @pyqtSlot()
    def reloadSettings(self):
        self.updateFileNames()
        self.smallSmtMachine.loadMachineData(self.fileNameGlobal,self.fileNameGlobalDefault,self.fileNameCalibrationFile)

    @pyqtSlot()
    def saveSettings(self):
        self.updateFileNames()
        if not self.smallSmtMachine.is_valid(self.fileNameCalibrationFile):
            QMessageBox.warning(self, QCoreApplication.translate("App","Warning"), QCoreApplication.translate("App","The machine configuration file name is not valid - creating default!"))
        self.smallSmtMachine.saveCalibrationMachineData(self.fileNameCalibrationFile)
        if self.machineConfigCB.findText(self.machineConfigCB.currentText()) == -1:
            self.machineConfigCB.addItem(self.machineConfigCB.currentText())

        if not self.smallSmtMachine.is_valid(self.fileNameGlobal):
            QMessageBox.warning(self, QCoreApplication.translate("App", "Warning"), QCoreApplication.translate("App", "The machine global configuration file name is not valid - creating default!"))
        self.smallSmtMachine.saveGlobalMachineData(self.fileNameGlobal)



    @pyqtSlot()
    def playground(self):
        configPlay = Playground(self.serial)
        configPlay.exec()


    @pyqtSlot()
    def refreshPort(self):
        self.listPorts()

    @pyqtSlot()
    def about(self):
        aboutDia = About()
        aboutDia.exec()
        pass


def main():
    parser = OptionParser()

    parser.add_option('-t', help='Machine type', dest='machineType',action ='store')
    parser.add_option('-c', help='Machine config file', dest='machineConfig', action='store')
    parser.add_option('-p', help='Controller port name', dest='machineSerialPort', action='store')
    parser.add_option('-s', help='Connect to port and start server', dest='machineStart', default = False, action = 'store_true')
    (options, args) = parser.parse_args(sys.argv)

    app = QApplication(sys.argv)
    app.setApplicationName('smallsmt_openpnp_server')
    form = SmallSmtDriverApp()
    form.show()
    form.configure(options.machineType,options.machineConfig,options.machineSerialPort,options.machineStart)
    app.exec()


if __name__ == '__main__':
    main()

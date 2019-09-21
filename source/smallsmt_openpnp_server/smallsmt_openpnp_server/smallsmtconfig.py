from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QObject,QFileInfo


import machineconfig
import configtreeview


class SmallSmtConfig(QObject, configtreeview.ConfigSaver):

    smallSmtLog = pyqtSignal([str])

    def __init__(self):
        QObject.__init__(self)
        self.globalConfig = machineconfig.GlobalConfig()
        self.machineConfig = machineconfig.MachineConfig()


    def logInfo(self,logText):
        self.smallSmtLog.emit(logText)

    def loadMachineData(self,globalFileName,globalFileDefault,configFileName):
        result = True
        try:
            self.globalConfig = self.load(globalFileName)
            self.logInfo(str.format("Loading global machine configuration from '{}'",QFileInfo(globalFileName).baseName()))
        except:
            self.logInfo("Loading global config failed - lets try default file")
            try:
                self.globalConfig = self.load(globalFileDefault)
                self.logInfo(str.format("Loading global machine configuration from '{}'", QFileInfo(globalFileDefault).baseName()))
            except:
                self.logInfo("No default file found")
                result = False

        try:
            self.machineConfig = self.load(configFileName)
            self.logInfo(str.format("Loading machine calibration  from '{}'", QFileInfo(configFileName).baseName()))
        except:
            self.logInfo("Loading machine config failed")
            result = False

        return result

    def saveGlobalMachineData(self,globalFileName):
        try:
            self.save(globalFileName, self.globalConfig, True)
            self.logInfo(str.format("Saved global configuration file to '{}'", QFileInfo(globalFileName).baseName()))
        except:
            self.logInfo("Saving machine global config failed.")

    def saveCalibrationMachineData(self,configFileName):
        try:
            self.save(configFileName,self.machineConfig,True)
            self.logInfo(str.format("Saved local configuration file to '{}'", QFileInfo(configFileName).baseName()))
        except:
            self.logInfo("Saving machine calibration data failed.")

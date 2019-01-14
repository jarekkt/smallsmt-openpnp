from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtCore import QObject,QSettings
import commserial

class CoordPair:
    def __init__(self):
        self.distMm = 0
        self.distPulse = 0
        self.cnvPulse2mm = 1
    def getMm(self):
        return self.distMm
    def getPulse(self):
        return self.distPulse
    def getCnvPulse2mm(self):
        return self.cnvPulse2mm
    def setMm(self,val):
        self.distMm = val
        self.distPulse = val/self.cnvPulse2mm
    def setPulse(self, val):
        self.distPulse = val
        self.distMm = val * self.cnvPulse2mm
    def setCnvPulse2mm(self,val):
        self.cnvPulse2mm = val
    def clear(self):
        self.distMm = 0
        self.distPulse = 0
        self.cnvPulse2mm = 1

class SmallSmt(QObject):

    INI_FILE = "machine_global.ini"

    # Base coordinates
    X = CoordPair()
    Y = CoordPair()

    # Heads
    Z1 = CoordPair()
    C1 = CoordPair()
    Z2 = CoordPair()
    C2 = CoordPair()
    Z3 = CoordPair()
    C3 = CoordPair()
    Z4 = CoordPair()
    C4 = CoordPair()

    # Feeders
    W1West = CoordPair()
    W2North = CoordPair()
    W3East = CoordPair()
    W4South = CoordPair()

    def loadMachineConfig(self):
        initFile = QSettings(self.INI_FILE, QSettings.IniFormat)

        self.machineType = initFile.value("main/type","VP2000S")
        self.machineSection = self.machineType + "_config"
        self.machineLocalIni = initFile.value("main/mine",self.machineType +"_mine.ini")

        # Common part for all machines, although some have less heads
        self.X.setCnvPulse2mm(initFile.value(self.machineSection + "/X_pulseCnv",1))
        self.Y.setCnvPulse2mm(initFile.value(self.machineSection + "/Y_pulseCnv", 1))
        self.Z1.setCnvPulse2mm(initFile.value(self.machineSection + "/Z1_pulseCnv", 1))
        self.C1.setCnvPulse2mm(initFile.value(self.machineSection + "/C1_pulseCnv", 1))
        self.Z2.setCnvPulse2mm(initFile.value(self.machineSection + "/Z2_pulseCnv", 1))
        self.C2.setCnvPulse2mm(initFile.value(self.machineSection + "/C2_pulseCnv", 1))
        self.Z3.setCnvPulse2mm(initFile.value(self.machineSection + "/Z3_pulseCnv", 1))
        self.C3.setCnvPulse2mm(initFile.value(self.machineSection + "/C3_pulseCnv", 1))
        self.Z4.setCnvPulse2mm(initFile.value(self.machineSection + "/Z4_pulseCnv", 1))
        self.C4.setCnvPulse2mm(initFile.value(self.machineSection + "/C4_pulseCnv", 1))

        # This is only for machines with automatic feeders
        # Controls steppers which move pneumatic actuator
        self.W1West.setCnvPulse2mm(initFile.value(self.machineSection + "/W1West_pulseCnv", 1))
        self.W2North.setCnvPulse2mm(initFile.value(self.machineSection + "/W2North_pulseCnv", 1))
        self.W3East.setCnvPulse2mm(initFile.value(self.machineSection + "/W3East_pulseCnv", 1))
        self.W4South.setCnvPulse2mm(initFile.value(self.machineSection + "/W4South_pulseCnv", 1))

        initFile = QSettings(self.machineLocalIni, QSettings.IniFormat)

        #
        #   TODO - do not have acces to such machine
        #

    def saveMachineConfig(self):
        initFile = QSettings(self.INI_FILE, QSettings.IniFormat)

        initFile.setValue(self.machineSection + "/X_pulseCnv",self.X.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/Y_pulseCnv",self.Y.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/Z1_pulseCnv",self.Z1.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/C1_pulseCnv",self.C1.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/Z2_pulseCnv",self.Z2.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/C2_pulseCnv",self.C2.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/Z3_pulseCnv",self.Z3.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/C3_pulseCnv",self.C3.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/Z4_pulseCnv",self.Z4.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/C4_pulseCnv",self.C4.getCnvPulse2mm())

        # This is only for machines with automatic feeders
        initFile.setValue(self.machineSection + "/W1West_pulseCnv",self.W1West.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/W2North_pulseCnv",self.W2North.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/W3East_pulseCnv",self.W3East.getCnvPulse2mm())
        initFile.setValue(self.machineSection + "/W4South_pulseCnv",self.W4South.getCnvPulse2mm())


    def initializeClean(self):
        self.X.clear()
        self.Y.clear()
        self.Z1.clear()
        self.C1.clear()
        self.Z2.clear()
        self.C2.clear()
        self.Z3.clear()
        self.C3.clear()
        self.Z4.clear()
        self.C4.clear()
        self.W1West.clear()
        self.W2North.clear()
        self.W3East.clear()
        self.W4South.clear()
        self.loadMachineConfig()


    def __init__(self):
        QObject.__init__(self)
        self.initializeClean()




from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtCore import QObject


import jsonpickle
import shutil
import datetime

import commserial


def class_mapper(d):
    for keys, cls in mapping.items():
        if keys.issuperset(d.keys()):
            return cls(**d)
    else:
        # Raise exception instead of silently returning None
        raise ValueError('Unable to find a matching class for object: {!s}'.format(d))


class CoordInfo:

    def setPosMm(self,mm):
        pass

    def home(self,mm):
        pass

    def __init__(self):
        self.pulse = 0
        self.cnvPulse2mm = 1
        self.min = float('nan')
        self.max = float('nan')



class SmallSmtMachine:


    def __init__(self):
        # Base coordinates
        self.X = CoordInfo()
        self.Y = CoordInfo()

        # Heads
        self.Z1 = CoordInfo()
        self.C1 = CoordInfo()
        self.Z2 = CoordInfo()
        self.C2 = CoordInfo()
        self.Z3 = CoordInfo()
        self.C3 = CoordInfo()
        self.Z4 = CoordInfo()
        self.C4 = CoordInfo()

        # Feeders
        self.W1West = CoordInfo()
        self.W2North = CoordInfo()
        self.W3East = CoordInfo()
        self.W4South = CoordInfo()

    def write(self):
        with open("smt_file.json", "w") as write_file:
            jsonpickle.dumps(self,write_file)
            #json.dump(self, write_file,sort_keys=True, indent=4,default=lambda x: x.__dict__)
    def read(self):
        with open("smt_file.json", "r") as read_file:
            self = jsonpickle.load(read_file)


class SmallSmt(QObject):

    def saveMachineConfig(self,machine_calibration_file):
        shutil.copy(machine_calibration_file, machine_calibration_file + "." + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M."))
        with open("data_file.json", "w") as write_file:
            json.dump(self.config, write_file,sort_keys=True, indent=4)

    def initializeClean(self):
        pass

    def __init__(self):
        QObject.__init__(self)
        self.machine = SmallSmtMachine()
        self.machine2 =SmallSmtMachine()

        self.machine.C1.max = 5
        self.machine.write()
        self.machine2.read()

        pass
        #with open(machine_type_file, "r") as read_file:
        #    self.machine = json.load(read_file)
        #with open(machine_calibration_file, "r") as read_file:
        #    self.config = json.load(read_file)






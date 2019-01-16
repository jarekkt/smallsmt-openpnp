from PyQt5 import QtWidgets, QtCore
import configtreeview

import jsonpickle
import json

class CoordInfo:

    def setPosMm(self,mm):
        pass

    def home(self,mm):
        pass

    def __init__(self):
        self.pulse_i = 0
        self.cnvPulse2mm_f = 1
        self.min_f = float('nan')
        self.max_f = float('nan')


class CoordDInfo:
    def __init__(self):
        self.gg = CoordInfo()

class Master :
    uu = 6
    def __init__(self):
        self.aa_c = CoordInfo()
        self.hh = 8
        self.pp = CoordDInfo()
        self.ar = [CoordInfo(),CoordInfo(),CoordInfo()]

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    view = configtreeview.ConfigTreeView()
    model = configtreeview.ConfigModel()
    mm = Master()
    model.putTreeData(mm)
    view.setModel(model)

    view.show()
    view.resize(500, 300)
    app.exec_()

    res = model.getTreeData()
    print(res)
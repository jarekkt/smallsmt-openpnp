from PyQt5 import QtWidgets, QtCore
import configtreeview
from PyQt5.QtCore import pyqtSlot

import jsonpickle
import json
import sys

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


class TestModel(configtreeview.ConfigModel):
    def __init__(self,parent = None):
        super(TestModel, self).__init__(parent)


class TestView(configtreeview.ConfigTreeView):
    def __init__(self,parent = None):
        super(TestView,self).__init__(parent)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
   #     self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def setModel(self, model):
        super(TestView, self).setModel(model)
        self.setCurrentIndex(self.model().index(0, 0))
        self.selectionModel().selectionChanged.connect(self.store_current_selection)
        self.activated.connect(self.store_activation)

    @pyqtSlot("QItemSelection, QItemSelection","QItemSelection")
    def store_current_selection(self,selected,deselected):
        print("hello sel")
        for index in selected.indexes():
            print(self.model().data(index, QtCore.Qt.DisplayRole))
            next = index.parent()
            if next.column() !=0:
                print(self.model().data(next, QtCore.Qt.DisplayRole))
                next = next.parent()
                if next.column() !=0:
                    print(self.model().data(next, QtCore.Qt.DisplayRole))
                    next = next.parent()
                    if next.column() !=0:
                        print(self.model().data(next, QtCore.Qt.DisplayRole))

    @pyqtSlot("QModelIndex")
    def store_activation(self, activated):
        print("hello act")
        print(self.model().data(activated, QtCore.Qt.DisplayRole))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = TestView()
    model = TestModel()
    mm = Master()
    model.putTreeData(mm)
    view.setModel(model)

    view.show()
    view.resize(500, 300)
    app.exec_()

    res = model.getTreeData()
    print(res)

    cfg = configtreeview.ConfigSaver()
    cfg.save("mycfg.json",res)

    res_clone = cfg.load("mycfg.json")
    print(res_clone)

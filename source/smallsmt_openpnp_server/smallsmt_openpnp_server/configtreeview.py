# Adaptation of https://github.com/dridk/QJsonModel/blob/master/qjsonmodel.py


from PyQt5 import QtWidgets, QtCore

import jsonpickle
import json
import re
import shutil
import datetime
import os

class QJsonTreeItem(object):
    def __init__(self, parent=None):
        self._parent = parent

        self._key = ""
        self._value = ""
        self._type = None
        self._children = list()

    def appendChild(self, item):
        self._children.append(item)

    def child(self, row):
        return self._children[row]

    def parent(self):
        return self._parent

    def childCount(self):
        return len(self._children)

    def row(self):
        return (
            self._parent._children.index(self)
            if self._parent else 0
        )

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, typ):
        self._type = typ

    @classmethod
    def load(self, value, parent=None, sort=True):
        rootItem = QJsonTreeItem(parent)
        rootItem.key = "root"

        if isinstance(value, dict):
            items = (
                sorted(value.items())
                if sort else value.items()
            )

            for key, value in items:
                child = self.load(value, rootItem)
                child.key = key
                child.type = type(value)
                rootItem.appendChild(child)

        elif isinstance(value, list):
            for index, value in enumerate(value):
                child = self.load(value, rootItem)
                child.key = str(index)
                child.type = type(value)
                rootItem.appendChild(child)

        else:
            rootItem.value = value
            rootItem.type = type(value)

        return rootItem


class QJsonModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(QJsonModel, self).__init__(parent)

        self._rootItem = QJsonTreeItem()
        self._headers = ("Variable", "Value")

    def load(self, document):
        """Load from dictionary
        Arguments:
            document (dict): JSON-compatible dictionary
        """

        assert isinstance(document, (dict, list, tuple)), (
            "`document` must be of dict, list or tuple, "
            "not %s" % type(document)
        )

        self.beginResetModel()

        self._rootItem = QJsonTreeItem.load(document)
        self._rootItem.type = type(document)

        self.endResetModel()

        return True

    def json(self, root=None):
        """Serialise model as JSON-compliant dictionary
        Arguments:
            root (QJsonTreeItem, optional): Serialise from here
                defaults to the the top-level item
        Returns:
            model as dict
        """

        root = root or self._rootItem
        return self.genJson(root)

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                # Remove our type formatting
                fkey = re.sub(r"_.*", "", item.key)
                return fkey
            if index.column() == 1:
                return item.value
        if role == QtCore.Qt.UserRole:
            if index.column() == 0:
                return item.key
            if index.column() == 1:
                return item.value
        elif role == QtCore.Qt.EditRole:
            # Gives pure unmodified values from model
            if index.column() == 1:
                return item.value

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            if index.column() == 1:
                item = index.internalPointer()

                key_idx = index.siblingAtColumn(index.column() - 1)
                key_val = key_idx.data(QtCore.Qt.UserRole)
                key_type = re.match("(?:.*)_(.*)(\\d)$", key_val)

                if key_type:
                    if key_type.group(1) == "f":
                        item.value = float(value)
                    else:
                        item.value = str(value)
                else:
                    item.value = str(value)

                self.dataChanged.emit(index, index, [QtCore.Qt.EditRole])
                return True

        return False

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            return self._headers[section]

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def flags(self, index):
        flags = super(QJsonModel, self).flags(index)

        if index.column() == 1:
            return QtCore.Qt.ItemIsEditable | flags
        else:
            return flags

    def genJson(self, item):
        nchild = item.childCount()

        if item.type is dict:
            document = {}
            for i in range(nchild):
                ch = item.child(i)
                document[ch.key] = self.genJson(ch)
            return document

        elif item.type == list:
            document = []
            for i in range(nchild):
                ch = item.child(i)
                document.append(self.genJson(ch))
            return document

        else:
            return item.value

class Delegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        key_idx = index.siblingAtColumn(index.column()-1)
        key_val = key_idx.data(QtCore.Qt.UserRole)
        key_type = re.match("(?:.*)_(.*)(\\d)$",key_val)

        if key_type:
            if key_type.group(1) == "f":
                editor = QtWidgets.QDoubleSpinBox(parent)
                if key_type.group(2):
                    editor.setDecimals(int(key_type.group(2)))
                else:
                    editor.setDecimals(4)
            else:
                editor = QtWidgets.QLineEdit(parent)
        else:
            editor = QtWidgets.QLineEdit(parent)
        return editor

class ConfigTreeView(QtWidgets.QTreeView):
    def __init__(self,parent = None):
        super(ConfigTreeView,self).__init__(parent)
        self.setItemDelegate(Delegate())

class ConfigModel(QtCore.QSortFilterProxyModel):
    def __init__(self,parent = None):
        super(ConfigModel,self).__init__(parent)
        self.setFilterRegExp(QtCore.QRegExp("^(?:(?!py/object).)*$"))
        self.setFilterKeyColumn(0)
        self.model = QJsonModel()
        self.setSourceModel(self.model)

    def putTreeData(self,myObject):
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=False, indent=4)
        self.jp = jsonpickle.encode(myObject)
        self.document = json.loads(self.jp)
        self.model.load(self.document)

    def getTreeData(self):
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('jason', sort_keys=False, indent=4)
        json_dump = json.dumps(self.model.json())
        return jsonpickle.decode(json_dump)


class ConfigSaver:
    def __init__(self):
        pass
    def save(self,fileName,myObject,make_backup=False):
        if make_backup == True :
            try:
                shutil.copy(fileName, fileName + "." + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M."))
            except:
                pass # This is only best efort case. The file may not exist at all
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=False, indent=4)
        with open(fileName, 'w') as outfile:
            json_obj = jsonpickle.encode(myObject)
            outfile.write(json_obj)
    def load(self,fileName):
        jsonpickle.set_preferred_backend('json')
        with open(fileName, 'r') as infile:
            json_str = infile.read()
            return jsonpickle.decode(json_str)

    def is_valid(self,fname):
        valid = False

        if os.path.exists(fname):
            valid = True
        else:
            try:
                f = open(fname, 'w')
                f.close()
                valid = True
            except OSError:
                pass
        return valid
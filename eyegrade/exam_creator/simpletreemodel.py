#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

        if parent is not None:
            self.parentItem.appendChild(self)

    def appendChild(self, child):
        self.childItems.append(child)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"

        output += "|-----" + ', '.join(self.itemData) + "\n"

        for child in self.childItems:
            output += child.log(tabLevel)

        tabLevel -= 1
        return output

    def __repr__(self):
        return "%s\n" \
               "\t-columnCount: %s\n" \
               "\t-childCount: %s\n" \
               "%s" % (self.__class__,
                           self.columnCount(),
                           self.childCount(),
                           self.log(0))

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(('Column #1', 'Column #2', 'Column #3', 'Column #4'))
        self.setupModelData()

    def setupModelData(self):
        c1 = TreeItem(('A', 'B', 'C'), self.rootItem)
        c2 = TreeItem(('A'), self.rootItem)
        c11 = TreeItem(('AA', 'BB', 'CC', 'DD'), c1)
        c12 = TreeItem(('AAA', 'BBB'), c1)
        c111 = TreeItem(('a', 'b', 'c', 'd', 'e'), c11)
        c1111 = TreeItem(('a', 'b', 'c', 'd', 'e'), c111)
        c1112 = TreeItem(('a', 'b', 'c', 'd', 'e'), c111)
        c11111 = TreeItem(('a', 'b', 'c', 'd', 'e'), c1111)
        c11112 = TreeItem(('a', 'b', 'c', 'd', 'e'), c1111)
        print self.rootItem

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
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
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)


if __name__ == '__main__':
    class Dialog(QtGui.QDialog):
        def __init__(self, parent=None):
            super(Dialog, self).__init__(parent)
            self.initUI()

        def initUI(self):
            model = TreeModel(('DATA'))
            self.view = QtGui.QTreeView(self)
            self.view.setModel(model)
            self.view.setWindowTitle('Simple Tree Model')
            self.view.setGeometry(10, 10, 400, 300)
            self.setGeometry(300, 300, 420, 320)
            print model.rootItem


    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())

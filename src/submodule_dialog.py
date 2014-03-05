# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'


from PyQt4 import QtCore, QtGui


class SubmoduleDialog(QtGui.QDialog):
    def __init__(self, submodules:list, parent:QtGui.QWidget=None):
        super().__init__(parent)

        self._submodules_list = QtGui.QListWidget(self)
        self._submodules_list.addItems(submodules)
        self._submodules_list.itemDoubleClicked.connect(self.accept)

        self._submodules_list.setCurrentRow(0)

        self._buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
                                               QtCore.Qt.Horizontal,
                                               self)

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._submodules_list)
        layout.addWidget(self._buttons)
        self.setLayout(layout)

    def submodule(self):
        return self._submodules_list.currentItem().text()

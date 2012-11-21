# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import commites_model

class CommitesWidget(QtGui.QWidget):
    def __init__(self, path, parent = None):
        super(CommitesWidget, self).__init__(parent)

        self._table = QtGui.QTreeView(self)
        self._table.setRootIsDecorated(False)

        self._model = commites_model.CommitesModel(path, self)
        self._table.setModel(self._model)

        selection_model = self._table.selectionModel()
        selection_model.selectionChanged.connect(self._current_index_changed)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._table)
        super(CommitesWidget, self).setLayout(layout)

    def _current_index_changed(self, current, previous):
        print("!!!")

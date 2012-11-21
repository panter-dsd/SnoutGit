# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtGui
import commites_model

class CommitesWidget(QtGui.QWidget):
    def __init__(self, path, parent = None):
        super(CommitesWidget, self).__init__(parent)

        self._table = QtGui.QTableView(self)

        self._model = commites_model.CommitesModel(path, self)
        self._table.setModel(self._model)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._table)
        super(CommitesWidget, self).setLayout(layout)

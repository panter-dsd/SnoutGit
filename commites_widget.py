# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import commites_model

class CommitesWidget(QtGui.QWidget):
    current_commit_changed = QtCore.Signal(str)

    def __init__(self, path, parent = None):
        super(CommitesWidget, self).__init__(parent)

        self._table = QtGui.QTreeView(self)
        self._table.setRootIsDecorated(False)

        self._model = commites_model.CommitesModel(path, self)
        self._table.setModel(self._model)

        selection_model = self._table.selectionModel()
        selection_model.currentChanged.connect(self._current_index_changed)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._table)
        super(CommitesWidget, self).setLayout(layout)

    def _current_index_changed(self, current, previous):
        commit_id = self._model.index(current.row(), 0).data(QtCore.Qt.DisplayRole)
        self.current_commit_changed.emit(commit_id)

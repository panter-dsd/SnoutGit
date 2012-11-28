# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import commites_model


DEFAULT_COLUMN_WIDTH = [0, 300, 0]


class CommitesWidget(QtGui.QWidget):
    current_commit_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(CommitesWidget, self).__init__(parent)

        self._table = QtGui.QTreeView(self)
        self._table.setRootIsDecorated(False)

        self._model = commites_model.CommitesModel(self)
        self._table.setModel(self._model)

        for i in range(len(DEFAULT_COLUMN_WIDTH)):
            self._table.setColumnWidth(i, DEFAULT_COLUMN_WIDTH[i])

        self._table.resizeColumnToContents(0)

        selection_model = self._table.selectionModel()
        selection_model.currentChanged.connect(self._current_index_changed)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._table)
        super(CommitesWidget, self).setLayout(layout)

    def _current_index_changed(self, current, _previous):
        index = self._model.index(current.row(), 0)
        commit_id = index.data(QtCore.Qt.DisplayRole)
        self.current_commit_changed.emit(commit_id)

    @QtCore.Slot(str)
    def update_commites_list(self):
        self._model.update_commits_list()

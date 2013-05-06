# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import commites_model
import add_tag_dialog
from git import Git

DEFAULT_COLUMN_WIDTH = [0, 300, 200, 0]


class CommitesWidget(QtGui.QWidget):
    current_commit_changed = QtCore.pyqtSignal(str)

    def __init__(self, git=Git(), parent=None):
        super(CommitesWidget, self).__init__(parent)

        self._table = QtGui.QTreeView(self)
        self._table.setRootIsDecorated(False)
        self._table.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self._model = commites_model.CommitesModel(git, self)
        self._table.setModel(self._model)

        for i in range(len(DEFAULT_COLUMN_WIDTH)):
            self._table.setColumnWidth(i, DEFAULT_COLUMN_WIDTH[i])

        self._table.resizeColumnToContents(0)

        selection_model = self._table.selectionModel()
        selection_model.currentChanged.connect(self._current_index_changed)

        self._add_tag_action = QtGui.QAction(self)
        self._add_tag_action.setText("Add tag")
        self._add_tag_action.triggered.connect(self._add_tag)
        self._table.addAction(self._add_tag_action)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._table)
        super(CommitesWidget, self).setLayout(layout)

    def _current_index_changed(self, current, _previous):
        index = self._model.index(current.row(), 0)
        commit_id = index.data(QtCore.Qt.DisplayRole)
        self.current_commit_changed.emit(commit_id)

    @QtCore.pyqtSlot()
    def update_commites_list(self):
        self._model.update_commits_list()

    def _add_tag(self):
        index = self._model.index(self._table.currentIndex().row(), 0)
        commit_id = index.data(QtCore.Qt.DisplayRole)
        d = add_tag_dialog.AddTagDialog(commit_id, self)
        if d.exec_():
            self.update_commites_list()

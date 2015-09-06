# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QAction, QHBoxLayout, QTreeView, QWidget

import commites_model
import add_tag_dialog

from git import Git

DEFAULT_COLUMN_WIDTH = [0, 300, 200, 0]


class CommitesWidget(QWidget):
    current_commit_changed = pyqtSignal(str)

    def __init__(self, commites_model, parent=None):
        super(CommitesWidget, self).__init__(parent)

        self._table = QTreeView(self)
        self._table.setRootIsDecorated(False)
        self._table.setContextMenuPolicy(Qt.ActionsContextMenu)

        self._commites_model = commites_model
        self._table.setModel(self._commites_model)

        for i in range(len(DEFAULT_COLUMN_WIDTH)):
            self._table.setColumnWidth(i, DEFAULT_COLUMN_WIDTH[i])

        self._table.resizeColumnToContents(0)

        selection_model = self._table.selectionModel()
        selection_model.currentChanged.connect(self._current_index_changed)

        self._add_tag_action = QAction(self)
        self._add_tag_action.setText("Add tag")
        self._add_tag_action.triggered.connect(self._add_tag)
        self._table.addAction(self._add_tag_action)

        layout = QHBoxLayout()
        layout.addWidget(self._table)
        super(CommitesWidget, self).setLayout(layout)

    def _current_index_changed(self, current, _previous):
        index = self._commites_model.index(current.row(), 0)
        commit_id = index.data(Qt.DisplayRole)
        self.current_commit_changed.emit(commit_id)

    def _add_tag(self):
        index = self._commites_model.index(self._table.currentIndex().row(), 0)
        commit_id = index.data(Qt.DisplayRole)
        d = add_tag_dialog.AddTagDialog(commit_id, self)
        d.exec_()

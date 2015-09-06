# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

import git


class StashesWidget(QtWidgets.QWidget):
    _git = git.Git()
    state_changed = pyqtSignal()

    def __init__(self, parent=None):
        super(StashesWidget, self).__init__(parent)

        self._stashes_list = QtWidgets.QTableWidget(self)
        self._stashes_list.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )

        self._save_action = QtWidgets.QAction(self)
        self._save_action.setText("Save")
        self._save_action.triggered.connect(self.save)

        self._apply_action = QtWidgets.QAction(self)
        self._apply_action.setText("Apply stash")
        self._apply_action.triggered.connect(self.apply)

        self._pop_action = QtWidgets.QAction(self)
        self._pop_action.setText("Pop stash")
        self._pop_action.triggered.connect(self.pop)

        self._drop_action = QtWidgets.QAction(self)
        self._drop_action.setText("Drop stash")
        self._drop_action.triggered.connect(self.drop)

        self._stashes_list.selectionModel().selectionChanged.connect(
            self._update_actions_enabled
        )

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._stashes_list)
        super(StashesWidget, self).setLayout(layout)

    def _update_actions_enabled(self, selected):
        item_selected = not selected.isEmpty()
        self._drop_action.setEnabled(item_selected)
        self._apply_action.setEnabled(item_selected)
        self._pop_action.setEnabled(self._stashes_list.rowCount() > 0)

    def update_stashes_list(self):
        self._stashes_list.clear()

        stashes = self._git.stashes()

        self._stashes_list.setRowCount(len(stashes))
        self._stashes_list.setColumnCount(2)
        self._stashes_list.setHorizontalHeaderLabels(["Name", "Description"])

        row = 0
        for stash in stashes:
            item = QtWidgets.QTableWidgetItem(stash.name)
            item.setToolTip(item.text())
            self._stashes_list.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(stash.description)
            item.setToolTip(item.text())
            self._stashes_list.setItem(row, 1, item)
            row += 1

        self._stashes_list.resizeColumnsToContents()
        self._stashes_list.resizeRowsToContents()

        self._update_actions_enabled(
            self._stashes_list.selectionModel().selection()
        )
        self.state_changed.emit()

    def menu(self):
        result = QtWidgets.QMenu(self)
        result.setTitle("Stashes")

        result.addAction(self._save_action)
        result.addSeparator()
        result.addAction(self._apply_action)
        result.addAction(self._pop_action)
        result.addSeparator()
        result.addAction(self._drop_action)

        return result

    def save(self):
        self._git.save_stash()
        self.update_stashes_list()

    def pop(self):
        self._git.pop_stash()
        self.update_stashes_list()

    def _selected_stash(self):
        row = self._stashes_list.currentRow()

        stash_name = str ()
        if row >= 0:
            stash_name = self._stashes_list.item(row, 0).text()

        return stash_name

    def drop(self):
        self._git.drop_stash(self._selected_stash())
        self.update_stashes_list()

    def apply(self):
        self._git.apply_stash(self._selected_stash())
        self.update_stashes_list()

    def count(self):
        return self._stashes_list.rowCount()
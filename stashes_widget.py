# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtGui
import git

class StashesWidget(QtGui.QWidget):
    _git = git.Git()

    def __init__(self, parent=None):
        super(StashesWidget, self).__init__(parent)

        self._stashes_list = QtGui.QTableWidget(self)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._stashes_list)
        super(StashesWidget, self).setLayout(layout)

        self.update_stashes_list()

    def update_stashes_list(self):
        self._stashes_list.clear()

        stashes = self._git.stashes()

        self._stashes_list.setRowCount(len(stashes))
        self._stashes_list.setColumnCount(1)

        row = 0
        for stash in stashes:
            item = QtGui.QTableWidgetItem(stash)
            item.setToolTip(item.text())
            self._stashes_list.setItem(row, 0, item)
            row += 1

        self._stashes_list.resizeColumnsToContents()
        self._stashes_list.resizeRowsToContents()
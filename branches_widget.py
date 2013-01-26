# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git

class BranchesWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(BranchesWidget, self).__init__(parent)

        self._local_branches_label = QtGui.QLabel("Local branches", self)

        self._local_branches_list = QtGui.QListWidget(self)

        self._remote_branches_label = QtGui.QLabel("Remote branches", self)

        self._remote_branches_list = QtGui.QListWidget(self)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._local_branches_label)
        layout.addWidget(self._local_branches_list)
        layout.addWidget(self._remote_branches_label)
        layout.addWidget(self._remote_branches_list)
        super(BranchesWidget, self).setLayout(layout)
        self._update_lists()

    def _update_lists(self):
        self._local_branches_list.clear()
        self._remote_branches_list.clear()

        current_branch = git.Git().current_branch()

        for branch in git.Git().local_branches():
            item = QtGui.QListWidgetItem(branch, self._local_branches_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self._local_branches_list.addItem(item)
            if current_branch == branch:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

        for branch in git.Git().remote_branches():
            item = QtGui.QListWidgetItem(branch, self._remote_branches_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self._remote_branches_list.addItem(item)


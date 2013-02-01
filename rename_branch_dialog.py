# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git


class RenameBranchDialog(QtGui.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super(RenameBranchDialog, self).__init__(parent)

        self._source_branch_label = QtGui.QLabel(self)
        self._source_branch_label.setText("Old name")

        self._source_branch = QtGui.QComboBox(self)
        self._source_branch.addItems(self._git.local_branches())
        self._source_branch.setCurrentIndex(
            self._source_branch.find(self._git.current_branch())
        )

        self._target_branch_label = QtGui.QLabel(self)
        self._target_branch_label.setText("New name")

        self._target_branch = QtGui.QLineEdit(self)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self._target_branch.textChanged.connect(
            lambda: buttons.button(QtGui.QDialogButtonBox.Ok).setEnabled(
                len(self._target_branch.text()) > 0
            )
        )

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._source_branch_label)
        layout.addWidget(self._source_branch)
        layout.addWidget(self._target_branch_label)
        layout.addWidget(self._target_branch)
        layout.addWidget(buttons)

    def old_name(self):
        return self._source_branch.currentText()

    def new_name(self):
        return self._target_branch.text()

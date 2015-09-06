# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox

import git


class RenameBranchDialog(QtWidgets.QDialog):
    _git = git.Git()

    def __init__(self, branch=str(), parent=None):
        super().__init__(parent)

        self._source_branch_label = QtWidgets.QLabel(self)
        self._source_branch_label.setText("Old name")

        self._source_branch = QtWidgets.QComboBox(self)
        self._source_branch.addItems(self._git.local_branches())
        self._source_branch.setCurrentIndex(-1)
        self._source_branch.currentIndexChanged.connect(
            self._source_branch_changed
        )

        self._target_branch_label = QtWidgets.QLabel(self)
        self._target_branch_label.setText("New name")

        self._target_branch = QtWidgets.QLineEdit(self)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self._target_branch.textChanged.connect(
            lambda: buttons.button(QDialogButtonBox.Ok).setEnabled(
                bool(self._target_branch.text())
            )
        )
        self._target_branch.textChanged.emit(str())
        self._target_branch.setFocus(8)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._source_branch_label)
        layout.addWidget(self._source_branch)
        layout.addWidget(self._target_branch_label)
        layout.addWidget(self._target_branch)
        layout.addWidget(buttons)
        self.setLayout(layout)

        self.set_source_branch(branch)

    def old_name(self):
        return self._source_branch.currentText()

    def new_name(self):
        return self._target_branch.text()

    def set_source_branch(self, branch):
        self._source_branch.setCurrentIndex(
            self._source_branch.findText(branch)
        )

    def _source_branch_changed(self):
        if not self._target_branch.isModified():
            self._target_branch.setText(
                self._source_branch.currentText()
            )

            self._target_branch.selectAll()
            self._target_branch.setFocus()

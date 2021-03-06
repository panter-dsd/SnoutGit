# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox

import git


class CreateBranchDialog(QtWidgets.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super(CreateBranchDialog, self).__init__(parent)

        self._branch_name_label = QtWidgets.QLabel("Branch name", self)

        self._branch_name = QtWidgets.QLineEdit(self)

        self._parent_branch_label = QtWidgets.QLabel("Parent branch", self)

        self._parent_branch = QtWidgets.QComboBox(self)
        self._parent_branch.setEditable(False)
        self._parent_branch.currentIndexChanged.connect(
            self._parent_branch_changed
        )

        self._can_checkout = QtWidgets.QCheckBox("Checkout into branch", self)
        self._can_checkout.setChecked(True)

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._branch_name_label)
        layout.addWidget(self._branch_name)
        layout.addWidget(self._parent_branch_label)
        layout.addWidget(self._parent_branch)
        layout.addWidget(self._can_checkout)
        layout.addWidget(self._buttons)
        super(CreateBranchDialog, self).setLayout(layout)

        self._update_parent_branches()

    def _update_parent_branches(self):
        self._parent_branch.clear()

        for name in self._git.local_branches():
            self._parent_branch.addItem(name, "local")

        for name in self._git.remote_branches():
            self._parent_branch.addItem(name, "remote")

        self.set_parent_branch(self._git.current_branch())

    def branch_name(self):
        return self._branch_name.text()

    def set_branch_name(self, name):
        self._branch_name.setText(name)

    def parent_branch(self):
        return self._parent_branch.currentText()

    def set_parent_branch(self, name):
        for i in range(self._parent_branch.count()):
            if self._parent_branch.itemText(i) == name:
                self._parent_branch.setCurrentIndex(i)
                break

    def can_checkout(self):
        return self._can_checkout.isChecked()

    def _parent_branch_changed(self):
        if self._branch_name.isModified():
            return

        name = self._parent_branch.currentText()
        is_local = self._parent_branch.itemData(
            self._parent_branch.currentIndex()
        ) == "local"

        self._branch_name.setText(
            is_local and name or name[name.find('/') + 1:]
        )

    def _extract_branch_name_from_parent(self, parent):
        return

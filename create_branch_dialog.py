# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import git


class CreateBranchDialog(QtGui.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super(CreateBranchDialog, self).__init__(parent)

        self._branch_name_label = QtGui.QLabel("Branch name", self)

        self._branch_name = QtGui.QLineEdit(self)

        self._parent_branch_label = QtGui.QLabel("Parent branch", self)

        self._parent_branch = QtGui.QComboBox(self)
        self._parent_branch.setEditable(False)

        self._can_checkout = QtGui.QCheckBox("Checkout into branch", self)
        self._can_checkout.setChecked(True)

        self._buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok
                                               | QtGui.QDialogButtonBox.Cancel,
                                               QtCore.Qt.Horizontal,
                                               self)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout()
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

        for name in self._git.local_branches() + self._git.remote_branches():
            self._parent_branch.addItem(name)

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
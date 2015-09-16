# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QDialogButtonBox

import git


class DeleteBranchDialog(QtWidgets.QDialog):
    _git = git.Git()

    def __init__(self, branch, parent=None):
        super(DeleteBranchDialog, self).__init__(parent)

        self._branch_label = QtWidgets.QLabel("Branch for delete", self)

        self._branch = QtWidgets.QComboBox(self)
        self._branch.setEditable(False)
        self._branch.currentIndexChanged.connect(
            lambda: self._update_check_merge_model(
                self._check_merge_tabs.currentIndex()
            )
        )

        self._check_merge_group = QtWidgets.QGroupBox(self)
        self._check_merge_group.setTitle("Check for merge")
        self._check_merge_group.setCheckable(True)
        self._check_merge_group.setChecked(True)

        self._check_merge_tabs = QtWidgets.QTabBar(self)
        self._check_merge_tabs.addTab("Local branch")
        self._check_merge_tabs.addTab("Remote branch")
        self._check_merge_tabs.currentChanged.connect(
            self._update_check_merge_model
        )

        self._check_merge_model = QStringListModel(self)

        self._check_merge_view = QtWidgets.QListView(self)
        self._check_merge_view.setModel(self._check_merge_model)

        check_merge_layout = QtWidgets.QVBoxLayout()
        check_merge_layout.addWidget(self._check_merge_tabs)
        check_merge_layout.addWidget(self._check_merge_view)
        self._check_merge_group.setLayout(check_merge_layout)

        self._delete_force = QtWidgets.QCheckBox(self)
        self._delete_force.setText("Delete force")
        self._delete_force.setChecked(False)

        self._check_merge_group.toggled.connect(
            lambda checked: self._delete_force.setChecked(not checked)
        )

        self._delete_force.toggled.connect(
            lambda checked: self._check_merge_group.setChecked(not checked)
        )

        buttons = QDialogButtonBox(Qt.Horizontal, self)
        self._delete_button = QtWidgets.QPushButton(self)
        self._delete_button.setText("Delete")

        buttons.addButton(self._delete_button, QDialogButtonBox.AcceptRole)
        buttons.addButton(QDialogButtonBox.Cancel)

        buttons.accepted.connect(self._delete)
        buttons.rejected.connect(super(DeleteBranchDialog, self).reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._branch_label)
        layout.addWidget(self._branch)
        layout.addWidget(self._check_merge_group)
        layout.addWidget(self._delete_force)
        layout.addWidget(buttons)
        super(DeleteBranchDialog, self).setLayout(layout)

        self._update_branches_list()
        self.set_branch(branch)
        self._update_check_merge_model(0)

    def _update_branches_list(self):
        self._branch.clear()

        current = self._git.current_branch()

        for name in self._git.local_branches():
            if name != current:
                self._branch.addItem(name)

    def set_branch(self, name):
        for i in range(self._branch.count()):
            if self._branch.itemText(i) == name:
                self._branch.setCurrentIndex(i)
                break

    def _update_check_merge_model(self, current):
        merged = set(self._git.merged(self._branch.currentText()))

        def not_merged(branches):
            return list(set(branches) - set(merged))

        objects = []

        if current == 0:
            objects = self._git.local_branches()
        else:
            objects = self._git.remote_branches()

        self._check_merge_model.setStringList(not_merged(objects))

    def _delete(self):
        branch = self._branch.currentText()

        if self._check_merge_group.isChecked():
            check_branch = self._check_merge_view.currentIndex().data(
                Qt.DisplayRole
            )

            if len(check_branch) == 0:
                check_branch = self._git.current_branch()

            if self._git.merged(check_branch).count(branch) == 0:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Delete branch",
                    "Branch " + branch + " not merged to " + check_branch
                )
                return

        self._git.delete_branch(branch, True)

        super(DeleteBranchDialog, self).accept()
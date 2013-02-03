# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git


class DeleteBranchDialog(QtGui.QDialog):
    _git = git.Git()

    def __init__(self, branch, parent=None):
        super(DeleteBranchDialog, self).__init__(parent)

        self._branch_label = QtGui.QLabel("Branch for delete", self)

        self._branch = QtGui.QComboBox(self)
        self._branch.setEditable(False)
        self._branch.currentIndexChanged.connect(
            lambda: self._update_check_merge_model(
                self._check_merge_tabs.currentIndex()
            )
        )

        self._check_merge_group = QtGui.QGroupBox(self)
        self._check_merge_group.setTitle("Check for merge")
        self._check_merge_group.setCheckable(True)
        self._check_merge_group.setChecked(True)

        self._check_merge_tabs = QtGui.QTabBar(self)
        self._check_merge_tabs.addTab("Local branch")
        self._check_merge_tabs.addTab("Remote branch")
        self._check_merge_tabs.currentChanged.connect(
            self._update_check_merge_model
        )

        self._check_merge_model = QtGui.QStringListModel(self)

        self._check_merge_view = QtGui.QListView(self)
        self._check_merge_view.setModel(self._check_merge_model)

        check_merge_layout = QtGui.QVBoxLayout()
        check_merge_layout.addWidget(self._check_merge_tabs)
        check_merge_layout.addWidget(self._check_merge_view)
        self._check_merge_group.setLayout(check_merge_layout)

        self._delete_force = QtGui.QCheckBox(self)
        self._delete_force.setText("Delete force")
        self._delete_force.setChecked(False)

        self._check_merge_group.toggled.connect(
            lambda checked: self._delete_force.setChecked(not checked)
        )

        self._delete_force.toggled.connect(
            lambda checked: self._check_merge_group.setChecked(not checked)
        )

        buttons = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal,
                                         self)
        self._delete_button = QtGui.QPushButton(self)
        self._delete_button.setText("Delete")

        buttons.addButton(self._delete_button,
                          QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton(QtGui.QDialogButtonBox.Cancel)

        buttons.accepted.connect(self._delete)
        buttons.rejected.connect(super(DeleteBranchDialog, self).reject)

        layout = QtGui.QVBoxLayout()
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
        if current == 0:
            branches = self._git.local_branches()
        else:
            branches = self._git.remote_branches()

        branches.remove(self._branch.currentText())
        self._check_merge_model.setStringList(branches)

    def _delete(self):
        branch = self._branch.currentText()

        if self._check_merge_group.isChecked():
            check_branch = self._check_merge_view.currentIndex().data(
                QtCore.Qt.DisplayRole
            )

            if len(check_branch) == 0:
                check_branch = self._git.current_branch()

            if self._git.merged(branch).count(check_branch) == 0:
                QtGui.QMessageBox.critical(
                    self,
                    "Delete branch",
                    "Branch " + branch + " not merged to " + check_branch
                )
                return

        self._git.delete_branch(branch, True)

        super(DeleteBranchDialog, self).accept()
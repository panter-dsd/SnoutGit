# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox

import git


class RemotesWidget(QtWidgets.QWidget):
    def __init__(self, git_control: git.Git, parent=None):
        super().__init__(parent)

        self._git_control = git_control

        self._remote_label = None
        self._remote_list = None

        remotes = self._git_control.remote_list()

        layout = QtWidgets.QVBoxLayout()

        if len(remotes) > 1:
            self._remote_list = QtWidgets.QListWidget(self)
            self._remote_list.addItems(remotes)

            self._set_list_check_state()

            layout.addWidget(self._remote_list)
        elif remotes:
            self._remote_label = QtWidgets.QLabel(remotes[0], self)
            layout.addWidget(self._remote_label)

        self.setLayout(layout)

    def remotes(self) -> list:
        result = []

        if self._remote_label:
            result.append(self._remote_label.text())
        elif self._remote_list:
            for i in range(0, self._remote_list.count()):
                item = self._remote_list.item(i)
                if item.checkState() == Qt.Checked:
                    result.append(item.text())

        return result

    def _set_list_check_state(self):
        for i in range(0, self._remote_list.count()):
            self._remote_list.item(i).setCheckState(
                Qt.Checked if i == 0 else Qt.Unchecked
            )


class PushDialog(QtWidgets.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super(PushDialog, self).__init__(parent)

        self._branch_label = QtWidgets.QLabel("Branch", self)

        self._branch = QtWidgets.QComboBox(self)
        self._branch.setEditable(False)

        self._remote_label = QtWidgets.QLabel("Remote", self)

        self._remote = RemotesWidget(self._git)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self._branch_label, 0, 0)
        grid.addWidget(self._branch, 0, 1)
        grid.addWidget(self._remote_label, 1, 0)
        grid.addWidget(self._remote, 1, 1)

        self._options_group = QtWidgets.QGroupBox(self)
        self._options_group.setTitle("Options")

        self._force_option = QtWidgets.QCheckBox(self)
        self._force_option.setText("Force overwrite existing branch")
        self._force_option.setChecked(False)

        self._push_tags_option = QtWidgets.QCheckBox(self)
        self._push_tags_option.setText("Push tags")
        self._push_tags_option.setChecked(True)

        options_layout = QtWidgets.QVBoxLayout()
        options_layout.addWidget(self._force_option)
        options_layout.addWidget(self._push_tags_option)
        self._options_group.setLayout(options_layout)

        buttons = QtWidgets.QDialogButtonBox(Qt.Horizontal, self)
        self._push_button = QtWidgets.QPushButton(self)
        self._push_button.setText("Push")

        buttons.addButton(self._push_button, QDialogButtonBox.AcceptRole)
        buttons.addButton(QDialogButtonBox.Cancel)

        buttons.accepted.connect(self._push)
        buttons.rejected.connect(super(PushDialog, self).reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(self._options_group)
        layout.addWidget(buttons)
        super(PushDialog, self).setLayout(layout)

        self._update_branches_list()
        self.set_branch(self._git.current_branch())

    def _update_branches_list(self):
        self._branch.clear()
        self._branch.addItems(self._git.local_branches())

    def set_branch(self, name):
        for i in range(self._branch.count()):
            if self._branch.itemText(i) == name:
                self._branch.setCurrentIndex(i)
                break

    def _push(self):
        remotes = self._remote.remotes()
        if not remotes:
            super().reject()

        push_options = git.PushOptions(self._branch.currentText(), remotes)
        push_options.force = self._force_option.isChecked()
        push_options.include_tags = self._push_tags_option.isChecked()

        self._git.push(push_options)

        text = [self._git.last_error(),
                self._git.last_output()]

        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle("Push")

        if text[0]:
            dialog.setText("Failure")
            dialog.setDetailedText("\n".join(text[0]))
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
        else:
            dialog.setText("Success")
            dialog.setDetailedText("\n".join(text[1]))
            dialog.setIcon(QtWidgets.QMessageBox.Information)

        dialog.exec_()

        super().accept()

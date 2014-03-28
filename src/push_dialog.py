# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git


class PushDialog(QtGui.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super(PushDialog, self).__init__(parent)

        self._branch_label = QtGui.QLabel("Branch", self)

        self._branch = QtGui.QComboBox(self)
        self._branch.setEditable(False)

        self._remote_label = QtGui.QLabel("Remote", self)

        self._remote = QtGui.QComboBox(self)
        self._remote.setEditable(False)

        grid = QtGui.QGridLayout()
        grid.addWidget(self._branch_label, 0, 0)
        grid.addWidget(self._branch, 0, 1)
        grid.addWidget(self._remote_label, 1, 0)
        grid.addWidget(self._remote, 1, 1)

        self._options_group = QtGui.QGroupBox(self)
        self._options_group.setTitle("Options")

        self._force_option = QtGui.QCheckBox(self)
        self._force_option.setText("Force overwrite existing branch")
        self._force_option.setChecked(False)

        self._push_tags_option = QtGui.QCheckBox(self)
        self._push_tags_option.setText("Push tags")
        self._push_tags_option.setChecked(True)

        options_layout = QtGui.QVBoxLayout()
        options_layout.addWidget(self._force_option)
        options_layout.addWidget(self._push_tags_option)
        self._options_group.setLayout(options_layout)

        buttons = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal,
                                         self)
        self._push_button = QtGui.QPushButton(self)
        self._push_button.setText("Push")

        buttons.addButton(self._push_button,
                          QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton(QtGui.QDialogButtonBox.Cancel)

        buttons.accepted.connect(self._push)
        buttons.rejected.connect(super(PushDialog, self).reject)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(self._options_group)
        layout.addWidget(buttons)
        super(PushDialog, self).setLayout(layout)

        self._update_branches_list()
        self.set_branch(self._git.current_branch())

        self._update_remotes_list()

    def _update_branches_list(self):
        self._branch.clear()
        self._branch.addItems(self._git.local_branches())

    def set_branch(self, name):
        for i in range(self._branch.count()):
            if self._branch.itemText(i) == name:
                self._branch.setCurrentIndex(i)
                break

    def _update_remotes_list(self):
        self._remote.clear()
        self._remote.addItems(self._git.remote_list())

    def _push(self):
        push_options = git.PushOptions(self._branch.currentText(),
                                       self._remote.currentText())
        push_options.force = self._force_option.isChecked()
        push_options.include_tags = self._push_tags_option.isChecked()

        self._git.push(push_options)

        text = [self._git._last_error,
                self._git._last_output]

        dialog = QtGui.QMessageBox(self)
        dialog.setWindowTitle("Push")

        if text[0]:
            dialog.setText("Failure")
            dialog.setDetailedText("\n".join(text[0]))
            dialog.setIcon(QtGui.QMessageBox.Critical)
        else:
            dialog.setText("Success")
            dialog.setDetailedText("\n".join(text[1]))
            dialog.setIcon(QtGui.QMessageBox.Information)

        dialog.exec_()

        super(PushDialog, self).accept()
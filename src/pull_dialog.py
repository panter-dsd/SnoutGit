# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git


class PullDialog(QtGui.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._remote_label = QtGui.QLabel("Remote", self)

        self._remote = QtGui.QComboBox(self)
        self._remote.setEditable(False)

        grid = QtGui.QGridLayout()
        grid.addWidget(self._remote_label, 0, 0)
        grid.addWidget(self._remote, 0, 1)

        self._options_group = QtGui.QGroupBox(self)
        self._options_group.setTitle("Options")

        self._force_option = QtGui.QCheckBox(self)
        self._force_option.setText("Force overwrite existing branch")
        self._force_option.setChecked(False)

        self._no_tags_option = QtGui.QCheckBox(self)
        self._no_tags_option.setText("Don't pull tags")
        self._no_tags_option.setChecked(False)

        self._prune_option = QtGui.QCheckBox(self)
        self._prune_option.setText("Prune")
        self._prune_option.setChecked(True)

        options_layout = QtGui.QVBoxLayout()
        options_layout.addWidget(self._force_option)
        options_layout.addWidget(self._no_tags_option)
        options_layout.addWidget(self._prune_option)
        self._options_group.setLayout(options_layout)

        buttons = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal,
                                         self)
        self._push_button = QtGui.QPushButton(self)
        self._push_button.setText("Pull")

        buttons.addButton(self._push_button,
                          QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton(QtGui.QDialogButtonBox.Cancel)

        buttons.accepted.connect(self._pull)
        buttons.rejected.connect(super().reject)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(self._options_group)
        layout.addWidget(buttons)
        super().setLayout(layout)

        self._update_remotes_list()

    def _update_remotes_list(self):
        self._remote.clear()
        self._remote.addItems(self._git.remote_list())

    def _pull(self):
        pull_options = git.PullOptions(self._remote.currentText())
        pull_options.force = self._force_option.isChecked()
        pull_options.no_tags = self._no_tags_option.isChecked()
        pull_options.prune = self._prune_option.isChecked()

        self._git.pull(pull_options)

        text = [self._git._last_error,
                self._git._last_output]

        dialog = QtGui.QMessageBox(self)
        dialog.setWindowTitle("Pull")

        if text[0]:
            dialog.setText("\n".join(text[0]))
            dialog.setIcon(QtGui.QMessageBox.Critical)
        else:
            dialog.setText("\n".join(text[1]))
            dialog.setIcon(QtGui.QMessageBox.Information)

        dialog.exec_()

        super().accept()
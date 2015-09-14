# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox

import git


class PullDialog(QtWidgets.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._remote_label = QtWidgets.QLabel("Remote", self)

        self._remote = QtWidgets.QComboBox(self)
        self._remote.setEditable(False)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self._remote_label, 0, 0)
        grid.addWidget(self._remote, 0, 1)

        self._options_group = QtWidgets.QGroupBox(self)
        self._options_group.setTitle("Options")

        self._force_option = QtWidgets.QCheckBox(self)
        self._force_option.setText("Force overwrite existing branch")
        self._force_option.setChecked(False)

        self._no_tags_option = QtWidgets.QCheckBox(self)
        self._no_tags_option.setText("Don't pull tags")
        self._no_tags_option.setChecked(False)

        self._prune_option = QtWidgets.QCheckBox(self)
        self._prune_option.setText("Prune")
        self._prune_option.setChecked(True)

        options_layout = QtWidgets.QVBoxLayout()
        options_layout.addWidget(self._force_option)
        options_layout.addWidget(self._no_tags_option)
        options_layout.addWidget(self._prune_option)
        self._options_group.setLayout(options_layout)

        buttons = QDialogButtonBox(Qt.Horizontal, self)
        self._push_button = QtWidgets.QPushButton(self)
        self._push_button.setText("Pull")

        buttons.addButton(self._push_button, QDialogButtonBox.AcceptRole)
        buttons.addButton(QDialogButtonBox.Cancel)

        buttons.accepted.connect(self._pull)
        buttons.rejected.connect(super().reject)

        layout = QtWidgets.QVBoxLayout()
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

        text = [self._git._last_error, self._git._last_output]

        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle("Pull")

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

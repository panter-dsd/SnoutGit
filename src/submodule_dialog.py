# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox


class SubmoduleDialog(QtWidgets.QDialog):
    def __init__(self, submodules: list, parent: QtWidgets.QWidget=None):
        super().__init__(parent)

        self._submodules_list = QtWidgets.QListWidget(self)
        self._submodules_list.addItems(submodules)
        self._submodules_list.itemDoubleClicked.connect(self.accept)

        self._submodules_list.setCurrentRow(0)

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._submodules_list)
        layout.addWidget(self._buttons)
        self.setLayout(layout)

    def submodule(self):
        return self._submodules_list.currentItem().text()

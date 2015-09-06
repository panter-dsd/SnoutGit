# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox

from git import Remote, Git


class AddRemoteDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._name_label = QtWidgets.QLabel(self)
        self._name_label.setText("Name")

        self._name_edit = QtWidgets.QLineEdit(self)

        self._url_label = QtWidgets.QLabel(self)
        self._url_label.setText("Url")

        self._url_edit = QtWidgets.QLineEdit(self)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )

        buttons.accepted.connect(self._add_remote)
        buttons.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._name_label)
        layout.addWidget(self._name_edit)
        layout.addWidget(self._url_label)
        layout.addWidget(self._url_edit)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def _add_remote(self):
        name = self._name_edit.text()

        if not name:
            QtWidgets.QMessageBox.critical(self, "Error", "Name is empty")
            return

        url = self._url_edit.text()

        if not url:
            QtWidgets.QMessageBox.critical(self, "Error", "Url is empty")
            return

        remote = Remote(Git())
        remote.add_remote(name, url)
        self.accept()

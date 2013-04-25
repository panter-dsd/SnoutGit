# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui

from git import Remote, Git


class AddRemoteDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._name_label = QtGui.QLabel(self)
        self._name_label.setText("Name")

        self._name_edit = QtGui.QLineEdit(self)

        self._url_label = QtGui.QLabel(self)
        self._url_label.setText("Url")

        self._url_edit = QtGui.QLineEdit(self)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )

        buttons.accepted.connect(self._add_remote)
        buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._name_label)
        layout.addWidget(self._name_edit)
        layout.addWidget(self._url_label)
        layout.addWidget(self._url_edit)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def _add_remote(self):
        name = self._name_edit.text()

        if not name:
            QtGui.QMessageBox.critical(self, "Error", "Name is empty")
            return

        url = self._url_edit.text()

        if not url:
            QtGui.QMessageBox.critical(self, "Error", "Url is empty")
            return

        remote = Remote(Git())
        remote.add_remote(name, url)
        self.accept()

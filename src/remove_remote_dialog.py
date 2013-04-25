# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui

from git import Git, Remote


class RemoveRemoteDialog(QtGui.QDialog):
    _remote = Remote(Git())

    def __init__(self, parent=None):
        super().__init__(parent)

        self._remote_label = QtGui.QLabel(self)
        self._remote_label.setText("Remote")

        self._remote_edit = QtGui.QComboBox(self)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )

        buttons.accepted.connect(self._remove_remote)
        buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._remote_label)
        layout.addWidget(self._remote_edit)
        layout.addWidget(buttons)
        self.setLayout(layout)

        self._update_remotes_list()

    def _remove_remote(self):
        remote_name = self._remote_edit.currentText()

        if remote_name:
            self._remote.remove_remote(remote_name)
            self.accept()
        else:
            QtGui.QMessageBox.critical(self, "Error", "Select remote")

    def _update_remotes_list(self):
        self._remote_edit.clear()
        self._remote_edit.addItems(self._remote.remotes_list())
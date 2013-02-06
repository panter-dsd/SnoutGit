# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git


class AddTagDialog(QtGui.QDialog):
    _git = git.Git()

    def __init__(self, commit, parent=None):
        super(AddTagDialog, self).__init__(parent)

        self._commit = commit

        self._name_label = QtGui.QLabel(self)
        self._name_label.setText("Tag name")

        self._name = QtGui.QLineEdit(self)

        self._message_label = QtGui.QLabel(self)
        self._message_label.setText("Tag annotation")

        self._message = QtGui.QPlainTextEdit(self)

        buttons = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal, self)
        self._create_tag_button = QtGui.QPushButton(self)
        self._create_tag_button.setText("Create tag")

        buttons.addButton(self._create_tag_button,
                          QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton(QtGui.QDialogButtonBox.Cancel)

        buttons.accepted.connect(self._create_tag)
        buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._name_label)
        layout.addWidget(self._name)
        layout.addWidget(self._message_label)
        layout.addWidget(self._message)
        layout.addWidget(buttons)
        self.setLayout(layout)

    @property
    def commit(self):
        return self._commit

    @commit.setter
    def set_commit(self, commit):
        self._commit = commit

    def _create_tag(self):
        self._git.create_tag(self._commit,
                             self._name.text(),
                             self._message.toPlainText())
        self.accept()
# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import os
import subprocess

def commit(path, name, description):
    os.chdir(path)
    command = "git commit -m \"{0}\"".format(name + "\n" + description)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    print(process.stdout.readlines())
    return True


class CommitWidget(QtGui.QWidget):
    commited = QtCore.Signal()
    _path = str()

    def __init__(self, path, parent = None):
        super(CommitWidget, self).__init__(parent)

        self._path = path

        self._menu_button = QtGui.QToolButton(self)
        self._menu_button.setAutoRaise(True)
        self._menu_button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)

        self._commit_name_edit = QtGui.QLineEdit(self)

        self._save_button = QtGui.QToolButton(self)
        self._save_button.setAutoRaise(True)
        self._save_button.setText("Save")
        self._save_button.setIcon(super(CommitWidget, self).style().standardIcon(QtGui.QStyle.SP_DialogSaveButton))
        self._save_button.clicked.connect(self._commit)

        self._commit_description_edit = QtGui.QPlainTextEdit(self)

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(self._menu_button)
        top_layout.addWidget(self._commit_name_edit)
        top_layout.addWidget(self._save_button)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self._commit_description_edit)
        super(CommitWidget, self).setLayout(layout)

        save_action = QtGui.QAction(self)
        save_action.setText("Save")
        save_action.triggered.connect(self._commit)
        save_action.setShortcut(QtCore.Qt.CTRL | QtCore.Qt.Key_Return)
        self._menu_button.addAction(save_action)

        ammend_action = QtGui.QAction(self)
        ammend_action.setText("Ammend last commit")
        self._menu_button.addAction(ammend_action)

    def _commit(self):
        commit_name = self._commit_name_edit.text()
        if len(commit_name) > 0:
            if commit(self._path, commit_name, self._commit_description_edit.toPlainText()):
                self._commit_name_edit.clear()
                self._commit_description_edit.clear()
                self.commited.emit()
        else:
            QtGui.QMessageBox.critical(self, "Error", "Commit name is empty.")
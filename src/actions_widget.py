# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSizePolicy

import git
import push_dialog
import pull_dialog


class ActionsWidget(QtWidgets.QWidget):
    _git = git.Git()
    state_changed = pyqtSignal()

    def __init__(self, parent=None):
        super(ActionsWidget, self).__init__(parent)

        _svn_button = QtWidgets.QToolButton(self)
        _svn_button.setText("Svn")

        _svn_button.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )

        _svn_button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)

        rebase_action = QtWidgets.QAction(self)
        rebase_action.setText("Rebase")
        rebase_action.triggered.connect(self._svn_rebase)
        _svn_button.addAction(rebase_action)

        dcommit_action = QtWidgets.QAction(self)
        dcommit_action.setText("Dcommit")
        dcommit_action.triggered.connect(self._svn_dcommit)
        _svn_button.addAction(dcommit_action)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(_svn_button)

        layout.addSpacerItem(
            QtWidgets.QSpacerItem(
                0, 0, QSizePolicy.Preferred, QSizePolicy.Expanding
            )
        )

        super(ActionsWidget, self).setLayout(layout)

    def _svn_rebase(self):
        self._git.svn_rebase()
        self.show_dialog("SVN rebase")

    def _svn_dcommit(self):
        self._git.svn_dcommit()
        self.show_dialog("SVN dcommit")

    def show_dialog(self, command):
        text = [self._git._last_error, self._git._last_output]

        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle(command)

        if text[0]:
            dialog.setText("\n".join(text[0]))
            dialog.setIcon(QtWidgets.QMessageBox.Critical)
        else:
            dialog.setText("\n".join(text[1]))
            dialog.setIcon(QtWidgets.QMessageBox.Information)

        dialog.exec_()

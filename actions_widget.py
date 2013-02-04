# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git


class ActionsWidget(QtGui.QWidget):
    _git = git.Git()
    state_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ActionsWidget, self).__init__(parent)

        _push_button = QtGui.QPushButton(self)
        _push_button.setText("Push")
        _push_button.clicked.connect(self.push)

        _pull_button = QtGui.QPushButton(self)
        _pull_button.setText("Pull")
        _pull_button.clicked.connect(self.pull)

        _svn_button = QtGui.QToolButton(self)
        _svn_button.setText("Svn")
        _svn_button.setSizePolicy(QtGui.QSizePolicy.Preferred,
                                  QtGui.QSizePolicy.Preferred)
        _svn_button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)

        rebase_action = QtGui.QAction(self)
        rebase_action.setText("Rebase")
        rebase_action.triggered.connect(self._svn_rebase)
        _svn_button.addAction(rebase_action)

        dcommit_action = QtGui.QAction(self)
        dcommit_action.setText("Dcommit")
        dcommit_action.triggered.connect(self._svn_dcommit)
        _svn_button.addAction(dcommit_action)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(_push_button)
        layout.addWidget(_pull_button)
        layout.addWidget(_svn_button)
        layout.addSpacerItem(QtGui.QSpacerItem(0,
                                               0,
                                               QtGui.QSizePolicy.Preferred,
                                               QtGui.QSizePolicy.Expanding))
        super(ActionsWidget, self).setLayout(layout)

    def push(self):
        self._git.push()
        self.state_changed.emit()
        self.show_dialog("Push")

    def pull(self):
        self._git.pull()
        self.show_dialog("Pull")

    def _svn_rebase(self):
        self._git.svn_rebase()
        self.show_dialog("SVN rebase")

    def _svn_dcommit(self):
        self._git.svn_dcommit()
        self.show_dialog("SVN dcommit")

    def show_dialog(self, command):
        text = [self._git._last_error,
                self._git._last_output]

        dialog = QtGui.QMessageBox(self)
        dialog.setWindowTitle(command)

        if len(text[0]) > 0:
            dialog.setText("\n".join(text[0]))
            dialog.setIcon(QtGui.QMessageBox.Critical)
        else:
            dialog.setText("\n".join(text[1]))
            dialog.setIcon(QtGui.QMessageBox.Information)

        dialog.exec_()
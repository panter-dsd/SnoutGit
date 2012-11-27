# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtGui
import subprocess
import os


def push(path):
    os.chdir(path)
    command = "git push"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    print(process.stdout.readlines())
    return True


def pull(path):
    os.chdir(path)
    command = "git pull"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    print(process.stdout.readlines())
    return True

def svn_rebase(path):
    os.chdir(path)
    command = "git svn rebase"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    print(process.stdout.readlines())
    return True

def svn_dcommit(path):
    os.chdir(path)
    command = "git svn dcommit"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    print(process.stdout.readlines())
    return True



class ActionsWidget(QtGui.QWidget):
    _path = str()

    def __init__(self, path, parent=None):
        super(ActionsWidget, self).__init__(parent)

        self._path = path

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
        push(self._path)

    def pull(self):
        pull(self._path)

    def _svn_rebase(self):
        svn_rebase(self._path)

    def _svn_dcommit(self):
        svn_dcommit(self._path)

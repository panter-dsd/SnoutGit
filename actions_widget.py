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


class ActionsWidget(QtGui.QWidget):
    _path = str()

    def __init__(self, path, parent=None):
        super(ActionsWidget, self).__init__(parent)

        self._path = path

        push_button = QtGui.QPushButton(self)
        push_button.setText("Push")
        push_button.clicked.connect(self.push)

        pull_button = QtGui.QPushButton(self)
        pull_button.setText("Pull")
        pull_button.clicked.connect(self.pull)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(push_button)
        layout.addWidget(pull_button)
        layout.addSpacerItem(QtGui.QSpacerItem(0,
                                               0,
                                               QtGui.QSizePolicy.Preferred,
                                               QtGui.QSizePolicy.Expanding))
        super(ActionsWidget, self).setLayout(layout)

    def push(self):
        push(self._path)

    def pull(self):
        pull(self._path)

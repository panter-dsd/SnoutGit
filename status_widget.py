# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import subprocess
import os
import re

def get_status(path):
    os.chdir(path)
    command = "git status -u --porcelain"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    result = []
    for line in process.stdout.readlines():
        line = line.rstrip()
        if len(line) > 0:
            result.append(line.decode())
    return result

class StatusWidget(QtGui.QWidget):
    _path = str()
    _last_status = []

    def __init__(self, path, parent):
        super(StatusWidget, self).__init__(parent)

        self._path = path

        self._files_view = QtGui.QTreeWidget(self)
        self._files_view.setHeaderHidden(True)

        self._unstaged = QtGui.QTreeWidgetItem(self._files_view)
        self._unstaged.setText(0, "Unstaged")

        self._staged = QtGui.QTreeWidgetItem(self._files_view)
        self._staged.setText(0, "Staged")

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._files_view)
        super(StatusWidget, self).setLayout(layout)

        update_timer = QtCore.QTimer(self)
        update_timer.timeout.connect(self._update_file_list)
        update_timer.start(100)

    def _update_file_list(self):
        current_status = get_status(self._path)
        if self._last_status == current_status:
            return
        self._last_status = current_status

        self._staged.takeChildren()
        self._unstaged.takeChildren()

        for status_line in self._last_status:
            print(status_line)
            status = status_line[:2]
            file_name = status_line[3:]

            if not status[0] in [' ', '?']:
                item = QtGui.QTreeWidgetItem(self._staged)
                item.setText(0, file_name)

            if not status[1] in [' ', '?']:
                item = QtGui.QTreeWidgetItem(self._unstaged)
                item.setText(0, file_name)

        self._files_view.expandAll()
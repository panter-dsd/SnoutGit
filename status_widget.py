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

    def __init__(self, path, parent):
        super(StatusWidget, self).__init__(parent)

        self._path = path

        self._files_view = QtGui.QTreeWidget(self)
        self._files_view.setHeaderHidden(True)
        self._update_file_list()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._files_view)
        super(StatusWidget, self).setLayout(layout)

    def _update_file_list(self):
        self._files_view.clear()

        unstaged = QtGui.QTreeWidgetItem(self._files_view)
        unstaged.setText(0, "Unstaged")

        staged = QtGui.QTreeWidgetItem(self._files_view)
        staged.setText(0, "Staged")

        for status_line in get_status(self._path):
            print(status_line)
            status = status_line[:2]
            file_name = status_line[3:]

            if not status[0] in [' ', '?']:
                item = QtGui.QTreeWidgetItem(staged)
                item.setText(0, file_name)

            if not status[1] in [' ', '?']:
                item = QtGui.QTreeWidgetItem(unstaged)
                item.setText(0, file_name)

        for index in range(self._files_view.topLevelItemCount()):
            item = self._files_view.topLevelItem(index)
            if item.childCount() == 0:
                self._files_view.takeTopLevelItem(index)

        self._files_view.expandAll()
# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import os
import subprocess
import diff_highlighter


class DiffFileWidget(QtGui.QWidget):
    _file_name = str()

    def __init__(self, path, parent=None):
        super(DiffFileWidget, self).__init__(parent)

        self._path = path

        self._diff_veiw = QtGui.QPlainTextEdit(self)
        self._diff_veiw.setWordWrapMode(QtGui.QTextOption.NoWrap)
        diff_highlighter.DiffHighlighter(self._diff_veiw.document())

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._diff_veiw)
        super(DiffFileWidget, self).setLayout(layout)

    @QtCore.Slot(str)
    def set_file(self, file_name):
        self._file_name = file_name
        self._update_diff()

    @QtCore.Slot()
    def clear(self):
        self._diff_veiw.clear()

    def _update_diff(self):
        os.chdir(self._path)
        command = "git diff-index -U5 HEAD {0}".format(self._file_name)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        text = []

        for line in process.stdout.readlines():
            text.append(line.decode())

        self._diff_veiw.setPlainText("".join(text))

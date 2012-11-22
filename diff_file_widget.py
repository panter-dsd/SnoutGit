# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import re
import os
import subprocess

class DiffHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent = None):
        super(DiffHighlighter, self).__init__(parent)

    def highlightBlock(self, text):
        super(DiffHighlighter, self).setFormat (0, len(text), QtCore.Qt.black)

        added = re.match("^\+.*$", text)
        if added:
            super(DiffHighlighter, self).setFormat (added.pos, added.endpos, QtCore.Qt.green)

        removed = re.match("^\-.*$", text)
        if removed:
            super(DiffHighlighter, self).setFormat (removed.pos, removed.endpos, QtCore.Qt.red)


class DiffFileWidget(QtGui.QWidget):
    _file_name = str()

    def __init__(self, path, parent = None):
        super(DiffFileWidget, self).__init__(parent)

        self._path = path

        self._diff_veiw = QtGui.QPlainTextEdit(self)
        self._diff_veiw.setWordWrapMode(QtGui.QTextOption.NoWrap)
        DiffHighlighter(self._diff_veiw.document())

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._diff_veiw)
        super(DiffFileWidget, self).setLayout(layout)

    @QtCore.Slot(str)
    def set_file(self, file_name):
        self._file_name = file_name
        self._update_diff()

    def _update_diff(self):
        os.chdir(self._path)
        command = "git diff-tree -U5 HEAD {0}".format(self._file_name)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        text = []

        for line in process.stdout.readlines():
            text.append(line.decode())

        self._diff_veiw.setPlainText("".join(text))

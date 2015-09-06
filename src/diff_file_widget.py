# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget

import diff_highlighter
import git


class DiffFileWidget(QWidget):
    _file_name = str()

    def __init__(self, path, parent=None):
        super(DiffFileWidget, self).__init__(parent)

        self._path = path

        self._diff_veiw = QPlainTextEdit(self)
        self._diff_veiw.setReadOnly(True)
        self._diff_veiw.setWordWrapMode(QTextOption.NoWrap)
        self._diff_veiw.setUndoRedoEnabled(False)
        self._highlighter = diff_highlighter.DiffHighlighter(
            self._diff_veiw.document())

        layout = QVBoxLayout()
        layout.addWidget(self._diff_veiw)
        super(DiffFileWidget, self).setLayout(layout)

    @pyqtSlot(str, bool)
    def set_file(self, file_name, diff_with_index=False):
        self._file_name = file_name
        self._update_diff(diff_with_index)

    @pyqtSlot()
    def clear(self):
        self._diff_veiw.clear()

    def _update_diff(self, diff_with_index):
        command = ["diff", "-U5", self._file_name]
        if diff_with_index:
            command.insert(1, "--staged")

        self._diff_veiw.setPlainText(
            "\n".join(git.Git().execute_command(command, False))
        )

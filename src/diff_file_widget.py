# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QVBoxLayout, QWidget
from diff_highlighter import DiffHighlighter

from ApplicationSettings import application_settings as settings

import git

__author__ = 'panter.dsd@gmail.com'


class DiffFileWidget(QWidget):
    _file_name = str()

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self._path = path

        self._diff_viewer = QPlainTextEdit(self)
        self._diff_viewer.setReadOnly(True)
        self._diff_viewer.setWordWrapMode(QTextOption.NoWrap)
        self._diff_viewer.setUndoRedoEnabled(False)
        self._highlighter = DiffHighlighter(self._diff_viewer.document())

        self.apply_settings()

        layout = QVBoxLayout()
        layout.addWidget(self._diff_viewer)
        self.setLayout(layout)

    def apply_settings(self):
        font = settings.diff_viewer_font()
        self._diff_viewer.setFont(font if font else QApplication.font())
        self._highlighter.update_settings()

    @pyqtSlot(str, bool)
    def set_file(self, file_name, diff_with_index=False):
        self._file_name = file_name
        self._update_diff(diff_with_index)

    @pyqtSlot()
    def clear(self):
        self._diff_viewer.clear()

    def _update_diff(self, diff_with_index):
        command = ["diff", "-U5", self._file_name]

        if diff_with_index:
            command.insert(1, "--staged")

        self._diff_viewer.setPlainText(
            "\n".join(git.Git().execute_command(command, False))
        )

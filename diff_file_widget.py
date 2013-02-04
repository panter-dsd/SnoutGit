# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import diff_highlighter
import git


class DiffFileWidget(QtGui.QWidget):
    _file_name = str()

    def __init__(self, path, parent=None):
        super(DiffFileWidget, self).__init__(parent)

        self._path = path

        self._diff_veiw = QtGui.QPlainTextEdit(self)
        self._diff_veiw.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self._diff_veiw.setUndoRedoEnabled(False)
        self._highlighter = diff_highlighter.DiffHighlighter(
            self._diff_veiw.document())

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._diff_veiw)
        super(DiffFileWidget, self).setLayout(layout)

    @QtCore.pyqtSlot(str, bool)
    def set_file(self, file_name, diff_with_index=False):
        self._file_name = file_name
        self._update_diff(diff_with_index)

    @QtCore.pyqtSlot()
    def clear(self):
        self._diff_veiw.clear()

    def _update_diff(self, diff_with_index):
        command = ["diff", "-U5", self._file_name]
        if diff_with_index:
            command.insert(1, "--staged")

        self._diff_veiw.setPlainText(
            "\n".join(git.Git().execute_command(command, False))
        )

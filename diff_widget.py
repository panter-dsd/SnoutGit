# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import commit

class DiffWidget(QtGui.QWidget):
    def __init__(self, path, parent = None):
        super(DiffWidget, self).__init__(parent)

        self._path = path

        self._diff_veiw = QtGui.QPlainTextEdit(self)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._diff_veiw)
        super(DiffWidget, self).setLayout(layout)

    @QtCore.Slot(str)
    def set_commit(self, id):
        self._diff_veiw.setPlainText(commit.Commit(self._path, id).diff())

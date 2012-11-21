# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import commit
import re

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


class DiffWidget(QtGui.QWidget):
    _id = str()

    def __init__(self, path, parent = None):
        super(DiffWidget, self).__init__(parent)

        self._path = path

        self._diff_veiw = QtGui.QPlainTextEdit(self)
        self._diff_veiw.setWordWrapMode(QtGui.QTextOption.NoWrap)
        diffHighlighter = DiffHighlighter(self._diff_veiw.document())

        panel = QtGui.QWidget(self)

        self._diff_lines_count_edit = QtGui.QSpinBox(self)
        self._diff_lines_count_edit.valueChanged.connect(self._update_diff)
        self._diff_lines_count_edit.setValue(3)

        panelLayout = QtGui.QHBoxLayout()
        panelLayout.addWidget(QtGui.QLabel("Context strings count"))
        panelLayout.addWidget(self._diff_lines_count_edit)
        panelLayout.addSpacerItem(QtGui.QSpacerItem(0,
                                                    0,
                                                    QtGui.QSizePolicy.Expanding,
                                                    QtGui.QSizePolicy.Preferred))

        panel.setLayout(panelLayout)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(panel)
        layout.addWidget(self._diff_veiw)
        super(DiffWidget, self).setLayout(layout)

    @QtCore.Slot(str)
    def set_commit(self, id):
        self._id = id
        self._update_diff()

    def _update_diff(self):
        self._diff_veiw.setPlainText(commit.Commit(self._path, self._id).diff(self._diff_lines_count_edit.value()))
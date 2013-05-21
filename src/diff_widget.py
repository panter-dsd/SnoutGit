# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import commit
import git
import diff_highlighter


class DiffWidget(QtGui.QWidget):
    _id = str()
    _git = git.Git()

    def __init__(self, path, parent=None):
        super(DiffWidget, self).__init__(parent)

        self._path = path

        self._diff_veiw = QtGui.QPlainTextEdit(self)
        self._diff_veiw.setReadOnly(True)
        self._diff_veiw.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self._diff_veiw.setUndoRedoEnabled(False)
        self._highlighter = diff_highlighter.DiffHighlighter(
            self._diff_veiw.document())

        self._files_list = QtGui.QListWidget(self)
        self._files_list.itemPressed.connect(self._select_file)

        panel = QtGui.QWidget(self)
        panel.setSizePolicy(QtGui.QSizePolicy.Preferred,
                            QtGui.QSizePolicy.Maximum)

        self._diff_lines_count_edit = QtGui.QSpinBox(self)
        self._diff_lines_count_edit.valueChanged.connect(self._update_diff)
        self._diff_lines_count_edit.setValue(3)

        panelLayout = QtGui.QHBoxLayout()
        panelLayout.addWidget(QtGui.QLabel("Context strings count"))
        panelLayout.addWidget(self._diff_lines_count_edit)
        spacer = QtGui.QSpacerItem(0,
                                   0,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Preferred)
        panelLayout.addSpacerItem(spacer)

        panel.setLayout(panelLayout)

        horizontal_split = QtGui.QSplitter(self)
        horizontal_split.addWidget(self._diff_veiw)
        horizontal_split.addWidget(self._files_list)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(panel)
        layout.addWidget(horizontal_split)
        super(DiffWidget, self).setLayout(layout)

    @QtCore.pyqtSlot(str)
    def set_commit(self, id):
        self._id = id
        self._update_diff()

    def _update_diff(self):
        current_commit = commit.Commit(self._git, self._id)
        diff_text = current_commit.diff(self._diff_lines_count_edit.value())
        self._diff_veiw.setPlainText(diff_text)

        self._files_list.clear()
        for file_name in current_commit.changed_files():
            self._files_list.addItem(QtGui.QListWidgetItem(file_name))

    def _select_file(self, item):
        doc = self._diff_veiw.document()
        cursor = doc.find(QtCore.QRegExp("a/" + item.text()))
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        self._diff_veiw.setTextCursor(cursor)
        self._diff_veiw.centerCursor()
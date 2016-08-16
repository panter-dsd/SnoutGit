# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QRegExp
from PyQt5.QtGui import QTextCursor, QTextOption
from PyQt5.QtWidgets import QApplication, QSizePolicy
from diff_highlighter import DiffHighlighter

from ApplicationSettings import application_settings as settings

import commit
import git

__author__ = 'panter.dsd@gmail.com'


class DiffWidget(QtWidgets.QWidget):
    _id = str()
    _git = git.Git()

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self._path = path

        self._diff_viewer = QtWidgets.QPlainTextEdit(self)
        self._diff_viewer.setReadOnly(True)
        self._diff_viewer.setWordWrapMode(QTextOption.NoWrap)
        self._diff_viewer.setUndoRedoEnabled(False)
        self._highlighter = DiffHighlighter(self._diff_viewer.document())

        self.apply_settings()

        self._files_list = QtWidgets.QListWidget(self)
        self._files_list.itemPressed.connect(self._select_file)

        panel = QtWidgets.QWidget(self)
        panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self._diff_lines_count_edit = QtWidgets.QSpinBox(self)
        self._diff_lines_count_edit.valueChanged.connect(self._update_diff)

        self._diff_lines_count_edit.setValue(
            settings.commit_info_context_line_count()
        )

        panel_layout = QtWidgets.QHBoxLayout()
        panel_layout.addWidget(QtWidgets.QLabel("Context strings count"))
        panel_layout.addWidget(self._diff_lines_count_edit)

        spacer = QtWidgets.QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred
        )

        panel_layout.addSpacerItem(spacer)
        panel.setLayout(panel_layout)

        horizontal_split = QtWidgets.QSplitter(self)
        horizontal_split.addWidget(self._diff_viewer)
        horizontal_split.addWidget(self._files_list)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(panel)
        layout.addWidget(horizontal_split)

        self.setLayout(layout)

    def apply_settings(self):
        font = settings.diff_viewer_font()
        self._diff_viewer.setFont(font if font else QApplication.font())
        self._highlighter.update_settings()

    def save_settings(self):
        settings.set_commit_info_context_line_count(
            self._diff_lines_count_edit.value()
        )

    @pyqtSlot(str)
    def set_commit(self, commit_id):
        self._id = commit_id
        self._update_diff()

    def _update_diff(self):
        current_commit = commit.Commit(self._git, self._id)
        diff_text = current_commit.diff(self._diff_lines_count_edit.value())
        self._diff_viewer.setPlainText(diff_text)

        self._files_list.clear()

        for file_name in current_commit.changed_files():
            self._files_list.addItem(QtWidgets.QListWidgetItem(file_name))

    def _select_file(self, item):
        doc = self._diff_viewer.document()
        cursor = doc.find(QRegExp("a/" + item.text()))
        cursor.movePosition(QTextCursor.StartOfLine)
        self._diff_viewer.setTextCursor(cursor)
        self._diff_viewer.centerCursor()

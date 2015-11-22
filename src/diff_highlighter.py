# -*- coding: utf-8 -*-

import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter

from ApplicationSettings import application_settings

__author__ = 'panter.dsd@gmail.com'


class DiffHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._highlighted_line_pattern = re.compile(r'^(@@|\+|-).*$')

        self._line_colors = {
            '@@': application_settings.diff_viewer_range_line_color(),
            '+': application_settings.diff_viewer_added_line_color(),
            '-': application_settings.diff_viewer_removed_line_color(),
        }

    def highlightBlock(self, text):
        match = self._highlighted_line_pattern.match(text)

        if match:
            self.setFormat(
                match.pos, match.endpos, self._line_colors[match.group(1)]
            )

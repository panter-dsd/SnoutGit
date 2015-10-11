# -*- coding: utf-8 -*-

import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter

__author__ = 'panter.dsd@gmail.com'


class DiffHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._highlighted_line_pattern = re.compile(r'^(@@|\+|-).*$')

        self._line_colors = {
            '@@': Qt.blue,
            '+': Qt.darkGreen,
            '-': Qt.darkRed,
        }

    def highlightBlock(self, text):
        match = self._highlighted_line_pattern.match(text)

        if match:
            self.setFormat(
                match.pos, match.endpos, self._line_colors[match.group(1)]
            )

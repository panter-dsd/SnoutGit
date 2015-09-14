# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter


class DiffHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(DiffHighlighter, self).__init__(parent)

    def highlightBlock(self, text):
        added = re.match("^\+.*$", text)
        if added:
            self.setFormat(added.pos, added.endpos, Qt.darkGreen)

        removed = re.match("^\-.*$", text)
        if removed:
            self.setFormat(removed.pos, removed.endpos, Qt.darkRed)

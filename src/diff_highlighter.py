# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import re

from PyQt4 import QtCore, QtGui


class DiffHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(DiffHighlighter, self).__init__(parent)

    def highlightBlock(self, text):
        super(DiffHighlighter, self).setFormat(0, len(text), QtCore.Qt.black)

        added = re.match("^\+.*$", text)
        if added:
            super(DiffHighlighter, self).setFormat(added.pos,
                                                   added.endpos,
                                                   QtCore.Qt.green)

        removed = re.match("^\-.*$", text)
        if removed:
            super(DiffHighlighter, self).setFormat(removed.pos,
                                                   removed.endpos,
                                                   QtCore.Qt.red)

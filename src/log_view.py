# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets


class LogView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LogView, self).__init__(parent)

        self._text_view = QtWidgets.QTextEdit(self)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._text_view)
        super(LogView, self).setLayout(layout)

    def append_command(self, text):
        self._text_view.setHtml(
            self._text_view.toHtml() \
            + "<p style=\"color:white\">" \
            + text.replace("\n", "<BR>") \
            + "</p>"
        )
        self._scroll()

    def append_output(self, text):
        self._text_view.setHtml(
            self._text_view.toHtml() \
            + "<p style=\"color:green\">" \
            + text.replace("\n", "<BR>") \
            + "</p>"
        )
        self._scroll()

    def append_error(self, text):
        self._text_view.setHtml(
            self._text_view.toHtml() \
            + "<p style=\"color:red\">" \
            + text.replace("\n", "<BR>") \
            + "</p>"
        )
        self._scroll()

    def _scroll(self):
        self._text_view.verticalScrollBar().setValue(
            self._text_view.verticalScrollBar().maximum())
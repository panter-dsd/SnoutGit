# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtWidgets import QFontDialog, QPushButton


class FontSelectionButton(QPushButton):
    font_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._font = None

        self.clicked.connect(self._select_font)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        if self._font:
            painter.setFont(self._font)

        painter.drawText(
            self.rect(), Qt.AlignCenter, self._display_font(self._font)
        )

    def font(self):
        return self._font

    def set_font(self, font: QFont):
        self._font = font
        self.update()

        self.font_changed.emit()

    def _select_font(self):
        font, is_selected = QFontDialog.getFont(self._font, self) \
            if self._font else QFontDialog.getFont(self)

        if is_selected:
            self.set_font(font)

    @staticmethod
    def _display_font(font):
        return '{} {}'.format(font.family(), font.pointSize()) \
            if font else 'System default'

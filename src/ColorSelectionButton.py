# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QColorDialog, QPushButton


class ColorSelectionButton(QPushButton):
    color_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = Qt.transparent

        self.clicked.connect(self._select_color)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.fillRect(self._color_label_rect(), self._color)

    def color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        self.update()

        self.color_changed.emit()

    def _color_label_rect(self):
        margin = 5

        return QRect(
            margin,
            margin,
            self.width() - 2 * margin,
            self.height() - 2 * margin
        )

    def _select_color(self):
        self.set_color(QColorDialog.getColor(self._color, self))

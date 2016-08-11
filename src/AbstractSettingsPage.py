# -*- coding: utf-8 -*-

import abc

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class AbstractSettingsPage(QWidget):
    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_loaded = False
        self._has_changes = False

        self.settings_changed.connect(self._on_settings_changed)

    def load_settings(self):
        if not self._is_loaded:
            self.blockSignals(True)
            self._load_settings()
            self.blockSignals(False)

            self._is_loaded = True

    def save_settings(self):
        if self._has_changes:
            self._save_settings()
            self._has_changes = False

    def _on_settings_changed(self):
        self._has_changes = True

    @abc.abstractmethod
    def _load_settings(self):
        pass

    @abc.abstractmethod
    def _save_settings(self):
        pass

# -*- coding: utf-8 -*-

import Uic

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from ApplicationSettings import application_settings as settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Dialog | Qt.WindowCloseButtonHint)
        self._ui = Uic.load_ui_from_file('SettingsDialog.ui', self)
        self._load_settings()

        self._ui.gitCommandLineEdit_.textChanged.connect(
            self._update_buttons_state
        )

    def accept(self):
        self._save_settings()
        super().accept()

    def _load_settings(self):
        self._ui.gitCommandLineEdit_.setText(settings.git_executable_path())
        self._save_button().setEnabled(False)

    def _save_settings(self):
        settings.set_git_executable_path(self._ui.gitCommandLineEdit_.text())

    def _save_button(self):
        return self._ui.buttonBox_.button(QDialogButtonBox.Save)

    def _update_buttons_state(self):
        can_save_settings = len(self._ui.gitCommandLineEdit_.text()) > 0
        self._save_button().setEnabled(can_save_settings)

# -*- coding: utf-8 -*-

import Uic

from AbstractSetingsPage import AbstractSetingsPage

from ApplicationSettings import application_settings as settings


class GeneralSettingsPage(AbstractSetingsPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Uic.load_ui_from_file('GeneralSettingsPage.ui', self)

        self._ui.gitBinaryEdit_.textChanged.connect(self.settings_changed)

    def _load_settings(self):
        self._ui.gitBinaryEdit_.setText(settings.git_executable_path())

    def _save_settings(self):
        settings.set_git_executable_path(self._ui.gitCommandLineEdit_.text())

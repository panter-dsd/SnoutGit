# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont


class ApplicationSettings(object):
    _application = 'SnoutGit'
    _organization = 'PanteR'

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance

    def value(self, key, default_value, scope=QSettings.UserScope):
        return self._settings(scope).value(key, default_value)

    def set_value(self, key, value, scope=QSettings.UserScope):
        self._settings(scope).setValue(key, value)

    def git_executable_path(self):
        return self.value('GitExecutable', 'git')

    def application_font(self):
        return self._font_value('ApplicationFont')

    def diff_viewer_font(self):
        return self._font_value('DiffViewer/Font')

    def commit_info_context_line_count(self):
        return int(self.value('GUI/CommitInfoContextLineCount', 3))

    def set_commit_info_context_line_count(self, value):
        self.set_value('GUI/CommitInfoContextLineCount', value)

    def _settings(self, scope=QSettings.UserScope):
        return QSettings(scope, self._organization, self._application)

    def _font_value(self, key, scope=QSettings.UserScope):
        value = self.value(key, None, scope)
        font = None

        if type(value) is str:
            font = self._font_from_string(value)
        elif type(value) is list:
            font = self._font_from_string(','.join(value))

        return font

    @staticmethod
    def _font_from_string(value):
        font = QFont()
        return font if font.fromString(value) else None


application_settings = ApplicationSettings()

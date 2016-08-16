# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QColor, QFont


class ApplicationSettings(object):
    _application = 'SnoutGit'
    _organization = 'PanteR'

    _default_values = {
        'GitExecutable': 'git',
        'ApplicationFont': None,
        'DiffViewer/Font': None,
        'DiffViewer/RangeLineColor': QColor(Qt.blue),
        'DiffViewer/AddedLineColor': QColor(Qt.darkGreen),
        'DiffViewer/RemovedLineColor': QColor(Qt.darkRed),
        'GUI/CommitInfoContextLineCount': 3,
    }

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance

    def value(self, key, scope=QSettings.UserScope):
        return self._settings(scope).value(key, self.default_value(key))

    def set_value(self, key, value, scope=QSettings.UserScope):
        self._settings(scope).setValue(key, value)

    def default_value(self, key):
        return self._default_values.get(key, None)

    def git_executable_path(self):
        return self.value('GitExecutable')

    def set_git_executable_path(self, path):
        self.set_value('GitExecutable', path)

    def application_font(self):
        return self._font_value('ApplicationFont')

    def diff_viewer_font(self):
        return self._font_value('DiffViewer/Font')

    def set_diff_viewer_font(self, font):
        self.set_value('DiffViewer/Font', font.toString() if font else None)

    def diff_viewer_range_line_color(self):
        return self._color_value('DiffViewer/RangeLineColor')

    def set_diff_viewer_range_line_color(self, color):
        return self._set_color_value('DiffViewer/RangeLineColor', color)

    def diff_viewer_added_line_color(self):
        return self._color_value('DiffViewer/AddedLineColor')

    def set_diff_viewer_added_line_color(self, color):
        return self._set_color_value('DiffViewer/AddedLineColor', color)

    def diff_viewer_removed_line_color(self):
        return self._color_value('DiffViewer/RemovedLineColor')

    def set_diff_viewer_removed_line_color(self, color):
        return self._set_color_value('DiffViewer/RemovedLineColor', color)

    def commit_info_context_line_count(self):
        return int(self.value('GUI/CommitInfoContextLineCount'))

    def set_commit_info_context_line_count(self, value):
        self.set_value('GUI/CommitInfoContextLineCount', value)

    def _settings(self, scope=QSettings.UserScope):
        return QSettings(scope, self._organization, self._application)

    def _color_value(self, key, scope=QSettings.UserScope):
        value = self.value(key, scope)
        color = None

        if type(value) is str:
            color = QColor(value)
        elif type(value) is list and (len(value) > 2):
            color = QColor(*[int(item) for item in value])

        return color if color else self.default_value(key)

    def _set_color_value(self, key, value, scope=QSettings.UserScope):
        color_value = [value.red(), value.green(), value.blue(), value.alpha()]
        self.set_value(key, color_value, scope)

    def _font_value(self, key, scope=QSettings.UserScope):
        value = self.value(key, scope)
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

# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import qApp


class ApplicationSettings(object):
    _application = qApp.applicationName()
    _organization = qApp.organizationName()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance

    def value(self, key, default_value, scope=QSettings.UserScope):
        return self._settings(scope).value(key, default_value)

    def set_value(self, key, value, scope=QSettings.UserScope):
        self._settings(scope).setValue(key, value)

    @property
    def git_executable_path(self):
        return self.value('git_executable_path', 'git')

    def _settings(self, scope):
        return QSettings(scope, self._organization, self._application)


application_settings = ApplicationSettings()

# -*- coding: utf-8 -*-

import Uic

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from ColorSelectionButton import ColorSelectionButton

from ApplicationSettings import application_settings as settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Dialog | Qt.WindowCloseButtonHint)
        self._ui = Uic.load_ui_from_file('SettingsDialog.ui', self)
        self._range_line_color_selection_button = ColorSelectionButton(self)
        self._added_line_color_selection_button = ColorSelectionButton(self)
        self._removed_line_color_selection_button = ColorSelectionButton(self)
        self._insert_color_selection_buttons()

        self._load_settings()

        self._ui.gitCommandLineEdit_.textChanged.connect(
            self._update_buttons_state
        )

        for button in self.findChildren(ColorSelectionButton):
            button.color_changed.connect(self._update_buttons_state)

    def accept(self):
        self._save_settings()
        super().accept()

    def _load_settings(self):
        self._load_general_settings()
        self._load_diff_viewer_settings()
        self._ok_button().setEnabled(False)

    def _save_settings(self):
        self._save_general_settings()
        self._save_diff_viewer_settings()

    def _load_general_settings(self):
        self._ui.gitCommandLineEdit_.setText(settings.git_executable_path())

    def _save_general_settings(self):
        settings.set_git_executable_path(self._ui.gitCommandLineEdit_.text())

    def _load_diff_viewer_settings(self):
        self._range_line_color_selection_button.set_color(
            settings.diff_viewer_range_line_color()
        )

        self._added_line_color_selection_button.set_color(
            settings.diff_viewer_added_line_color()
        )

        self._removed_line_color_selection_button.set_color(
            settings.diff_viewer_removed_line_color()
        )

    def _save_diff_viewer_settings(self):
        settings.set_diff_viewer_range_line_color(
            self._range_line_color_selection_button.color()
        )

        settings.set_diff_viewer_added_line_color(
            self._added_line_color_selection_button.color()
        )

        settings.set_diff_viewer_removed_line_color(
            self._removed_line_color_selection_button.color()
        )

    def _ok_button(self):
        return self._ui.buttonBox_.button(QDialogButtonBox.Ok)

    def _update_buttons_state(self):
        can_save_settings = len(self._ui.gitCommandLineEdit_.text()) > 0
        self._ok_button().setEnabled(can_save_settings)

    def _insert_color_selection_buttons(self):
        layout = self._ui.diffViewerSettingsTab_.layout()
        layout.addWidget(self._range_line_color_selection_button, 0, 1)
        layout.addWidget(self._added_line_color_selection_button, 1, 1)
        layout.addWidget(self._removed_line_color_selection_button, 2, 1)

# -*- coding: utf-8 -*-

import Uic

from AbstractSettingsPage import AbstractSettingsPage
from ColorSelectionButton import ColorSelectionButton
from FontSelectionButton import FontSelectionButton

from ApplicationSettings import application_settings as settings


class DiffViewerSettingsPage(AbstractSettingsPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Uic.load_ui_from_file('DiffViewerSettingsPage.ui', self)
        self._insert_selection_buttons()

        for button in self.findChildren(ColorSelectionButton):
            button.color_changed.connect(self.settings_changed)

        for button in self.findChildren(FontSelectionButton):
            button.font_changed.connect(self.settings_changed)

    def restore_defaults(self):
        self._font_selection_button.set_font(
            settings.default_value('DiffViewer/Font')
        )

        self._range_line_color_selection_button.set_color(
            settings.default_value('DiffViewer/RangeLineColor')
        )

        self._added_line_color_selection_button.set_color(
            settings.default_value('DiffViewer/AddedLineColor')
        )

        self._removed_line_color_selection_button.set_color(
            settings.default_value('DiffViewer/RemovedLineColor')
        )

    def _load_settings(self):
        self._font_selection_button.set_font(settings.diff_viewer_font())

        self._range_line_color_selection_button.set_color(
            settings.diff_viewer_range_line_color()
        )

        self._added_line_color_selection_button.set_color(
            settings.diff_viewer_added_line_color()
        )

        self._removed_line_color_selection_button.set_color(
            settings.diff_viewer_removed_line_color()
        )

    def _save_settings(self):
        settings.set_diff_viewer_font(self._font_selection_button.font())

        settings.set_diff_viewer_range_line_color(
            self._range_line_color_selection_button.color()
        )

        settings.set_diff_viewer_added_line_color(
            self._added_line_color_selection_button.color()
        )

        settings.set_diff_viewer_removed_line_color(
            self._removed_line_color_selection_button.color()
        )

    def _insert_selection_buttons(self):
        layout = self._ui.frame_.layout()

        self._font_selection_button = FontSelectionButton(self)
        layout.addWidget(self._font_selection_button, 0, 1)

        self._range_line_color_selection_button = ColorSelectionButton(self)
        layout.addWidget(self._range_line_color_selection_button, 1, 1)

        self._added_line_color_selection_button = ColorSelectionButton(self)
        layout.addWidget(self._added_line_color_selection_button, 2, 1)

        self._removed_line_color_selection_button = ColorSelectionButton(self)
        layout.addWidget(self._removed_line_color_selection_button, 3, 1)

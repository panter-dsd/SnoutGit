# -*- coding: utf-8 -*-

import Uic

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from GeneralSettingsPage import GeneralSettingsPage
from DiffViewerSettingsPage import DiffViewerSettingsPage
from SettingsPageModel import SettingsPageModel


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Dialog | Qt.WindowCloseButtonHint)
        self._ui = Uic.load_ui_from_file('SettingsDialog.ui', self)
        self._page_model = SettingsPageModel(self)

        self._add_page(self.tr('General'), GeneralSettingsPage(self))
        self._add_page(self.tr('Diff viewer'), DiffViewerSettingsPage(self))

        self._ui.pageListView_.setModel(self._page_model)

        self._ui.pageListView_.selectionModel().currentChanged.connect(
            self._set_current_page
        )

        self._ui.buttonBox_.clicked.connect(self._on_buttonbox_clicked)

        self._apply_button().setDisabled(True)

    def accept(self):
        self._save_settings()
        super().accept()

    def _apply_button(self):
        return self._ui.buttonBox_.button(QDialogButtonBox.Apply)

    def _add_page(self, title, page):
        self._page_model.add_page(title, page)
        self._ui.stackedWidget_.addWidget(page)

        page.settings_changed.connect(
            lambda: self._apply_button().setEnabled(True)
        )

    def _current_page(self):
        return self._ui.stackedWidget_.currentWidget()

    def _set_current_page(self, index):
        page = self._page_model.page(index)
        page_index = self._ui.stackedWidget_.indexOf(page)

        self._ui.pageTitle_.setText(str(index.data()))
        self._ui.stackedWidget_.setCurrentIndex(page_index)
        self._current_page().load_settings()

    def _save_settings(self):
        for i in range(self._ui.stackedWidget_.count()):
            self._ui.stackedWidget_.widget(i).save_settings()

        self._apply_button().setDisabled(True)

    def _on_buttonbox_clicked(self, button):
        standard_button = self._ui.buttonBox_.standardButton(button)

        if standard_button == QDialogButtonBox.Ok:
            self.accept()
        elif standard_button == QDialogButtonBox.Apply:
            self._save_settings()
            self.accepted.emit()
        elif standard_button == QDialogButtonBox.Cancel:
            self.reject()
        elif standard_button == QDialogButtonBox.RestoreDefaults:
            self._current_page().restore_defaults()

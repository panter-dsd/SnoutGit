# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex


class SettingsPageModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._page_items = list()

    def rowCount(self, parent=QModelIndex()):
        return len(self._page_items)

    def data(self, index, role=Qt.DisplayRole):
        return self._page_items[index.row()]['title'] \
            if index.isValid() and role == Qt.DisplayRole else None

    def page(self, index):
        return self._page_items[index.row()]['page'] \
            if index.isValid() else None

    def add_page(self, title, page):
        self._page_items.append({
            'title': title,
            'page': page,
        })

# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QFile, QTimer
from PyQt5.QtGui import QIcon

import git


class StatusWidget(QtWidgets.QWidget):
    current_file_changed = pyqtSignal(str, bool)
    status_changed = pyqtSignal()

    _git = git.Git()
    _path = str()
    _last_status = []

    def __init__(self, parent):
        super(StatusWidget, self).__init__(parent)

        self._files_view = QtWidgets.QTreeWidget(self)
        self._files_view.setHeaderHidden(True)
        self._files_view.itemDoubleClicked.connect(
            self._change_item_status
        )
        self._files_view.currentItemChanged.connect(
            self._current_item_changed
        )

        self._files_view.setContextMenuPolicy(Qt.CustomContextMenu)

        self._files_view.customContextMenuRequested.connect(
            self._show_menu
        )
        self._files_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )

        self._unstaged = QtWidgets.QTreeWidgetItem(self._files_view)
        self._unstaged.setText(0, "Unstaged")

        self._staged = QtWidgets.QTreeWidgetItem(self._files_view)
        self._staged.setText(0, "Staged")

        self._untracked = QtWidgets.QTreeWidgetItem(self._files_view)
        self._untracked.setText(0, "Untracked")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._files_view)
        super(StatusWidget, self).setLayout(layout)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._update_file_list)
        self.update_timer.start(1000)

    def _save_status_in_item(self, item, status):
        item.setData(0, Qt.UserRole, status)

    def _extract_status_from_item(self, item):
        return item.data(0, Qt.UserRole)

    def _update_file_list(self):
        images_path = os.path.dirname(__file__) + "/../share/images/"

        new_icon = QIcon(images_path + "add.png")
        changed_icon = QIcon(images_path + "edit.png")
        updated_but_unmerged = QIcon(
            super(StatusWidget, self).style().standardIcon(
                QtWidgets.QStyle.SP_DialogSaveButton
            ))
        deleted_icon = QIcon(images_path + "remove.png")

        icons = {
            'A': new_icon,
            'M': changed_icon,
            'U': updated_but_unmerged,
            'D': deleted_icon,
        }

        current_status = self._git.get_status()
        if self._last_status == current_status:
            return

        self._last_status = current_status

        self._staged.takeChildren()
        self._unstaged.takeChildren()
        self._untracked.takeChildren()

        for status_line in self._last_status:
            print(status_line)
            status = status_line[:2]
            file_name = status_line[3:]

            item = QtWidgets.QTreeWidgetItem()
            self._save_status_in_item(item, status)
            item.setText(0, file_name)

            if status[0] == '?' or status[1] == '?':
                item.setIcon(0, new_icon)
                self._untracked.addChild(item)
            elif status[0] == 'R':
                names = file_name.split(" -> ")
                item.setText(0, names[0])
                item.setIcon(0, deleted_icon)
                self._staged.addChild(item)
                if status[1] == "M":
                    parent = self._unstaged
                else:
                    parent = self._staged
                item_ = QtWidgets.QTreeWidgetItem(parent)
                item_.setText(0, names[1])
                item_.setIcon(0, new_icon)
                self._save_status_in_item(item_, status)
            else:
                if not status[0] in [' ', 'U']:
                    item = QtWidgets.QTreeWidgetItem(self._staged)
                    self._save_status_in_item(item, status)
                    item.setText(0, file_name)
                    item.setIcon(0, icons[status[0]])

                if status[1] != ' ':
                    item = QtWidgets.QTreeWidgetItem(self._unstaged)
                    self._save_status_in_item(item, status)
                    item.setText(0, file_name)
                    item.setIcon(0, icons[status[1]])

        self._files_view.expandAll()
        self.status_changed.emit()

    def _change_item_status(self, item):
        if item.parent() is self._unstaged:
            self._stage_items([item])
        elif item.parent() is self._staged:
            self._unstage_items([item])
        elif item.parent() is self._untracked:
            self._add_items([item])

    def _current_item_changed(self, current, _prev):
        if current and current.parent():
            self.current_file_changed.emit(
                current.text(0),
                current.parent() is self._staged
            )

    def is_in_item_list(self, item, item_list):
        result = False
        for _item in item_list:
            if _item is item:
                result = True
                break
        return result

    def _show_menu(self, point):
        items = self._files_view.selectedItems()

        menu = QtWidgets.QMenu(self)

        self._stage_all_action = QtWidgets.QAction(self)
        self._stage_all_action.setText("Stage all")
        self._stage_all_action.triggered.connect(self._stage_all)

        self._unstage_all_action = QtWidgets.QAction(self)
        self._unstage_all_action.setText("Unstage all")
        self._unstage_all_action.triggered.connect(self._unstage_all)

        self._add_all_action = QtWidgets.QAction(self)
        self._add_all_action.setText("Add all")
        self._add_all_action.triggered.connect(self._add_all)

        self._stage_selected_action = QtWidgets.QAction(self)
        self._stage_selected_action.setText("Stage selected")
        self._stage_selected_action.triggered.connect(
            self._stage_selected
        )

        self._unstage_selected_action = QtWidgets.QAction(self)
        self._unstage_selected_action.setText("Unstage selected")
        self._unstage_selected_action.triggered.connect(
            self._unstage_selected
        )

        self._add_selected_action = QtWidgets.QAction(self)
        self._add_selected_action.setText("Add selected")
        self._add_selected_action.triggered.connect(
            self._add_selected
        )

        self._revert_selected_action = QtWidgets.QAction(self)
        self._revert_selected_action.setText("Revert selected")
        self._revert_selected_action.triggered.connect(
            self._revert_selected
        )

        self._remove_selected_action = QtWidgets.QAction(self)
        self._remove_selected_action.setText("Remove selected")
        self._remove_selected_action.triggered.connect(
            self._remove_selected
        )

        if self.is_in_item_list(self._unstaged, items):
            if self._unstaged.childCount() > 0:
                menu.addAction(self._stage_all_action)

        if self.is_in_item_list(self._staged, items):
            if self._staged.childCount() > 0:
                menu.addAction(self._unstage_all_action)

        if self.is_in_item_list(self._untracked, items):
            if self._untracked.childCount() > 0:
                menu.addAction(self._add_all_action)

        if menu.actions():
            menu.addSeparator()

        for item in items:
            if item.parent() is self._unstaged:
                if not self._stage_selected_action in menu.actions():
                    menu.addAction(self._stage_selected_action)
                    menu.addAction(self._revert_selected_action)
                    menu.addAction(self._remove_selected_action)

            if item.parent() is self._staged:
                if not self._unstage_selected_action in menu.actions():
                    menu.addAction(self._unstage_selected_action)
                    menu.addAction(self._remove_selected_action)

            if item.parent() is self._untracked:
                if not self._add_selected_action in menu.actions():
                    menu.addAction(self._add_selected_action)
                    menu.addAction(self._remove_selected_action)

        if menu.actions():
            menu.exec_(self.mapToGlobal(point))

    def _child_items(self, parent):
        items = []
        for i in range(parent.childCount()):
            items.append(parent.child(i))
        return items

    def _stage_all(self):
        self._stage_items(self._child_items(self._unstaged))

    def _unstage_all(self):
        self._unstage_items(self._child_items(self._staged))

    def _add_all(self):
        self._add_items(self._child_items(self._untracked))

    def _stage_selected(self):
        self._stage_items(self._files_view.selectedItems())

    def _unstage_selected(self):
        self._unstage_items(self._files_view.selectedItems())

    def _add_selected(self):
        self._add_items(self._files_view.selectedItems())

    def _revert_selected(self):
        self._revert_items(self._files_view.selectedItems())

    def _remove_selected(self):
        self._remove_items(self._files_view.selectedItems())

    def _stage_items(self, items):
        files_to_add = []
        files_to_remove = []
        for item in items:
            if item.parent() is self._unstaged:
                status = self._extract_status_from_item(item)
                if status[1] == "D":
                    files_to_remove.append(item.text(0))
                else:
                    files_to_add.append(item.text(0))

        self._git.stage_files(files_to_add)
        self._git.remove_files(files_to_remove)

        self._update_file_list()

    def _unstage_items(self, items):
        files_list = []
        for item in items:
            if item.parent() is self._staged:
                files_list.append(item.text(0))

        self._git.unstage_files(files_list)

        self._update_file_list()

    def _add_items(self, items):
        files_list = []
        for item in items:
            if item.parent() is self._untracked:
                files_list.append(item.text(0))

        self._git.stage_files(files_list)

        self._update_file_list()

    def _revert_items(self, items):
        files_list = []
        for item in items:
            if item.parent() is self._unstaged:
                files_list.append(item.text(0))

        self._git.revert_files(files_list)

        self._update_file_list()

    def _remove_items(self, items):
        for item in items:
            if item.parent():
                QFile.remove(item.text(0))

        self._update_file_list()

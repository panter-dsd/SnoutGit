# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import git


class StatusWidget(QtGui.QWidget):
    current_file_changed = QtCore.Signal(str)
    status_changed = QtCore.Signal()

    _path = str()
    _last_status = []

    def __init__(self, parent):
        super(StatusWidget, self).__init__(parent)

        self._files_view = QtGui.QTreeWidget(self)
        self._files_view.setHeaderHidden(True)
        self._files_view.itemDoubleClicked.connect(self._change_item_status)
        self._files_view.currentItemChanged.connect(self._current_item_changed)
        self._files_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._files_view.customContextMenuRequested.connect(self._show_menu)
        self._files_view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self._unstaged = QtGui.QTreeWidgetItem(self._files_view)
        self._unstaged.setText(0, "Unstaged")

        self._staged = QtGui.QTreeWidgetItem(self._files_view)
        self._staged.setText(0, "Staged")

        self._untracked = QtGui.QTreeWidgetItem(self._files_view)
        self._untracked.setText(0, "Untracked")

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._files_view)
        super(StatusWidget, self).setLayout(layout)

        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self._update_file_list)
        self.update_timer.start(1000)

    def _update_file_list(self):
        current_status = git.Git().get_status()
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

            if not status[0] in [' ', '?']:
                item = QtGui.QTreeWidgetItem(self._staged)
                item.setText(0, file_name)

            if not status[1] in [' ', '?']:
                item = QtGui.QTreeWidgetItem(self._unstaged)
                item.setText(0, file_name)

            if status[0] == '?' or status[1] == '?':
                item = QtGui.QTreeWidgetItem(self._untracked)
                item.setText(0, file_name)

        self._files_view.expandAll()
        self.status_changed.emit()

    def _change_item_status(self, item):
        if item.parent() is self._unstaged:
            git.Git().stage(item.text(0))
        elif item.parent() is self._staged:
            git.Git().unstage(item.text(0))
        elif item.parent() is self._untracked:
            git.Git().stage(item.text(0))
        self._update_file_list()

    def _current_item_changed(self, current, _prev):
        if current and current.parent():
            self.current_file_changed.emit(current.text(0))

    def is_in_item_list(self, item, item_list):
        result = False
        for _item in item_list:
            if _item is item:
                result = True
                break
        return result

    def _show_menu(self, point):
        items = self._files_view.selectedItems()

        menu = QtGui.QMenu(self)

        self._stage_all_action = QtGui.QAction(self)
        self._stage_all_action.setText("Stage all")
        self._stage_all_action.triggered.connect(self._stage_all)

        self._unstage_all_action = QtGui.QAction(self)
        self._unstage_all_action.setText("Unstage all")
        self._unstage_all_action.triggered.connect(self._unstage_all)

        self._add_all_action = QtGui.QAction(self)
        self._add_all_action.setText("Add all")
        self._add_all_action.triggered.connect(self._add_all)

        self._stage_selected_action = QtGui.QAction(self)
        self._stage_selected_action.setText("Stage selected")
        self._stage_selected_action.triggered.connect(self._stage_selected)

        self._unstage_selected_action = QtGui.QAction(self)
        self._unstage_selected_action.setText("Unstage selected")
        self._unstage_selected_action.triggered.connect(self._unstage_selected)

        self._add_selected_action = QtGui.QAction(self)
        self._add_selected_action.setText("Add selected")
        self._add_selected_action.triggered.connect(self._add_selected)

        if self.is_in_item_list(self._unstaged, items):
            if self._unstaged.childCount() > 0:
                menu.addAction(self._stage_all_action)

        if self.is_in_item_list(self._staged, items):
            if self._staged.childCount() > 0:
                menu.addAction(self._unstage_all_action)

        if self.is_in_item_list(self._untracked, items):
            if self._untracked.childCount() > 0:
                menu.addAction(self._add_all_action)

        if len(menu.actions()) > 0:
            menu.addSeparator()

        for item in items:
            if item.parent() is self._unstaged:
                if not self._stage_selected_action in menu.actions():
                    menu.addAction(self._stage_selected_action)

            if item.parent() is self._staged:
                if not self._unstage_selected_action in menu.actions():
                    menu.addAction(self._unstage_selected_action)

            if item.parent() is self._untracked:
                if not self._add_selected_action in menu.actions():
                    menu.addAction(self._add_selected_action)

        if len(menu.actions()) > 0:
            menu.exec_(self.mapToGlobal(point))

    def _stage_all(self):
        files_list = []
        for i in range(self._unstaged.childCount()):
            files_list.append(self._unstaged.child(i).text(0))

        for file_name in files_list:
            git.Git().stage(file_name)

        self._update_file_list()

    def _unstage_all(self):
        files_list = []
        for i in range(self._staged.childCount()):
            files_list.append(self._staged.child(i).text(0))

        for file_name in files_list:
            git.Git().unstage(file_name)

        self._update_file_list()

    def _add_all(self):
        files_list = []
        for i in range(self._untracked.childCount()):
            files_list.append(self._untracked.child(i).text(0))

        for file_name in files_list:
            git.Git().stage(file_name)

        self._update_file_list()

    def _stage_selected(self):
        files_list = []
        for item in self._files_view.selectedItems():
            if item.parent() is self._unstaged:
                files_list.append(item.text(0))

        for file_name in files_list:
            git.Git().stage(file_name)

        self._update_file_list()

    def _unstage_selected(self):
        files_list = []
        for item in self._files_view.selectedItems():
            if item.parent() is self._staged:
                files_list.append(item.text(0))

        for file_name in files_list:
            git.Git().unstage(file_name)

        self._update_file_list()

    def _add_selected(self):
        files_list = []
        for item in self._files_view.selectedItems():
            if item.parent() is self._untracked:
                files_list.append(item.text(0))

        for file_name in files_list:
            git.Git().stage(file_name)

        self._update_file_list()

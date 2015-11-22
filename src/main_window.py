# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QByteArray, QSettings, QSize

from commites_widget import CommitesWidget
from diff_widget import DiffWidget
from status_widget import StatusWidget
from diff_file_widget import DiffFileWidget
from commit_widget import CommitWidget
from actions_widget import ActionsWidget
from log_view import LogView
from git import Git
from branches_widget import BranchesWidget
from stashes_widget import StashesWidget
from merge_dialog import MergeDialog
from add_remote_dialog import AddRemoteDialog
from remove_remote_dialog import RemoveRemoteDialog
from pull_dialog import PullDialog
from push_dialog import PushDialog
from commites_model import CommitesModel
from git_flow_menu import GitFlowMenu
from SettingsDialog import SettingsDialog

__author__ = 'panter.dsd@gmail.com'


class State(object):
    _name = str()
    _data = None

    def __init__(self, name=str(), data=None):
        super().__init__()

        self._name = name
        self._data = data

    def name(self):
        return self._name

    def data(self):
        return self._data

    def empty(self):
        return len(self._name) == 0


class States(object):
    _states = []

    def __init__(self):
        super().__init__()

    def states_count(self):
        return len(self._states)

    def state(self, index):
        return self._states[index]

    def state_for_name(self, name):
        for state in self._states:
            if state.name() == name:
                return state

        return State()

    def append_state(self, name, data):
        self._states.append(State(name, data))

    def remove_state(self, state):
        self.remove_state_by_name(state.name())

    def remove_state_by_name(self, name):
        for state in self._states:
            if state.name() == name:
                self._states.remove(state)
                break

    def rename_state(self, old_name, new_name):
        for state in self._states:
            if state.name() == old_name:
                state._name = new_name
                break

    def update_state(self, name, data):
        for state in self._states:
            if state.name() == name:
                state._data = data
                break


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._states = States()
        self._current_state = State()
        self._git = Git()
        self._commites_model = CommitesModel(self._git, self)

        self._create_docks()

        self._commites_widget.current_commit_changed.connect(
            self._diff_widget.set_commit
        )

        self._status_widget.current_file_changed.connect(
            self._diff_file_widget.set_file
        )
        self._status_widget.status_changed.connect(
            self._diff_file_widget.clear
        )

        self._commit_widget.commited.connect(
            self._commites_model.update_commits_list
        )

        self._actions_widget.state_changed.connect(
            self._commites_model.update_commits_list
        )

        self._load_settings()
        if self._states.states_count() == 0:
            self._init_default_state()
        self._create_main_menu()
        self._create_exit_action()
        self._update_title()

    def _init_default_state(self):
        self._states.append_state("Default", bytes())
        self._current_state = self._states.state(0)

    def _create_docks(self):
        top_area = Qt.TopDockWidgetArea
        bottom_area = Qt.BottomDockWidgetArea
        self.addDockWidget(bottom_area, self._create_log_view_dock())
        self.addDockWidget(top_area, self._create_commites_dock())
        self.addDockWidget(bottom_area, self._create_diff_dock())
        self.addDockWidget(top_area, self._create_status_dock())
        self.addDockWidget(top_area, self._create_diff_file_widget_dock())
        self.addDockWidget(bottom_area, self._create_commit_widget_dock())
        self.addDockWidget(bottom_area, self._create_actions_widget_dock())
        self.addDockWidget(bottom_area, self._create_branches_widget_dock())
        self.addDockWidget(bottom_area, self._create_stashes_widget_dock())

    def _create_dock(self, widget, object_name, title=str()):
        dock = QtWidgets.QDockWidget(self)
        dock.setObjectName(object_name)
        dock.setWindowTitle(title)
        dock.setWidget(widget)
        return dock

    def _create_commites_dock(self):
        self._commites_widget = CommitesWidget(self._commites_model, self)

        return self._create_dock(
            self._commites_widget, "CommitesDock", "Commites tree"
        )

    def _create_diff_dock(self):
        self._diff_widget = DiffWidget(self)

        return self._create_dock(
            self._diff_widget, "DiffDock", "Commit info"
        )

    def _create_status_dock(self):
        self._status_widget = StatusWidget(self)

        return self._create_dock(
            self._status_widget, "StatusDock", "Status"
        )

    def _create_diff_file_widget_dock(self):
        self._diff_file_widget = DiffFileWidget(self)

        return self._create_dock(
            self._diff_file_widget, "DiffFileDock", "Diff"
        )

    def _create_commit_widget_dock(self):
        self._commit_widget = CommitWidget(self._commites_model)

        return self._create_dock(
            self._commit_widget, "CommitDock", "Commit"
        )

    def _create_actions_widget_dock(self):
        self._actions_widget = ActionsWidget(self)

        return self._create_dock(
            self._actions_widget, "ActionsDock", "Actions"
        )

    def _create_log_view_dock(self):
        self._log_view = LogView(self)
        Git.log_view = self._log_view

        return self._create_dock(self._log_view, "LogView", "Log")

    def _create_branches_widget_dock(self):
        self._branches_widget = BranchesWidget(self)
        return self._create_dock(
            self._branches_widget, "BranchesWidget", "Branches"
        )

    def _create_stashes_widget_dock(self):
        self._stashes_widget = StashesWidget(self)

        stashes_dock = self._create_dock(self._stashes_widget, "StashesWidget")
        self._stashes_widget.state_changed.connect(
            lambda: stashes_dock.setWindowTitle(
                "Stashes ({0})".format(self._stashes_widget.count())
            )
        )
        self._stashes_widget.update_stashes_list()

        return stashes_dock

    def _create_main_menu(self):
        self._menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self._menu_bar)
        self._menu_bar.addMenu(self._stashes_widget.menu())
        self._menu_bar.addMenu(self._make_settings_menu())
        self._menu_bar.addMenu(self._make_actions_menu())
        self._menu_bar.addMenu(self._make_remote_menu())

        self._git_flow = GitFlowMenu(self)
        self._menu_bar.addMenu(self._git_flow)

    def _create_exit_action(self):
        exit_action = QtWidgets.QAction(self)
        exit_action.setShortcut(Qt.CTRL | Qt.Key_Q)
        exit_action.triggered.connect(self.close)
        self.addAction(exit_action)

    def _update_title(self):
        self.setWindowTitle("Branch: " + Git().current_branch())

    def _save_state(self):
        state_name = QtWidgets.QInputDialog.getText(
            self, "Save state", "StateName"
        )[0]

        if state_name:
            self._states.append_state(state_name, self.saveState())
            self._current_state = self._states.state_for_name(state_name)
            self._update_states_menu()

    def _select_state(self):
        states = []

        for i in range(self._states.states_count()):
            states.append(self._states.state(i).name())

        if states:
            state_name = QtWidgets.QInputDialog.getItem(
                self, "Save state", "State name", states, 0, False
            )[0]

            return self._states.state_for_name(state_name)

    def _remove_state(self):
        state = self._select_state()

        if state.name():
            self._states.remove_state(state)
            self._update_states_menu()

    def _rename_state(self):
        state = self._select_state()
        if state.name():
            state_name = QtWidgets.QInputDialog.getText(
                self, "Rename state", "State name"
            )[0]

            if state_name:
                self._states.rename_state(state.name(), state_name)
                self._update_states_menu()

    def _update_state(self):
        state = self._select_state()

        if state.name():
            self._states.update_state(state.name(), self.saveState())
            self._update_states_menu()

    def _update_states_menu(self):
        self._states_menu.clear()
        self._states_menu.addAction(self._save_state_action)
        self._states_menu.addAction(self._update_state_action)
        self._states_menu.addAction(self._rename_state_action)
        self._states_menu.addAction(self._remove_state_action)
        self._states_menu.addSeparator()

        enabled = self._states.states_count() > 0
        self._update_state_action.setEnabled(enabled)
        self._rename_state_action.setEnabled(enabled)
        self._remove_state_action.setEnabled(enabled)

        for i in range(self._states.states_count()):
            state = self._states.state(i)
            action = self._make_action(state.name(), self._restore_state)
            action.setCheckable(True)
            self._states_menu.addAction(action)

            if state.name() == self._current_state.name():
                action.setChecked(True)

    def _restore_state(self):
        state_name = self.sender().text()
        print(state_name)
        self._current_state = self._states.state_for_name(state_name)
        self.restoreState(self._current_state.data())
        self._update_states_menu()

    def closeEvent(self, event):
        self._save_settings()
        event.accept()

    def _load_settings(self):
        settings = QSettings()

        settings.beginGroup("GUI")
        settings.beginGroup("MainWindow")

        self.restoreState(settings.value("State", QByteArray()))

        if settings.contains("pos"):
            self.move(settings.value("pos"))

        size = settings.value("size", QSize(1024, 768))

        self.resize(size)

        is_maximized = settings.value("IsMaximized", False) == "true"

        if is_maximized:
            self.setWindowState(Qt.WindowMaximized)

        settings.endGroup()

        states_count = settings.beginReadArray("States")

        for i in range(states_count):
            settings.setArrayIndex(i)
            self._states.append_state(
                settings.value("Name"),
                settings.value("Data"))

        settings.endArray()

        state_name = settings.value("CurrentState", str())

        if state_name:
            self._current_state = self._states.state_for_name(state_name)
            self.restoreState(self._current_state.data())

        settings.endGroup()

    def _save_settings(self):
        settings = QSettings()

        settings.beginGroup("GUI")
        settings.beginGroup("MainWindow")

        if self.windowState() != Qt.WindowMaximized:
            settings.setValue("pos", self.pos())
            settings.setValue("size", self.size())
            settings.setValue("IsMaximized", False)
        else:
            settings.setValue("IsMaximized", True)

        settings.endGroup()

        settings.beginWriteArray("States")

        for i in range(self._states.states_count()):
            settings.setArrayIndex(i)
            state = self._states.state(i)
            settings.setValue("Name", state.name())
            settings.setValue("Data", state.data())

        settings.endArray()

        if not self._current_state.empty():
            settings.setValue("CurrentState", self._current_state.name())
        else:
            settings.remove("CurrentState")

        settings.endGroup()

        self._diff_widget.save_settings()

    def _merge(self):
        dialog = MergeDialog(self)
        dialog.exec_()

    def _abort_merge(self):
        result = QtWidgets.QMessageBox.question(
            self,
            "Are you sure?",
            "Abort merge",
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )

        if result == QtWidgets.QMessageBox.Ok:
            self._git.abort_merge()

    def _add_remote(self):
        dialog = AddRemoteDialog(self)
        dialog.exec_()

    def _remove_remote(self):
        dialog = RemoveRemoteDialog(self)
        dialog.exec_()

    def _pull_remote(self):
        dialog = PullDialog(self)
        dialog.exec_()

    def _push_remote(self):
        dialog = PushDialog(self)
        dialog.exec_()

    def _make_action(self, caption, slot):
        action = QtWidgets.QAction(self)
        action.setText(caption)
        action.triggered.connect(slot)
        return action

    def _make_menu(self, title, actions):
        menu = QtWidgets.QMenu(self)
        menu.setTitle(title)

        for action in actions:
            menu.addAction(self._make_action(action[0], action[1]))

        return menu

    def _make_remote_menu(self):
        return self._make_menu(
            "Remote",
            [
                ("Add remote", self._add_remote),
                ("Pull remote", self._pull_remote),
                ("Push to remote", self._push_remote),
                ("Remove remote", self._remove_remote)
            ]
        )

    def _make_settings_menu(self):
        settings_menu = QtWidgets.QMenu(self)
        settings_menu.setTitle("Settings")
        settings_menu.addMenu(self._make_states_menu())
        settings_menu.addSeparator()

        application_settings_action = self._make_action(
            "Application settings", self._show_settings_dialog
        )

        settings_menu.addAction(application_settings_action)

        return settings_menu

    def _make_states_menu(self):
        self._save_state_action = self._make_action(
            "Save state", self._save_state
        )

        self._update_state_action = self._make_action(
            "Update state", self._update_state
        )

        self._rename_state_action = self._make_action(
            "Rename state", self._rename_state
        )

        self._remove_state_action = self._make_action(
            "Remove state", self._remove_state
        )

        self._states_menu = QtWidgets.QMenu(self)
        self._states_menu.setTitle("States")
        self._update_states_menu()

        return self._states_menu

    def _make_actions_menu(self):
        return self._make_menu(
            "Actions",
            [
                ("Merge...", self._merge),
                ("Abort merge", self._abort_merge)
            ]
        )

    def _show_settings_dialog(self):
        dialog = SettingsDialog(self)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._diff_file_widget.apply_settings()
            self._diff_widget.apply_settings()

    def set_current_state(self, state_name):
        self._current_state = self._states.state_for_name(state_name)

        if not self._current_state.empty():
            self.restoreState(self._current_state.data())

        self._update_states_menu()

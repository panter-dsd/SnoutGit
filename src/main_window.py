# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

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

        self.create_docks()

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
        self.create_main_menu()
        self.create_exit_action()
        self.update_title()

    def _init_default_state(self):
        self._states.append_state("Default", bytes())
        self._current_state = self._states.state(0)

    def create_docks(self):
        top_area = Qt.TopDockWidgetArea
        bottom_area = Qt.BottomDockWidgetArea
        self.addDockWidget(bottom_area, self.create_log_view_dock())
        self.addDockWidget(top_area, self.create_commites_dock())
        self.addDockWidget(bottom_area, self.create_diff_dock())
        self.addDockWidget(top_area, self.create_status_dock())
        self.addDockWidget(top_area, self.create_diff_file_widget_dock())
        self.addDockWidget(bottom_area, self.create_commit_widget_dock())
        self.addDockWidget(bottom_area, self.create_actions_widget_dock())
        self.addDockWidget(bottom_area, self.create_branches_widget_dock())
        self.addDockWidget(bottom_area, self.create_stashes_widget_dock())

    def _create_dock(self, widget, object_name, title=str()):
        dock = QtWidgets.QDockWidget(self)
        dock.setObjectName(object_name)
        dock.setWindowTitle(title)
        dock.setWidget(widget)
        return dock

    def create_commites_dock(self):
        self._commites_widget = CommitesWidget(self._commites_model, self)
        return self._create_dock(self._commites_widget,
                                 "CommitesDock",
                                 "Commites tree")

    def create_diff_dock(self):
        self._diff_widget = DiffWidget(self)
        return self._create_dock(self._diff_widget, "DiffDock", "Commit info")

    def create_status_dock(self):
        self._status_widget = StatusWidget(self)
        return self._create_dock(self._status_widget, "StatusDock", "Status")

    def create_diff_file_widget_dock(self):
        self._diff_file_widget = DiffFileWidget(self)
        return self._create_dock(self._diff_file_widget,
                                 "DiffFileDock",
                                 "Diff")

    def create_commit_widget_dock(self):
        self._commit_widget = CommitWidget(self._commites_model, parent=self)
        return self._create_dock(self._commit_widget, "CommitDock", "Commit")

    def create_actions_widget_dock(self):
        self._actions_widget = ActionsWidget(self)
        return self._create_dock(self._actions_widget,
                                 "ActionsDock",
                                 "Actions")

    def create_log_view_dock(self):
        self._log_view = LogView(self)
        Git.log_view = self._log_view
        return self._create_dock(self._log_view, "LogView", "Log")

    def create_branches_widget_dock(self):
        self._branches_widget = BranchesWidget(self)
        return self._create_dock(self._branches_widget,
                                 "BranchesWidget",
                                 "Branches")

    def create_stashes_widget_dock(self):
        self._stashes_widget = StashesWidget(self)

        stashes_dock = self._create_dock(self._stashes_widget, "StashesWidget")
        self._stashes_widget.state_changed.connect(
            lambda: stashes_dock.setWindowTitle(
                "Stashes ({0})".format(self._stashes_widget.count())
            )
        )
        self._stashes_widget.update_stashes_list()

        return stashes_dock

    def create_main_menu(self):
        self._menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self._menu_bar)
        self._menu_bar.addMenu(self._stashes_widget.menu())
        self._menu_bar.addMenu(self.make_states_menu())
        self._menu_bar.addMenu(self.make_actions_menu())
        self._menu_bar.addMenu(self.make_remote_menu())

        self._git_flow = GitFlowMenu(self)
        self._menu_bar.addMenu(self._git_flow)

    def create_exit_action(self):
        exit_action = QtWidgets.QAction(self)
        exit_action.setShortcut(Qt.CTRL | Qt.Key_Q)
        exit_action.triggered.connect(self.close)
        self.addAction(exit_action)

    def update_title(self):
        self.setWindowTitle("Branch: " + Git().current_branch())

    def save_state(self):
        state_name = QtWidgets.QInputDialog.getText(
            self, "Save state", "StateName"
        )[0]

        if state_name:
            self._current_state = self._states.append_state(
                state_name,
                self.saveState()
            )

            self.update_states_menu()

    def select_state(self):
        states = []
        for i in range(self._states.states_count()):
            states.append(self._states.state(i).name())

        if len(states) == 0:
            return

        state_name = QtWidgets.QInputDialog.getItem(
            self, "Save state", "State name", states, 0, False
        )[0]

        return self._states.state_for_name(state_name)

    def remove_state(self):
        state = self.select_state()
        if state.name():
            self._states.remove_state(state)
            self.update_states_menu()

    def rename_state(self):
        state = self.select_state()
        if state.name():
            state_name = QtWidgets.QInputDialog.getText(
                self, "Rename state", "State name"
            )[0]

            if state_name:
                self._states.rename_state(state.name(), state_name)
                self.update_states_menu()

    def update_state(self):
        state = self.select_state()

        if state.name():
            self._states.update_state(state.name(), self.saveState())
            self.update_states_menu()

    def update_states_menu(self):
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
            action = self._make_action(state.name(), self.restore_state)
            action.setCheckable(True)
            self._states_menu.addAction(action)
            if state.name() == self._current_state.name():
                action.setChecked(True)

    def restore_state(self):
        state_name = self.sender().text()
        print(state_name)
        self._current_state = self._states.state_for_name(state_name)
        self.restoreState(self._current_state.data())
        self.update_states_menu()

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

        isMaximized = settings.value("IsMaximized", False) == "true"

        if isMaximized:
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
            settings.setValue("CurrentState",
                              self._current_state.name())
        else:
            settings.remove("CurrentState")

        settings.endGroup()

    def merge(self):
        d = MergeDialog(self)
        d.exec_()

    def abort_merge(self):
        result = QtWidgets.QMessageBox.question(
            self,
            "Are you sure?",
            "Abort merge",
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )

        if result == QtWidgets.QMessageBox.Ok:
            self._git.abort_merge()

    def add_remote(self):
        d = AddRemoteDialog(self)
        d.exec_()

    def remove_remote(self):
        d = RemoveRemoteDialog(self)
        d.exec_()

    def pull_remote(self):
        d = PullDialog(self)
        d.exec_()

    def push_remote(self):
        d = PushDialog(self)
        d.exec_()

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

    def make_remote_menu(self):
        return self._make_menu(
            "Remote",
            [
                ("Add remote", self.add_remote),
                ("Pull remote", self.pull_remote),
                ("Push to remote", self.push_remote),
                ("Remove remote", self.remove_remote)
            ]
        )

    def make_states_menu(self):
        self._save_state_action = self._make_action("Save state",
                                                    self.save_state)

        self._update_state_action = self._make_action("Update state",
                                                      self.update_state)

        self._rename_state_action = self._make_action("Rename state",
                                                      self.rename_state)

        self._remove_state_action = self._make_action("Remove state",
                                                      self.remove_state)

        self._states_menu = QtWidgets.QMenu(self)
        self._states_menu.setTitle("States")
        self.update_states_menu()

        return self._states_menu

    def make_actions_menu(self):
        return self._make_menu(
            "Actions",
            [
                ("Merge...", self.merge),
                ("Abort merge", self.abort_merge)
            ]
        )

    def set_current_state(self, state_name):
        self._current_state = self._states.state_for_name(state_name)
        if not self._current_state.empty():
            self.restoreState(self._current_state.data())
        self.update_states_menu()
# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import commites_widget
import diff_widget
import status_widget
import diff_file_widget
import commit_widget
import actions_widget
import log_view
import git
import branches_widget
import stashes_widget
import merge_dialog
import add_remote_dialog
import remove_remote_dialog
import pull_dialog
import push_dialog


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
        return None

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


class MainWindow(QtGui.QMainWindow):
    _states = States()
    _current_state = State()
    _git = git.Git()

    def __init__(self, parent=None):
        super().__init__(parent)

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
            self._commites_widget.update_commites_list
        )

        self._actions_widget.state_changed.connect(
            self._commites_widget.update_commites_list
        )

        self._load_settings()
        self.create_main_menu()
        self.create_exit_action()
        self.update_title()

    def create_docks(self):
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,
                           self.create_log_view_dock())
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           self.create_commites_dock())
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,
                           self.create_diff_dock())
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           self.create_status_dock())
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           self.create_diff_file_widget_dock())
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,
                           self.create_commit_widget_dock())
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,
                           self.create_actions_widget_dock())
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,
                           self.create_branches_widget_dock())
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,
                           self.create_stashes_widget_dock())

    def create_commites_dock(self):
        commitesDock = QtGui.QDockWidget(self)
        commitesDock.setObjectName("CommitesDock")
        commitesDock.setWindowTitle("Commites tree")
        self._commites_widget = commites_widget.CommitesWidget(
            commitesDock)
        commitesDock.setWidget(self._commites_widget)
        return commitesDock

    def create_diff_dock(self):
        diffDock = QtGui.QDockWidget(self)
        diffDock.setObjectName("DiffDock")
        diffDock.setWindowTitle("Commit info")
        self._diff_widget = diff_widget.DiffWidget(diffDock)
        diffDock.setWidget(self._diff_widget)
        return diffDock

    def create_status_dock(self):
        status_dock = QtGui.QDockWidget(self)
        status_dock.setObjectName("StatusDock")
        status_dock.setWindowTitle("Status")
        self._status_widget = status_widget.StatusWidget(status_dock)
        status_dock.setWidget(self._status_widget)
        return status_dock

    def create_diff_file_widget_dock(self):
        diff_file_dock = QtGui.QDockWidget(self)
        diff_file_dock.setObjectName("DiffFileDock")
        diff_file_dock.setWindowTitle("Diff")
        self._diff_file_widget = diff_file_widget.DiffFileWidget(
            diff_file_dock)
        diff_file_dock.setWidget(self._diff_file_widget)
        return diff_file_dock

    def create_commit_widget_dock(self):
        commit_widget_dock = QtGui.QDockWidget(self)
        commit_widget_dock.setObjectName("CommitDock")
        commit_widget_dock.setWindowTitle("Commit")
        self._commit_widget = commit_widget.CommitWidget(
            commit_widget_dock)
        commit_widget_dock.setWidget(self._commit_widget)
        return commit_widget_dock

    def create_actions_widget_dock(self):
        actions_widget_dock = QtGui.QDockWidget(self)
        actions_widget_dock.setObjectName("ActionsDock")
        actions_widget_dock.setWindowTitle("Actions")
        self._actions_widget = actions_widget.ActionsWidget(
            actions_widget_dock)
        actions_widget_dock.setWidget(self._actions_widget)
        return actions_widget_dock

    def create_log_view_dock(self):
        log_view_dock = QtGui.QDockWidget(self)
        log_view_dock.setObjectName("LogView")
        log_view_dock.setWindowTitle("Log")
        self._log_view = log_view.LogView(log_view_dock)

        git.Git.log_view = self._log_view

        log_view_dock.setWidget(self._log_view)
        return log_view_dock

    def create_branches_widget_dock(self):
        branches_dock = QtGui.QDockWidget(self)
        branches_dock.setObjectName("BranchesWidget")
        branches_dock.setWindowTitle("Branches")
        self._branches_widget = branches_widget.BranchesWidget(
            branches_dock)
        branches_dock.setWidget(self._branches_widget)
        return branches_dock

    def create_stashes_widget_dock(self):
        stashes_dock = QtGui.QDockWidget(self)
        stashes_dock.setObjectName("StashesWidget")
        self._stashes = stashes_widget.StashesWidget(stashes_dock)
        self._stashes.state_changed.connect(
            lambda: stashes_dock.setWindowTitle(
                "Stashes ({0})".format(self._stashes.count())
            )
        )
        self._stashes.update_stashes_list()
        stashes_dock.setWidget(self._stashes)
        return stashes_dock

    def create_main_menu(self):
        self._menu_bar = QtGui.QMenuBar(self)
        self.setMenuBar(self._menu_bar)
        self._menu_bar.addMenu(self._stashes.menu())
        self._menu_bar.addMenu(self.make_states_menu())
        self._menu_bar.addMenu(self.make_actions_menu())
        self._menu_bar.addMenu(self.make_remote_menu())

    def create_exit_action(self):
        exit_action = QtGui.QAction(self)
        exit_action.setShortcut(QtCore.Qt.CTRL | QtCore.Qt.Key_Q)
        exit_action.triggered.connect(self.close)
        self.addAction(exit_action)

    def update_title(self):
        self.setWindowTitle("Branch: " + git.Git().current_branch())

    def save_state(self):
        state_name = QtGui.QInputDialog.getText(self,
                                                "Save state",
                                                "StateName")[0]
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

        state_name = QtGui.QInputDialog.getItem(self,
                                                "Save state",
                                                "State name",
                                                states,
                                                0,
                                                False)[0]
        return self._states.state_for_name(state_name)

    def remove_state(self):
        state = self.select_state()
        if state.name():
            self._states.remove_state(state)
            self.update_states_menu()

    def rename_state(self):
        state = self.select_state()
        if state.name():
            state_name = QtGui.QInputDialog.getText(self,
                                                    "Rename state",
                                                    "State name")[0]
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
        settings = QtCore.QSettings()

        settings.beginGroup("GUI")
        settings.beginGroup("MainWindow")

        self.restoreState(settings.value("State", QtCore.QByteArray()))

        if settings.contains("pos"):
            self.move(settings.value("pos"))

        size = settings.value("size", QtCore.QSize(1024, 768))

        self.resize(size)

        isMaximized = settings.value("IsMaximized", False) == "true"

        if isMaximized:
            self.setWindowState(QtCore.Qt.WindowMaximized)

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
        settings = QtCore.QSettings()

        settings.beginGroup("GUI")
        settings.beginGroup("MainWindow")

        if self.windowState() != QtCore.Qt.WindowMaximized:
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
        d = merge_dialog.MergeDialog(self)
        d.exec_()

    def abort_merge(self):
        result = QtGui.QMessageBox.question(
            self,
            "Are you sure?",
            "Abort merge",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

        if result == QtGui.QMessageBox.Ok:
            self._git.abort_merge()

    def add_remote(self):
        d = add_remote_dialog.AddRemoteDialog(self)
        d.exec_()

    def remove_remote(self):
        d = remove_remote_dialog.RemoveRemoteDialog(self)
        d.exec_()

    def pull_remote(self):
        d = pull_dialog.PullDialog(self)
        d.exec_()

    def push_remote(self):
        d = push_dialog.PushDialog(self)
        d.exec_()

    def _make_action(self, caption, slot):
        action = QtGui.QAction(self)
        action.setText(caption)
        action.triggered.connect(slot)
        return action

    def _make_menu(self, title, actions):
        menu = QtGui.QMenu(self)
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

        self._states_menu = QtGui.QMenu(self)
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
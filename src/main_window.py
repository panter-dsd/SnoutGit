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
        super(State, self).__init__()

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
        super(States, self).__init__()

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
        super(MainWindow, self).__init__(parent)

        commitesDock = QtGui.QDockWidget(self)
        commitesDock.setObjectName("CommitesDock")
        commitesDock.setWindowTitle("Commites tree")
        commites = commites_widget.CommitesWidget(commitesDock)
        commitesDock.setWidget(commites)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, commitesDock)

        diffDock = QtGui.QDockWidget(self)
        diffDock.setObjectName("DiffDock")
        diffDock.setWindowTitle("Commit info")
        diff = diff_widget.DiffWidget(diffDock)
        diffDock.setWidget(diff)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, diffDock)

        commites.current_commit_changed.connect(diff.set_commit)

        status_dock = QtGui.QDockWidget(self)
        status_dock.setObjectName("StatusDock")
        status_dock.setWindowTitle("Status")
        status = status_widget.StatusWidget(status_dock)
        status_dock.setWidget(status)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, status_dock)

        diff_file_dock = QtGui.QDockWidget(self)
        diff_file_dock.setObjectName("DiffFileDock")
        diff_file_dock.setWindowTitle("Diff")
        diff_file = diff_file_widget.DiffFileWidget(diff_file_dock)
        diff_file_dock.setWidget(diff_file)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, diff_file_dock)

        status.current_file_changed.connect(diff_file.set_file)
        status.status_changed.connect(diff_file.clear)

        commit_widget_dock = QtGui.QDockWidget(self)
        commit_widget_dock.setObjectName("CommitDock")
        commit_widget_dock.setWindowTitle("Commit")
        commit = commit_widget.CommitWidget(commit_widget_dock)
        commit_widget_dock.setWidget(commit)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, commit_widget_dock)

        commit.commited.connect(commites.update_commites_list)

        actions_widget_dock = QtGui.QDockWidget(self)
        actions_widget_dock.setObjectName("ActionsDock")
        actions_widget_dock.setWindowTitle("Actions")
        actions = actions_widget.ActionsWidget(actions_widget_dock)
        actions_widget_dock.setWidget(actions)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, actions_widget_dock)

        actions.state_changed.connect(commites.update_commites_list)

        log_view_dock = QtGui.QDockWidget(self)
        log_view_dock.setObjectName("LogView")
        log_view_dock.setWindowTitle("Log")
        log = log_view.LogView(log_view_dock)
        log_view_dock.setWidget(log)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, log_view_dock)
        git.Git.log_view = log

        branches_dock = QtGui.QDockWidget(self)
        branches_dock.setObjectName("BranchesWidget")
        branches_dock.setWindowTitle("Branches")
        branches = branches_widget.BranchesWidget(branches_dock)
        branches_dock.setWidget(branches)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, branches_dock)

        stashes_dock = QtGui.QDockWidget(self)
        stashes_dock.setObjectName("StashesWidget")
        stashes = stashes_widget.StashesWidget(stashes_dock)
        stashes.state_changed.connect(
            lambda: stashes_dock.setWindowTitle(
                "Stashes ({0})".format(stashes.count())
            )
        )
        stashes.update_stashes_list()
        stashes_dock.setWidget(stashes)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, stashes_dock)

        self._load_settings()

        self._menu_bar = QtGui.QMenuBar(self)
        super(MainWindow, self).setMenuBar(self._menu_bar)

        self._menu_bar.addMenu(stashes.menu())
        self._menu_bar.addMenu(self.make_states_menu())
        self._menu_bar.addMenu(self.make_actions_menu())
        self._menu_bar.addMenu(self.make_remote_menu())

        exit_action = QtGui.QAction(self)
        exit_action.setShortcut(QtCore.Qt.CTRL | QtCore.Qt.Key_Q)
        exit_action.triggered.connect(self.close)
        super(MainWindow, self).addAction(exit_action)

        self.update_title()

    def update_title(self):
        super(MainWindow, self).setWindowTitle(
            "Branch: " + git.Git().current_branch()
        )

    def save_state(self):
        state_name = QtGui.QInputDialog.getText(self,
                                                "Save state",
                                                "StateName")[0]
        if state_name:
            self._current_state = self._states.append_state(
                state_name,
                super(MainWindow, self).saveState()
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
            self._states.update_state(
                state.name(),
                super(MainWindow, self).saveState()
            )
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
        super(MainWindow, self).restoreState(
            self._current_state.data()
        )
        self.update_states_menu()

    def closeEvent(self, event):
        self._save_settings()
        event.accept()

    def _load_settings(self):
        settings = QtCore.QSettings()

        settings.beginGroup("GUI")
        settings.beginGroup("MainWindow")

        super(MainWindow, self).restoreState(
            settings.value("State",
                           QtCore.QByteArray()))

        if settings.contains("pos"):
            super(MainWindow, self).move(settings.value("pos"))

        size = settings.value("size", QtCore.QSize(1024, 768))

        super(MainWindow, self).resize(size)

        isMaximized = settings.value("IsMaximized", False) == "true"

        if isMaximized:
            super(MainWindow, self).setWindowState(
                QtCore.Qt.WindowMaximized
            )

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
            super(MainWindow, self).restoreState(
                self._current_state.data()
            )

        settings.endGroup()

    def _save_settings(self):
        settings = QtCore.QSettings()

        settings.beginGroup("GUI")
        settings.beginGroup("MainWindow")

        if super(MainWindow, self).windowState() != QtCore.Qt.WindowMaximized:
            settings.setValue("pos", super(MainWindow, self).pos())
            settings.setValue("size", super(MainWindow, self).size())
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
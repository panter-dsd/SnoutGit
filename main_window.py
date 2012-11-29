# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import commites_widget
import diff_widget
import status_widget
import diff_file_widget
import commit_widget
import actions_widget
import log_view
import git


class State(object):
    _name = str()
    _data = None

    def __init__(self, name=None, data=None):
        super(State, self).__init__()

        self._name = name
        self._data = data

    def name(self):
        return self._name

    def data(self):
        return self._data


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

        log_view_dock = QtGui.QDockWidget(self)
        log_view_dock.setObjectName("LogView")
        log_view_dock.setWindowTitle("Log")
        log = log_view.LogView(log_view_dock)
        log_view_dock.setWidget(log)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, log_view_dock)
        git.Git.log_view = log

        self._load_settings()

        self._save_state_action = QtGui.QAction(self)
        self._save_state_action.setText("Save state")
        self._save_state_action.triggered.connect(self.save_state)

        self._update_state_action = QtGui.QAction(self)
        self._update_state_action.setText("Update state")
        self._update_state_action.triggered.connect(self.update_state)

        self._rename_state_action = QtGui.QAction(self)
        self._rename_state_action.setText("Rename state")
        self._rename_state_action.triggered.connect(self.rename_state)

        self._remove_state_action = QtGui.QAction(self)
        self._remove_state_action.setText("Remove state")
        self._remove_state_action.triggered.connect(self.remove_state)

        self._menu_bar = QtGui.QMenuBar(self)
        super(MainWindow, self).setMenuBar(self._menu_bar)

        self._states_menu = QtGui.QMenu(self)
        self._states_menu.setTitle("States")
        self._menu_bar.addMenu(self._states_menu)
        self.update_states_menu()

        exit_action = QtGui.QAction(self)
        exit_action.setShortcut(QtCore.Qt.CTRL | QtCore.Qt.Key_Q)
        exit_action.triggered.connect(self.close)
        super(MainWindow, self).addAction(exit_action)


    def save_state(self):
        state_name = QtGui.QInputDialog.getText(self,
            "Save state",
            "StateName")[0]
        if len(state_name) > 0:
            self._current_state = self._states.append_state(
                state_name,
                super(MainWindow, self).saveState())
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
        if len(state.name()) > 0:
            self._states.remove_state(state)
            self.update_states_menu()

    def rename_state(self):
        state = self.select_state()
        if len(state.name()) > 0:
            state_name = QtGui.QInputDialog.getText(self,
                "Rename state",
                "State name")[0]
            if len(state_name) > 0:
                self._states.rename_state(state.name(), state_name)
                self.update_states_menu()

    def update_state(self):
        state = self.select_state()

        if len(state.name()) > 0:
            self._states.update_state(state.name(), super(MainWindow, self).saveState())
            self.update_states_menu()


    def update_states_menu(self):
        self._states_menu.clear()
        self._states_menu.addAction(self._save_state_action)
        self._states_menu.addAction(self._update_state_action)
        self._states_menu.addAction(self._rename_state_action)
        self._states_menu.addAction(self._remove_state_action)
        self._remove_state_action.setEnabled(self._states.states_count() > 0)
        self._states_menu.addSeparator()

        for i in range(self._states.states_count()):
            action = QtGui.QAction(self)
            state = self._states.state(i)
            action.setText(state.name())
            action.triggered.connect(self.restore_state)
            action.setCheckable(True)
            self._states_menu.addAction(action)
            if state.name() == self._current_state.name():
                action.setChecked(True)

    def restore_state(self):
        state_name = self.sender().text()
        print(state_name)
        self._current_state = self._states.state_for_name(state_name)
        super(MainWindow, self).restoreState(self._current_state.data())
        self.update_states_menu()

    def closeEvent(self, event):
        self._save_settings()
        event.accept()

    def _load_settings(self):
        settings = QtCore.QSettings()

        settings.beginGroup("GUI")
        settings.beginGroup("MainWindow")

        if settings.contains("pos"):
            super(MainWindow, self).move(settings.value("pos"))

        size = settings.value("size", QtCore.QSize(1024, 768))

        super(MainWindow, self).resize(size)

        isMaximized = settings.value("IsMaximized", False) == "true"

        if isMaximized:
            super(MainWindow, self).setWindowState(QtCore.Qt.WindowMaximized)

        super(MainWindow, self).restoreState(settings.value("State"))

        settings.endGroup()

        states_count = settings.beginReadArray("States")
        for i in range(states_count):
            settings.setArrayIndex(i)
            self._states.append_state(
                settings.value("Name"),
                settings.value("Data"))
        settings.endArray()

        state_name = settings.value("CurrentState", str())
        if len(state_name) > 0:
            self._current_state = self._states.state_for_name(state_name)
            super(MainWindow, self).restoreState(self._current_state.data())

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

        settings.setValue("CurrentState", self._current_state.name())

        settings.endGroup()

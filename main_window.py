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


class MainWindow(QtGui.QMainWindow):
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

        settings.setValue("State", super(MainWindow, self).saveState())

        settings.endGroup()
        settings.endGroup()

# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import commites_widget
import diff_widget
import status_widget
import diff_file_widget
import commit_widget
import actions_widget


class MainWindow(QtGui.QMainWindow):
    def __init__(self, path, parent=None):
        super(MainWindow, self).__init__(parent)

        commitesDock = QtGui.QDockWidget(self)
        commites = commites_widget.CommitesWidget(path, commitesDock)
        commitesDock.setWidget(commites)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, commitesDock)

        diffDock = QtGui.QDockWidget(self)
        diff = diff_widget.DiffWidget(path, diffDock)
        diffDock.setWidget(diff)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, diffDock)

        commites.current_commit_changed.connect(diff.set_commit)

        status_dock = QtGui.QDockWidget(self)
        status = status_widget.StatusWidget(path, status_dock)
        status_dock.setWidget(status)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, status_dock)

        diff_file_dock = QtGui.QDockWidget(self)
        diff_file = diff_file_widget.DiffFileWidget(path)
        diff_file_dock.setWidget(diff_file)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, diff_file_dock)

        status.current_file_changed.connect(diff_file.set_file)
        status.status_changed.connect(diff_file.clear)

        commit_widget_dock = QtGui.QDockWidget(self)
        commit = commit_widget.CommitWidget(path)
        commit_widget_dock.setWidget(commit)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, commit_widget_dock)

        commit.commited.connect(commites.update_commites_list)

        actions_widget_dock = QtGui.QDockWidget(self)
        actions = actions_widget.ActionsWidget(path)
        actions_widget_dock.setWidget(actions)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, actions_widget_dock)

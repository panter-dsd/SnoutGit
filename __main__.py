# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'



import sys
import os
from PySide import QtCore, QtGui
import commites_widget
import diff_widget
import status_widget
import diff_file_widget
import commit_widget
import actions_widget

PATH = os.curdir

@QtCore.Slot(str)
def ttt(eee):
    import commit
    print(commit.Commit(PATH, eee).name())

def main():
    """main"""
    app = QtGui.QApplication(sys.argv)

    window = QtGui.QMainWindow()

    commitesDock = QtGui.QDockWidget(window)
    commites = commites_widget.CommitesWidget(PATH, commitesDock)
    commitesDock.setWidget(commites)
    window.addDockWidget(QtCore.Qt.TopDockWidgetArea, commitesDock)

    diffDock = QtGui.QDockWidget(window)
    diff = diff_widget.DiffWidget(PATH, diffDock)
    diffDock.setWidget(diff)
    window.addDockWidget(QtCore.Qt.BottomDockWidgetArea, diffDock)

    commites.current_commit_changed.connect(diff.set_commit)

    status_dock = QtGui.QDockWidget(window)
    status = status_widget.StatusWidget(PATH, status_dock)
    status_dock.setWidget(status)
    window.addDockWidget(QtCore.Qt.TopDockWidgetArea, status_dock)

    diff_file_dock = QtGui.QDockWidget(window)
    diff_file = diff_file_widget.DiffFileWidget(PATH)
    diff_file_dock.setWidget(diff_file)
    window.addDockWidget(QtCore.Qt.TopDockWidgetArea, diff_file_dock)

    status.current_file_changed.connect(diff_file.set_file)
    status.status_changed.connect(diff_file.clear)

    commit_widget_dock = QtGui.QDockWidget(window)
    commit = commit_widget.CommitWidget(PATH)
    commit_widget_dock.setWidget(commit)
    window.addDockWidget(QtCore.Qt.BottomDockWidgetArea, commit_widget_dock)

    commit.commited.connect(commites.update_commites_list)

    actions_widget_dock = QtGui.QDockWidget(window)
    actions = actions_widget.ActionsWidget(PATH)
    actions_widget_dock.setWidget(actions)
    window.addDockWidget(QtCore.Qt.BottomDockWidgetArea,actions_widget_dock)

    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

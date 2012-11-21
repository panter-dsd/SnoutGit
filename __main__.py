# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'


PATH = "/media/work/other/phradar"

import sys
from PySide import QtCore, QtGui
import commites_widget
import diff_widget

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

    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
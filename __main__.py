# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'


PATH = "/media/work/other/phradar"

import sys
from PySide import QtCore, QtGui
import commites_widget

def main():
    """main"""
    app = QtGui.QApplication(sys.argv)

    window = QtGui.QMainWindow()

    commitesDock = QtGui.QDockWidget(window)
    commitesDock.setWidget(commites_widget.CommitesWidget(PATH, commitesDock))

    window.addDockWidget(QtCore.Qt.TopDockWidgetArea, commitesDock)

    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
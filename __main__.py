# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import sys
import os
from PySide import QtGui
import main_window


def main():
    """main"""

    if len(sys.argv) < 2:
        path = os.curdir
    else:
        path = sys.argv[1]

    os.chdir(path)

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("PyGitGui")
    app.setApplicationVersion("0.0.0.0")
    app.setOrganizationName("PanteR")

    window = main_window.MainWindow(path)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

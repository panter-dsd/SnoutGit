#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import sys
import os
from PyQt4 import QtGui
import main_window


def main():
    """main"""

    if len(sys.argv) < 2:
        path = os.path.abspath(os.curdir)
    else:
        path = os.path.abspath(sys.argv[1])

    while not os.path.exists(path + "/.git"):
        path = os.path.dirname(path)
        if len(path) == 1:
            break

    print("Use git repository:", path)
    os.chdir(path)

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("PyGitGui")
    app.setApplicationVersion("0.0.0.0")
    app.setOrganizationName("PanteR")

    window = main_window.MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import sys
import os
from PyQt4 import QtGui
import main_window


def is_git_root(path):
    return os.path.exists(path + "/.git")


def get_git_root_path(path):
    result = path
    while not is_git_root(result):
        parent_dir = os.path.dirname(result)
        if result == parent_dir:
            break
        result = parent_dir

    return is_git_root(result) and result or path


def main():
    """main"""

    if len(sys.argv) < 2:
        path = os.path.abspath(os.curdir)
    else:
        path = os.path.abspath(sys.argv[1])

    path = get_git_root_path(path)
    print("Use git repository:", path)

    try:
        os.chdir(path)
    except OSError as error:
        print(error)
        return

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("SnoutGit")
    app.setApplicationVersion("0.0.0.0")
    app.setOrganizationName("PanteR")

    window = main_window.MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

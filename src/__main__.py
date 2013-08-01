#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import sys
import os
from PyQt4 import QtGui
import main_window
import git


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


def load_current_state():
    result = str()
    try:
        state_name_index = sys.argv.index("--state") + 1
        if state_name_index < len(sys.argv):
            result = sys.argv[state_name_index]
    except ValueError:
        pass

    return result

def get_font():
    result = str()
    try:
        font_name_index = sys.argv.index("--font") + 1
        if font_name_index < len(sys.argv):
            result = sys.argv[font_name_index]
    except ValueError:
        pass

    return result

def main():
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

    git.Git.repo_path = path + "/.git"

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("SnoutGit")
    app.setApplicationVersion("0.0.0.0")
    app.setOrganizationName("PanteR")

    font_name = get_font()
    if font_name:
        font = app.font()
        font.setFamily(font_name)
        app.setFont(font)

    window = main_window.MainWindow()

    state = load_current_state()
    if state:
        window.set_current_state(state)

    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

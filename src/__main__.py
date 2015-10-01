#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtWidgets import QApplication

import main_window
import git

from submodule_dialog import SubmoduleDialog

__author__ = 'panter.dsd@gmail.com'


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


def get_git_executable_path():
    result = "git"
    try:
        git_executable_path_index = sys.argv.index("--git-executable") + 1
        if git_executable_path_index < len(sys.argv):
            result = sys.argv[git_executable_path_index]
    except ValueError:
        pass

    return result


def main():
    if len(sys.argv) < 2:
        path = os.path.abspath(os.curdir)
    else:
        path = os.path.abspath(sys.argv[-1])

    git.Git.git_executable_path = get_git_executable_path()

    path = get_git_root_path(path)
    print("Use git repository:", path)

    try:
        os.chdir(path)
    except OSError as error:
        print(error)
        return

    git.Git.repo_path = path

    app = QApplication(sys.argv)
    app.setApplicationName("SnoutGit")
    app.setApplicationVersion("0.0.0.0")
    app.setOrganizationName("PanteR")

    font_name = get_font()
    if font_name:
        font = app.font()
        font.setFamily(font_name)
        app.setFont(font)

    if "--submodule" in sys.argv:
        submodules = git.Git().submodules()

        if submodules:
            submodule_dialog = SubmoduleDialog(submodules)
            if submodule_dialog.exec():
                git.Git.repo_path = path + "/" + submodule_dialog.submodule()

    window = main_window.MainWindow()

    state = load_current_state()
    if state:
        window.set_current_state(state)

    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

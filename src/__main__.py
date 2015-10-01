#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import QCommandLineParser, QCommandLineOption
from PyQt5.QtWidgets import QApplication

import main_window
import git

from submodule_dialog import SubmoduleDialog

__author__ = 'panter.dsd@gmail.com'


def is_git_root(repository_path):
    return os.path.exists(os.path.join(repository_path, ".git"))


def get_git_root_path(repository_path):
    result = repository_path

    while not is_git_root(result):
        parent_dir = os.path.dirname(result)

        if result == parent_dir:
            break

        result = parent_dir

    return is_git_root(result) and result or repository_path


def command_line_arguments_parser():
    parser = QCommandLineParser()

    parser.setApplicationDescription(
        "Qt-based graphical user interface to Git."
    )

    parser.addHelpOption()
    parser.addVersionOption()
    parser.addPositionalArgument("path", "The path to the repository.")

    submodule_option = QCommandLineOption(
        "submodule", "Runs the application with submodule selection dialog."
    )

    font_option = QCommandLineOption(
        "font", "Sets the font of the application.", "font name"
    )

    git_executable_option = QCommandLineOption(
        "git-executable",
        "Sets the path to git executable file.",
        "path",
        "git"
    )

    state_option = QCommandLineOption(
        "state", "Loads the state of main window.", "state"
    )

    parser.addOption(submodule_option)
    parser.addOption(font_option)
    parser.addOption(git_executable_option)
    parser.addOption(state_option)

    return parser


if __name__ == '__main__':
    args_parser = command_line_arguments_parser()

    app = QApplication(sys.argv)
    app.setApplicationName("SnoutGit")
    app.setApplicationVersion("0.0.0.0")
    app.setOrganizationName("PanteR")

    args_parser.process(app)

    args = args_parser.positionalArguments()
    path = get_git_root_path(os.path.abspath(args[0] if args else os.curdir))
    print("Use git repository:", path)

    git.Git.git_executable_path = args_parser.value("git-executable")

    try:
        os.chdir(path)
    except OSError as error:
        print(error)
        sys.exit(1)

    git.Git.repo_path = path

    if args_parser.isSet("font"):
        font = app.font()
        font.setFamily(args_parser.value("font"))
        app.setFont(font)

    if args_parser.isSet("submodule"):
        submodules = git.Git().submodules()

        if submodules:
            dialog = SubmoduleDialog(submodules)

            if dialog.exec():
                git.Git.repo_path = os.path.join(path, dialog.submodule())

    window = main_window.MainWindow()

    if args_parser.isSet("state"):
        window.set_current_state(args_parser.value("state"))

    window.show()

    sys.exit(app.exec_())

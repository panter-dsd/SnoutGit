# -*- coding: utf-8 -*-

import os.path

from PyQt5 import uic


def load_ui_from_file(file_name,  baseinstance=None):
    return uic.loadUi(
        os.path.join(_ui_files_directory(), file_name), baseinstance
    )


def _ui_files_directory():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)))

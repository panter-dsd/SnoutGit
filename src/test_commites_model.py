# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import tempfile
import os
import unittest
from PyQt4 import QtCore

from git import Git
from commites_model import CommitesModel


class TestCommitesModel(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.init_empty_git_repo()

    def tearDown(self):
        del self.temp_dir

    def init_empty_git_repo(self):
        os.chdir(self.temp_dir.name)
        self._git = Git()
        self._git.execute_command(["init"], False)
        self._git.repo_path = self.temp_dir.name + "/.git"

    def test_empty_repo(self):
        model = CommitesModel(self._git, None)
        self.assertEqual(model.rowCount(), 0)
        self.assertEqual(model.columnCount(), 4)
        for column in range(model.columnCount()):
            self.assertFalse(model.data(model.index(0, column),
                                        QtCore.Qt.DisplayRole))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommitesModel))
    return suite
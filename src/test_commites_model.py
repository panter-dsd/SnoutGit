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
        self.temp_dir.cleanup()
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

    def _commit_file(self, commit_name):
        file = tempfile.mkstemp(dir=self.temp_dir.name)
        self._git.stage_files([file[1]])
        self.assertTrue(self._git.commit(commit_name))

    def _generate_repo(self):
        result = []
        for i in range(10):
            commit_name = "Commit" + str(i)
            self._commit_file(commit_name)
            result.append(commit_name)

        return result

    def test_comments_repo(self):
        commites = self._generate_repo()
        model = CommitesModel(self._git, None)
        self.assertEqual(model.rowCount(), len(commites))
        i = len(commites) - 1
        for commit in commites:
            self.assertEqual(model.data(model.index(i, 1), QtCore.Qt.EditRole),
                             commit)
            i -= 1

    def test_roles_data(self):
        commites = self._generate_repo()
        model = CommitesModel(self._git, None)

        commit = commites[-1]

        self.assertEqual(model.data(model.index(0, 1), QtCore.Qt.DisplayRole),
                         "[master]" + commit)
        self.assertEqual(model.data(model.index(0, 1), QtCore.Qt.ToolTipRole),
                         commit)
        self.assertEqual(model.data(model.index(0, 1), QtCore.Qt.EditRole),
                         commit)
        self.assertTrue(
            model.data(model.index(0, 0), QtCore.Qt.EditRole).startswith(
                model.data(model.index(0, 0), QtCore.Qt.DisplayRole)
            )
        )
        self.assertNotEqual(
            model.data(model.index(0, 0), QtCore.Qt.EditRole),
            model.data(model.index(0, 0), QtCore.Qt.DisplayRole)
        )

    def test_data_with_tag(self):
        commites = self._generate_repo()
        tag_name = "some_tag"
        tag_message = "some_tag_message"
        self._git.create_tag(self._git.commites()[0].id(), tag_name,
                             tag_message)

        model = CommitesModel(self._git, None)
        commit = commites[-1]

        self.assertEqual(model.data(model.index(0, 1), QtCore.Qt.DisplayRole),
                         "<" + tag_name + ">[master]" + commit)
        self.assertTrue(tag_name in model.data(model.index(0, 1),
                                               QtCore.Qt.ToolTipRole))
        self.assertTrue(tag_message in model.data(model.index(0, 1),
                                                  QtCore.Qt.ToolTipRole))
        self.assertEqual(model.data(model.index(0, 1), QtCore.Qt.EditRole),
                         commit)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommitesModel))
    return suite

# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import tempfile
import os
import unittest

from git import Git, Stash, MergeOptions, Remote


class StashTest(unittest.TestCase):
    def test_empty_data(self):
        stash = Stash(str(), str())
        self.assertFalse(stash.name)
        self.assertFalse(stash.description)

    def test_no_empty_data(self):
        name = "name"
        descr = "descr"
        stash = Stash(name, descr)
        self.assertEqual(stash.name, name)
        self.assertEqual(stash.description, descr)


class MergeOptionsTest(unittest.TestCase):
    def test_empty_data(self):
        mo = MergeOptions(str())
        self.assertFalse(mo.source_target)
        self.assertTrue(mo.commit)
        self.assertFalse(mo.fast_forward)
        self.assertFalse(mo.squash)

    def test_no_empty_data(self):
        source_target = "test"
        mo = MergeOptions(source_target)
        self.assertEqual(mo.source_target, source_target)
        self.assertTrue(mo.commit)
        self.assertFalse(mo.fast_forward)
        self.assertFalse(mo.squash)


class RemoteTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)
        self._git = Git()
        self._git.execute_command(["init"], False)
        self._git.repo_path = self.temp_dir.name + "/.git"

    def tearDown(self):
        del self.temp_dir

    def test_remotes_list(self):
        remote = Remote(self._git)
        self.assertFalse(remote.remotes_list())

    def test_add_remote(self):
        remote = Remote(self._git)
        remote.add_remote("some", "url")
        self.assertEqual(remote.remotes_list(), ["some"])

    def test_rename_remote(self):
        remote = Remote(self._git)
        remote.add_remote("some", "url")
        remote.rename_remote("some", "not_some")
        self.assertEqual(remote.remotes_list(), ["not_some"])

    def test_remove_remote(self):
        remote = Remote(self._git)
        remote.add_remote("some", "url")
        self.assertEqual(remote.remotes_list(), ["some"])
        remote.remove_remote("some")
        self.assertFalse(remote.remotes_list())


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StashTest))
    suite.addTest(unittest.makeSuite(MergeOptionsTest))
    suite.addTest(unittest.makeSuite(RemoteTest))
    return suite
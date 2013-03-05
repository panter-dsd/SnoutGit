# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import tempfile
import os
import unittest
import git


class StashTest(unittest.TestCase):
    def test_empty_data(self):
        stash = git.Stash(str(), str())
        self.assertFalse(stash.name)
        self.assertFalse(stash.description)

    def test_no_empty_data(self):
        name = "name"
        descr = "descr"
        stash = git.Stash(name, descr)
        self.assertEqual(stash.name, name)
        self.assertEqual(stash.description, descr)


class MergeOptionsTest(unittest.TestCase):
    def test_empty_data(self):
        mo = git.MergeOptions(str())
        self.assertFalse(mo.source_target)
        self.assertTrue(mo.commit)
        self.assertFalse(mo.fast_forward)
        self.assertFalse(mo.squash)

    def test_no_empty_data(self):
        source_target = "test"
        mo = git.MergeOptions(source_target)
        self.assertEqual(mo.source_target, source_target)
        self.assertTrue(mo.commit)
        self.assertFalse(mo.fast_forward)
        self.assertFalse(mo.squash)


class PushOptionsTest(unittest.TestCase):
    def test_empty_data(self):
        po = git.PushOptions(str(), str())
        self.assertFalse(po.branch)
        self.assertFalse(po.remote)
        self.assertFalse(po.force)
        self.assertTrue(po.include_tags)

    def test_no_empty_data(self):
        branch = "branch"
        remote = "remote"
        po = git.PushOptions(branch, remote)
        self.assertEqual(po.branch, branch)
        self.assertEqual(po.remote, remote)
        self.assertFalse(po.force)
        self.assertTrue(po.include_tags)


class RemoteTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)
        self._git = git.Git()
        self._git.execute_command(["init"], False)
        self._git.repo_path = self.temp_dir.name + "/.git"

    def tearDown(self):
        del self.temp_dir

    def test_remotes_list(self):
        remote = git.Remote(self._git)
        self.assertFalse(remote.remotes_list())

    def test_add_remote(self):
        remote = git.Remote(self._git)
        remote.add_remote("some", "url")
        self.assertEqual(remote.remotes_list(), ["some"])

    def test_rename_remote(self):
        remote = git.Remote(self._git)
        remote.add_remote("some", "url")
        remote.rename_remote("some", "not_some")
        self.assertEqual(remote.remotes_list(), ["not_some"])

    def test_remove_remote(self):
        remote = git.Remote(self._git)
        remote.add_remote("some", "url")
        self.assertEqual(remote.remotes_list(), ["some"])
        remote.remove_remote("some")
        self.assertFalse(remote.remotes_list())

class GitTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)
        self._git = git.Git()
        self._git.execute_command(["init"], False)
        self._git.repo_path = self.temp_dir.name + "/.git"

    def tearDown(self):
        del self.temp_dir

    def test_commites(self):
        self.assertFalse(self._git.commites())

        file = tempfile.mkstemp(dir=self.temp_dir.name)
        self._git.stage_files([file[1]])
        self._git.commit("Test commit")
        self.assertTrue(self._git.commites())


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StashTest))
    suite.addTest(unittest.makeSuite(MergeOptionsTest))
    suite.addTest(unittest.makeSuite(PushOptionsTest))
    suite.addTest(unittest.makeSuite(RemoteTest))
    suite.addTest(unittest.makeSuite(GitTest))
    return suite
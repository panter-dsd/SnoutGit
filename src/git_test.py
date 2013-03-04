# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from git import Stash
import unittest


class StashTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_data(self):
        stash = Stash(str(), str())
        self.assertFalse(stash.name)
        self.assertFalse(stash.description)

    def test_init(self):
        stash = Stash("name", "descr")
        self.assertEqual(stash.name, "name")
        self.assertEqual(stash.description, "descr")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StashTest))
    return suite
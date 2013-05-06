# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

import unittest
import sys
from PyQt4 import QtGui

from main_window import MainWindow, State

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self._app = QtGui.QApplication(sys.argv)

    def tearDown(self):
        del self._app

    def test_set_current_state(self):
        window = MainWindow()
        self.assertTrue(window._states.states_count() > 0)
        window._current_state = State()
        self.assertTrue(window._current_state.empty())
        window.set_current_state("Some")
        self.assertTrue(window._current_state.empty())
        window.set_current_state("Default")
        self.assertEqual(window._current_state.name(), "Default")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMainWindow))
    return suite

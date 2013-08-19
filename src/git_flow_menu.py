# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git
from create_branch_dialog import CreateBranchDialog


class GitFlowMenu(QtGui.QMenu):
    _git = git.Git()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Git flow")

        self._add_fix_action = QtGui.QAction(self)
        self._add_fix_action.setText("Add fix branch (fix/....)")
        self._add_fix_action.triggered.connect(self.add_fix_branch)
        self.addAction(self._add_fix_action)

        self._add_feature_action = QtGui.QAction(self)
        self._add_feature_action.setText("Add feature branch (feature/....)")
        self._add_feature_action.triggered.connect(self.add_feature_branch)
        self.addAction(self._add_feature_action)

    def add_fix_branch(self):
        dialog = CreateBranchDialog(self)
        dialog.set_parent_branch("develop")
        dialog.set_branch_name("fix/")
        if (dialog.exec()):
            self._create_branch(dialog)

    def add_feature_branch(self):
        dialog = CreateBranchDialog(self)
        dialog.set_parent_branch("develop")
        dialog.set_branch_name("feature/")
        if (dialog.exec()):
            self._create_branch(dialog)

    def _create_branch(self, create_branch_dialog):
        branch = create_branch_dialog.branch_name()
        parent_branch = create_branch_dialog.parent_branch()
        if self._git.create_branch(branch, parent_branch):
            self._git.checkout(branch)
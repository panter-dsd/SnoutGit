# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import create_branch_dialog
import git
import rename_branch_dialog

class BranchesWidget(QtGui.QWidget):
    _git = git.Git()

    def __init__(self, parent=None):
        super(BranchesWidget, self).__init__(parent)

        self._local_branches_label = QtGui.QLabel("Local branches", self)

        self._local_branches_list = QtGui.QListWidget(self)

        self._remote_branches_label = QtGui.QLabel("Remote branches", self)

        self._remote_branches_list = QtGui.QListWidget(self)

        self._create_button = QtGui.QPushButton("Create", self)
        self._create_button.clicked.connect(self._create)

        self._checkout_button = QtGui.QPushButton("Checkout", self)
        self._checkout_button.clicked.connect(self._checkout)

        self._rename_button = QtGui.QPushButton("Rename", self)
        self._rename_button.clicked.connect(self._rename)

        buttons_layout = QtGui.QVBoxLayout()
        buttons_layout.addWidget(self._checkout_button)
        buttons_layout.addWidget(self._create_button)
        buttons_layout.addWidget(self._rename_button)
        buttons_layout.addSpacerItem(QtGui.QSpacerItem(0,
                                                       0,
                                                       QtGui.QSizePolicy.Preferred,
                                                       QtGui.QSizePolicy.Expanding))

        tables_layout = QtGui.QVBoxLayout()
        tables_layout.addWidget(self._local_branches_label)
        tables_layout.addWidget(self._local_branches_list)
        tables_layout.addWidget(self._remote_branches_label)
        tables_layout.addWidget(self._remote_branches_list)

        main_layout = QtGui.QHBoxLayout()
        main_layout.addLayout(tables_layout)
        main_layout.addLayout(buttons_layout)

        super(BranchesWidget, self).setLayout(main_layout)
        self._update_lists()

    def _update_lists(self):
        self._local_branches_list.clear()
        self._remote_branches_list.clear()

        current_branch = self._git.current_branch()

        for branch in self._git.local_branches():
            item = QtGui.QListWidgetItem(branch, self._local_branches_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self._local_branches_list.addItem(item)
            if current_branch == branch:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

        for branch in self._git.remote_branches():
            item = QtGui.QListWidgetItem(branch, self._remote_branches_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self._remote_branches_list.addItem(item)

    def _create(self):
        d = create_branch_dialog.CreateBranchDialog(self)
        if d.exec_():
            self._git.create_branch(d.branch_name(),
                                    d.parent_branch())
            if d.can_checkout():
                self._git.checkout(d.branch_name())
            self._update_lists()

    def _checkout(self):
        item = self._local_branches_list.currentItem()
        if item and item.checkState() != QtCore.Qt.Checked:
            self._git.checkout(item.text())
            self._update_lists()

    def _rename(self):
        item = self._local_branches_list.currentItem()
        d = rename_branch_dialog.RenameBranchDialog(
            item and item.text() or str(),
            self
        )
        if d.exec_():
            self._git.rename_branch(d.old_name(), d.new_name())
            self._update_lists()
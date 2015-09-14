# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy

import create_branch_dialog
import git
import rename_branch_dialog
import delete_branch_dialog


class BranchesWidget(QtWidgets.QWidget):
    _git = git.Git()

    def __init__(self, parent=None):
        super(BranchesWidget, self).__init__(parent)

        self._local_branches_label = QtWidgets.QLabel("Local branches", self)
        self._local_branches_list = QtWidgets.QListWidget(self)

        self._remote_branches_label = QtWidgets.QLabel("Remote branches", self)
        self._remote_branches_list = QtWidgets.QListWidget(self)

        self._create_button = QtWidgets.QPushButton("Create", self)
        self._create_button.clicked.connect(self._create)

        self._checkout_button = QtWidgets.QPushButton("Checkout", self)
        self._checkout_button.clicked.connect(self._checkout)

        self._rename_button = QtWidgets.QPushButton("Rename", self)
        self._rename_button.clicked.connect(self._rename)

        self._delete_button = QtWidgets.QPushButton("Delete", self)
        self._delete_button.clicked.connect(self._delete)

        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.addWidget(self._checkout_button)
        buttons_layout.addWidget(self._create_button)
        buttons_layout.addWidget(self._rename_button)
        buttons_layout.addWidget(self._delete_button)

        buttons_layout.addSpacerItem(
            QtWidgets.QSpacerItem(
                0, 0, QSizePolicy.Preferred, QSizePolicy.Expanding
            )
        )

        tables_layout = QtWidgets.QVBoxLayout()
        tables_layout.addWidget(self._local_branches_label)
        tables_layout.addWidget(self._local_branches_list)
        tables_layout.addWidget(self._remote_branches_label)
        tables_layout.addWidget(self._remote_branches_list)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(tables_layout)
        main_layout.addLayout(buttons_layout)

        super(BranchesWidget, self).setLayout(main_layout)
        self._update_lists()

    def _update_lists(self):
        self._local_branches_list.clear()
        self._remote_branches_list.clear()

        current_branch = self._git.current_branch()

        for branch in self._git.local_branches():
            item = QtWidgets.QListWidgetItem(branch, self._local_branches_list)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self._local_branches_list.addItem(item)
            if current_branch == branch:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

        for branch in self._git.remote_branches():
            item = QtWidgets.QListWidgetItem(
                branch, self._remote_branches_list
            )

            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
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
        if item and item.checkState() != Qt.Checked:
            self._git.checkout(item.text())
            self._update_lists()

    def _rename(self):
        item = self._local_branches_list.currentItem()
        d = rename_branch_dialog.RenameBranchDialog(
            item and item.text() or self._git.current_branch(),
            self
        )
        if d.exec_():
            self._git.rename_branch(d.old_name(), d.new_name())
            self._update_lists()

    def _delete(self):
        item = self._local_branches_list.currentItem()
        d = delete_branch_dialog.DeleteBranchDialog(
            item and item.text() or str(),
            self
        )

        if d.exec_():
            self._update_lists()

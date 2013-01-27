# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore, QtGui
import create_branch_dialog
import git

class BranchesWidget(QtGui.QWidget):
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

        buttons_layout = QtGui.QVBoxLayout()
        buttons_layout.addWidget(self._create_button)
        buttons_layout.addWidget(self._checkout_button)
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

        current_branch = git.Git().current_branch()

        for branch in git.Git().local_branches():
            item = QtGui.QListWidgetItem(branch, self._local_branches_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self._local_branches_list.addItem(item)
            if current_branch == branch:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

        for branch in git.Git().remote_branches():
            item = QtGui.QListWidgetItem(branch, self._remote_branches_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self._remote_branches_list.addItem(item)

    def _create(self):
        d = create_branch_dialog.CreateBranchDialog(self)
        if d.exec_():
            _git = git.Git()
            _git.create_branch(d.branch_name(),
                                    d.parent_branch())
            if d.can_checkout():
                _git.checkout(d.branch_name())
            self._update_lists()

    def _checkout(self):
        item = self._local_branches_list.currentItem()
        if item and item.checkState() != QtCore.Qt.Checked:
            git.Git().checkout(item.text())
            self._update_lists()
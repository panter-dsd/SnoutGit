# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git


class MergeDialog(QtGui.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super(MergeDialog, self).__init__(parent)

        self._sources_tabs = QtGui.QTabBar(self)
        self._sources_tabs.addTab("Local branch")
        self._sources_tabs.addTab("Remote branch")
        self._sources_tabs.addTab("Tag")
        self._sources_tabs.currentChanged.connect(
            self._update_source
        )

        self._source_model = QtGui.QStringListModel(self)

        self._source_view = QtGui.QListView(self)
        self._source_view.setModel(self._source_model)

        self._source_target_label = QtGui.QLabel("Source target",
                                                 self)
        self._source_target_edit = QtGui.QLineEdit(self)
        self._source_view.clicked.connect(
            lambda index: self._source_target_edit.setText(
                index.data(QtCore.Qt.DisplayRole)
            )
        )

        source_target_layout = QtGui.QHBoxLayout()
        source_target_layout.addWidget(self._source_target_label)
        source_target_layout.addWidget(self._source_target_edit)

        self._commit_option = QtGui.QCheckBox(self)
        self._commit_option.setText("Commit")
        self._commit_option.setChecked(True)

        self._fast_forward_option = QtGui.QCheckBox(self)
        self._fast_forward_option.setText("Fast-forward")
        self._fast_forward_option.setChecked(False)

        self._squash_option = QtGui.QCheckBox(self)
        self._squash_option.setText("Squash")
        self._squash_option.setChecked(False)

        options_group = QtGui.QGroupBox(self)
        options_group.setTitle("Merge options")

        options_layout = QtGui.QHBoxLayout()
        options_layout.addWidget(self._commit_option)
        options_layout.addWidget(self._fast_forward_option)
        options_layout.addWidget(self._squash_option)
        options_group.setLayout(options_layout)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._sources_tabs)
        layout.addWidget(self._source_view)
        layout.addLayout(source_target_layout)
        layout.addWidget(options_group)

        super(MergeDialog, self).setLayout(layout)

        self._update_source(self._sources_tabs.currentIndex())

    def _update_source(self, current):
        model = self._source_model

        if current == 0:
            model.setStringList(self._git.local_branches())
        elif current == 1:
            model.setStringList(self._git.remote_branches())
        else:
            model.setStringList(self._git.tags())
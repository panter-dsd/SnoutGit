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
        self._squash_option.stateChanged.connect(self._option_changed)

        options_group = QtGui.QGroupBox(self)
        options_group.setTitle("Merge options")

        options_layout = QtGui.QHBoxLayout()
        options_layout.addWidget(self._commit_option)
        options_layout.addWidget(self._fast_forward_option)
        options_layout.addWidget(self._squash_option)
        options_group.setLayout(options_layout)

        buttons = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal,
                                         self)
        self._merge_button = QtGui.QPushButton(self)
        self._merge_button.setEnabled(False)
        self._merge_button.setText("Merge")
        self._source_target_edit.textChanged.connect(
            lambda: self._merge_button.setEnabled(
                bool(self._source_target_edit.text())
            )
        )

        buttons.addButton(self._merge_button,
                          QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton(QtGui.QDialogButtonBox.Cancel)

        buttons.accepted.connect(self._merge)
        buttons.rejected.connect(super(MergeDialog, self).reject)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._sources_tabs)
        layout.addWidget(self._source_view)
        layout.addLayout(source_target_layout)
        layout.addWidget(options_group)
        layout.addWidget(buttons)

        super(MergeDialog, self).setLayout(layout)

        self._update_source(self._sources_tabs.currentIndex())

    def _update_source(self, current):
        merged = set(self._git.merged(self._git.current_branch()))

        def not_merged(branches):
            return list(set(branches) - set(merged))

        objects = []

        if current == 0:
            objects = self._git.local_branches()
        elif current == 1:
            objects = self._git.remote_branches()
        else:
            objects = self._git.tags()

        self._source_model.setStringList(not_merged(objects))

    def _merge(self):
        target = self._source_target_edit.text()

        result = QtGui.QMessageBox.question(
            self,
            "Are you sure?",
            "Merge " + target + " into " + self._git.current_branch(),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

        if result == QtGui.QMessageBox.Ok:
            merge_options = git.MergeOptions(target)
            merge_options.commit = self._commit_option.isChecked()
            merge_options.fast_forward = self._fast_forward_option.isChecked()
            merge_options.squash = self._squash_option.isChecked()
            self._git.merge(merge_options)
            super(MergeDialog, self).accept()

    def _option_changed(self):
        is_squash = self._squash_option.isChecked()

        self._fast_forward_option.setEnabled(not is_squash)
        if is_squash and self._fast_forward_option.isChecked():
            self._fast_forward_option.setChecked(False)
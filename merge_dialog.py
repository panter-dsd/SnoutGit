# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtGui
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

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._sources_tabs)
        layout.addWidget(self._source_view)

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
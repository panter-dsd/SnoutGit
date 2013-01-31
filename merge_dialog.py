# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git


class AbstractSourceWidget(QtGui.QWidget):
    _git = None

    def __init__(self, git, parent=None):
        super(AbstractSourceWidget, self).__init__(parent)
        self._git = git

        self._sources_list = QtGui.QListWidget(self)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._sources_list)
        super(AbstractSourceWidget, self).setLayout(layout)
        self._update_lists()

    def _update_lists(self):
        pass



class LocalSourceWidget(AbstractSourceWidget):
    def __init__(self, git, parent=None):
        super(LocalSourceWidget, self).__init__(git, parent)

    def _update_lists(self):
        self._sources_list.clear()

        for branch in self._git.local_branches():
            item = QtGui.QListWidgetItem(branch, self._sources_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self._sources_list.addItem(item)


class RemoteSourceWidget(AbstractSourceWidget):
    def __init__(self, git, parent=None):
        super(RemoteSourceWidget, self).__init__(git, parent)
        self._git = git

    def _update_lists(self):
        self._sources_list.clear()

        for branch in self._git.remote_branches():
            item = QtGui.QListWidgetItem(branch, self._sources_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self._sources_list.addItem(item)

class TagsSourceWidget(AbstractSourceWidget):
    def __init__(self, git, parent=None):
        super(TagsSourceWidget, self).__init__(git, parent)
        self._git = git

    def _update_lists(self):
        self._sources_list.clear()

        for tag in self._git.tags():
            item = QtGui.QListWidgetItem(tag, self._sources_list)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self._sources_list.addItem(item)



class MergeDialog(QtGui.QDialog):
    _git = git.Git()

    def __init__(self, parent=None):
        super(MergeDialog, self).__init__(parent)

        self._sources_tabs = QtGui.QTabWidget(self)

        self._local_source = LocalSourceWidget(self._git, self)
        self._sources_tabs.addTab(self._local_source, "Local branch")

        self._remote_source = RemoteSourceWidget(self._git, self)
        self._sources_tabs.addTab(self._remote_source, "Remote branch")

        self._tags_source = TagsSourceWidget(self._git, self)
        self._sources_tabs.addTab(self._tags_source, "Tag")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._sources_tabs)
        super(MergeDialog, self).setLayout(layout)
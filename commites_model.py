# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore
import commit

import os
import subprocess


def get_commites_list(path):
    os.chdir(path)
    result = []
    command = "git log --pretty=format:%H"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    for line in process.stdout.readlines():
        result.append(commit.Commit(path, line.rstrip().decode()))
    return result


class CommitesModel(QtCore.QAbstractItemModel):
    """CommitesModel"""

    _commits_list = []

    def __init__(self, path, parent=None):
        """__init__"""
        super(CommitesModel, self).__init__(parent)
        self._path = path
        self.update_commits_list()

    def update_commits_list(self):
        old_commits_list = self._commits_list
        new_commits_list = get_commites_list(self._path)
        if old_commits_list == new_commits_list:
            return

        self._commits_list = new_commits_list

        old_size = len(old_commits_list)
        new_size = len(new_commits_list)

        if old_size != new_size:
            if old_size < new_size:
                QtCore.QAbstractItemModel.beginInsertRows(self,
                                                          QtCore.QModelIndex(),
                                                          old_size,
                                                          new_size - 1)
                QtCore.QAbstractItemModel.endInsertRows(self)
            else:
                QtCore.QAbstractItemModel.beginRemoveRows(self,
                                                          QtCore.QModelIndex(),
                                                          new_size,
                                                          old_size - 1)
                QtCore.QAbstractItemModel.endRemoveRows(self)

        for i in range(min(old_size, new_size)):
            if old_commits_list[i] != new_commits_list[i]:
                self.dataChanged.emit(self.index(i, 0),
                                      self.index(i, self.columnCount()))



    def index(self, row, column, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return QtCore.QModelIndex()

        return super(CommitesModel, self).createIndex(row, column)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._commits_list)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return 3

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return self._commits_list[index.row()].abbreviated_id()
            elif index.column() == 1:
                return self._commits_list[index.row()].name()
            elif index.column() == 2:
                return self._commits_list[index.row()].author()
        elif role == QtCore.Qt.ToolTipRole:
            if index.column() == 0:
                return self._commits_list[index.row()].id()
            elif index.column() == 1:
                return self._commits_list[index.row()].full_name()
            elif index.column() == 2:
                return self._commits_list[index.row()].author()

        return None

    def parent(self, index):
        return QtCore.QModelIndex()

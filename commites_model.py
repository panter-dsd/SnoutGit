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
        result.append(commit.Commit(path, line.strip().decode("utf-8")))
    return result


class CommitesModel(QtCore.QAbstractItemModel):
    """CommitesModel"""

    def __init__(self, path, parent=None):
        """__init__"""
        super(CommitesModel, self).__init__(parent)
        self._path = path
        self.update_commits_list()

    def update_commits_list(self):
        self._commits_list = get_commites_list(self._path)

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
                return self._commits_list[index.row()].id()
            elif index.column() == 1:
                return self._commits_list[index.row()].name()
            elif index.column() == 2:
                return self._commits_list[index.row()].author()
        return None

    def parent(self, index):
        return QtCore.QModelIndex()

__author__ = 'panter'

from PySide import QtCore

import os
import subprocess

class Commit(object):
    def __init__(self, path, id):
        super(Commit, self).__init__()
        self._path = path
        self._id = id
        self.name_ = str()
        self.author_ = str()

    def _commit_info(self, format_id):
        os.chdir(self._path)
        command = "git show -s --pretty=\"" + format_id + "\" " + self._id
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        return process.stdout.readline().strip().decode("utf-8")

    def id(self):
        return self._id

    def name(self):
        if len(self.name_) == 0:
            self.name_ = self._commit_info("%s")
        return self.name_

    def author(self):
        if len(self.author_) == 0:
            self.author_ = self._commit_info("%ae")
        return self.author_


def get_commites_list(path):
    os.chdir(path)
    result = []
    command = "git log --pretty=format:%H"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    for line in process.stdout.readlines():
        result.append(Commit(path, line.strip().decode("utf-8")))
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

# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtCore
import git


class CommitesModel(QtCore.QAbstractItemModel):
    """CommitesModel"""

    _commits_list = []
    _headers = ["Abbreviated id",
                "Comment",
                "Author",
                "Timestamp"]

    def __init__(self, parent=None):
        """__init__"""
        super(CommitesModel, self).__init__(parent)
        self.update_commits_list()

    def update_commits_list(self):
        old_commits_list = self._commits_list
        new_commits_list = git.Git().commites()
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
        return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return self._commits_list[index.row()].abbreviated_id()
            elif index.column() == 1:
                tags = str()
                for tag in self._commits_list[index.row()].tags_list():
                    tags += "[" + tag + "] "
                return tags + self._commits_list[index.row()].name()
            elif index.column() == 2:
                return self._commits_list[index.row()].author()
            elif index.column() == 3:
                return self._commits_list[index.row()].timestamp()
        elif role == QtCore.Qt.ToolTipRole:
            if index.column() == 0:
                return self._commits_list[index.row()].id()
            elif index.column() == 1:
                tags = str()
                _git = git.Git()
                for tag in self._commits_list[index.row()].tags_list():
                    tag_info =_git.tag_info(tag)
                    if len(tag_info) > 0:
                        tags += "\n".join(tag_info) + "\n\n"
                return tags + self._commits_list[index.row()].full_name()
            elif index.column() == 2:
                return self._commits_list[index.row()].author()
            elif index.column() == 3:
                return self._commits_list[index.row()].timestamp()

        return None

    def parent(self, index):
        return QtCore.QModelIndex()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._headers[section]

        return super(CommitesModel, self).headerData(section, orientation, role)
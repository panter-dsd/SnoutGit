# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore


def commit_date(commit):
    timestamp = int(commit.timestamp())
    return QtCore.QDateTime.fromTime_t(timestamp).toString(
        "yyyy-MM-dd hh:mm:ss"
    )


class CommitesModel(QtCore.QAbstractItemModel):
    _headers = ["Abbreviated id",
                "Comment",
                "Author",
                "Timestamp"]

    def __init__(self, git, parent=None):
        super().__init__(parent)
        self._git = git
        self._commits_list = []
        self.update_commits_list()

    def update_commits_list(self):
        old_commits_list = self._commits_list
        new_commits_list = self._git.commites()
        if old_commits_list == new_commits_list:
            return

        self._commits_list = new_commits_list

        old_size = len(old_commits_list)
        new_size = len(new_commits_list)

        if old_size != new_size:
            if old_size < new_size:
                QtCore.QAbstractItemModel.beginInsertRows(
                    self,
                    QtCore.QModelIndex(),
                    old_size,
                    new_size - 1)
                QtCore.QAbstractItemModel.endInsertRows(self)
            else:
                QtCore.QAbstractItemModel.beginRemoveRows(
                    self,
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

        return self.createIndex(row, column)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._commits_list)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._headers)

    def _is_index_correct(self, index):
        return index.row() in range(0, len(self._commits_list))

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not self._is_index_correct(index):
            return None

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return self._commits_list[index.row()].abbreviated_id()
            elif index.column() == 1:
                text = str()
                ref_names = self._commits_list[index.row()].ref_names()
                for tag in ref_names.tags():
                    text += "<" + tag + ">"
                for local in ref_names.locals():
                    text += "[" + local + "]"
                for remote in ref_names.remotes():
                    text += "[remote/" + remote + "]"
                return text + self._commits_list[index.row()].name()
            elif index.column() == 2:
                return self._commits_list[index.row()].author()
            elif index.column() == 3:
                return commit_date(self._commits_list[index.row()])
        elif role == QtCore.Qt.ToolTipRole:
            if index.column() == 0:
                return self._commits_list[index.row()].id()
            elif index.column() == 1:
                tags = str()
                ref_names = self._commits_list[index.row()].ref_names()
                for tag in ref_names.tags():
                    tag_info = self._git.tag_info(tag)
                    if tag_info:
                        tags += "\n".join(tag_info) + "\n\n"
                return tags + self._commits_list[index.row()].full_name()
            elif index.column() == 2:
                return self._commits_list[index.row()].author()
            elif index.column() == 3:
                return commit_date(self._commits_list[index.row()])
        elif role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return self._commits_list[index.row()].id()
            elif index.column() == 1:
                return self._commits_list[index.row()].full_name()
            elif index.column() == 2:
                return self._commits_list[index.row()].author()
            elif index.column() == 3:
                return commit_date(self._commits_list[index.row()])

        return None

    def parent(self, index):
        return QtCore.QModelIndex()

    def headerData(self,
                   section,
                   orientation,
                   role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return self._headers[section]

        return super(CommitesModel, self).headerData(section,
                                                     orientation,
                                                     role)
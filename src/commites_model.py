# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5.QtCore import Qt, QAbstractItemModel, QDateTime, QModelIndex


def commit_date(commit):
    try:
        timestamp = int(commit.timestamp())
    except ValueError:
        print("Error extract unix timestamp for commit: " + commit.id(),
              " timestamp - " + commit.timestamp())
        timestamp = 0

    return QDateTime.fromTime_t(timestamp).toString("yyyy-MM-dd hh:mm:ss")


class AbstractField(object):
    def __init__(self):
        super(AbstractField, self).__init__()

        self._commit = None

    def commit(self):
        return self._commit

    def set_commit(self, commit):
        self._commit = commit

    def title(self):
        return str()

    def data(self, role):
        if role == Qt.DisplayRole:
            return self._display_role_data()
        elif role == Qt.ToolTipRole:
            return self._tool_tip_role_data()
        elif role == Qt.EditRole:
            return self._edit_role_data()
        else:
            return None

    def _display_role_data(self):
        return None

    def _tool_tip_role_data(self):
        return None

    def _edit_role_data(self):
        return None


class AbbreviatedIdField(AbstractField):
    def title(self):
        return "Abbreviated id"

    def _display_role_data(self):
        return self.commit().abbreviated_id()

    def _edit_role_data(self):
        return self.commit().id()

    def _tool_tip_role_data(self):
        return self._edit_role_data()


class CommentField(AbstractField):
    def title(self):
        return "Comment"

    def _display_role_data(self):
        text = str()
        ref_names = self.commit().ref_names()
        for tag in ref_names.tags():
            text += "<" + tag + ">"
        for local in ref_names.locals():
            text += "[" + local + "]"
        for remote in ref_names.remotes():
            text += "[remote/" + remote + "]"
        return text + self.commit().name()

    def _tool_tip_role_data(self):
        tags = str()
        ref_names = self.commit().ref_names()
        for tag in ref_names.tags():
            tag_info = self.commit().git().tag_info(tag)
            if tag_info:
                tags += "\n".join(tag_info) + "\n\n"
        return tags + self.commit().full_name()

    def _edit_role_data(self):
        return self.commit().full_name()


class AuthorField(AbstractField):
    def title(self):
        return "Author"

    def _display_role_data(self):
        return self.commit().author()

    def _tool_tip_role_data(self):
        return self._display_role_data()

    def _edit_role_data(self):
        return self._display_role_data()


class TimestampField(AbstractField):
    def title(self):
        return "Timestamp"

    def _display_role_data(self):
        return commit_date(self.commit())

    def _tool_tip_role_data(self):
        return self._display_role_data()

    def _edit_role_data(self):
        return self._display_role_data()


class CommitesModel(QAbstractItemModel):
    _fields = [AbbreviatedIdField(),
               CommentField(),
               AuthorField(),
               TimestampField()]

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
                QAbstractItemModel.beginInsertRows(
                    self,
                    QModelIndex(),
                    0,
                    new_size - old_size - 1
                )

                QAbstractItemModel.endInsertRows(self)
            else:
                QAbstractItemModel.beginRemoveRows(
                    self,
                    QModelIndex(),
                    new_size,
                    old_size - 1
                )

                QAbstractItemModel.endRemoveRows(self)

                for i in range(min(old_size, new_size)):
                    if old_commits_list[i] != new_commits_list[i]:
                        self.dataChanged.emit(
                            self.index(i, 0),
                            self.index(i, self.columnCount())
                        )

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid():
            return QModelIndex()

        return self.createIndex(row, column)

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._commits_list)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._fields)

    def _is_index_correct(self, index):
        return index.row() in range(0, len(self._commits_list))

    def data(self, index, role=Qt.DisplayRole):
        if not self._is_index_correct(index):
            return None

        field = self._fields[index.column()]
        field.set_commit(self._commits_list[index.row()])
        return field.data(role)

    def parent(self, index):
        return QModelIndex()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self._fields[section].title()

        return super(CommitesModel, self).headerData(section,
                                                     orientation,
                                                     role)

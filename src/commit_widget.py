# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

import git
from commit import Commit


class CommitWidget(QtWidgets.QWidget):
    _git = git.Git()
    commited = pyqtSignal()

    def __init__(self, commites_model, parent=None):
        super(CommitWidget, self).__init__(parent)

        self._menu_button = QtWidgets.QToolButton(self)
        self._menu_button.setAutoRaise(True)
        self._menu_button.setPopupMode(
            QtWidgets.QToolButton.MenuButtonPopup
        )

        self._commites_model = commites_model

        self._commit_name_edit = QtWidgets.QLineEdit(self)
        self._set_completer(self._commites_model)

        self._save_button = QtWidgets.QToolButton(self)
        self._save_button.setAutoRaise(True)
        self._save_button.setText("Save")
        self._save_button.clicked.connect(self._commit)

        style = super(CommitWidget, self).style()
        icon = style.standardIcon(QtWidgets.QStyle.SP_DialogSaveButton)
        self._save_button.setIcon(icon)

        self._commit_description_edit = QtWidgets.QPlainTextEdit(self)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self._menu_button)
        top_layout.addWidget(self._commit_name_edit)
        top_layout.addWidget(self._save_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self._commit_description_edit)
        super(CommitWidget, self).setLayout(layout)

        self.save_action = QtWidgets.QAction(self)
        self.save_action.setText("Save")
        self.save_action.triggered.connect(self._commit)
        self.save_action.setShortcut(Qt.CTRL | Qt.Key_Return)

        self.ammend_action = QtWidgets.QAction(self)
        self.ammend_action.setText("Ammend last commit")
        self.refresh()

    def _commit(self):
        if not self._message_empty():
            commit_name = self._commit_name_edit.text()
            description = self._commit_description_edit.toPlainText()
            if self._git.commit(commit_name, description):
                self._commit_name_edit.clear()
                self._commit_description_edit.clear()
                self.commited.emit()
                self.refresh()
            else:
                error_text = self._git.last_error()
                if not error_text:
                    error_text = self._git.last_output()

                QtWidgets.QMessageBox.critical(
                    self, "Error", "\n".join(error_text)
                )
        else:
            QtWidgets.QMessageBox.critical(
                self, "Error", "Commit name is empty."
            )

    def _set_completer(self, commites_model):
        completer = QtWidgets.QCompleter(self._commit_name_edit)
        completer.setModel(commites_model)
        completer.setCompletionColumn(1)
        completer.setCompletionRole(Qt.EditRole)
        self._commit_name_edit.setCompleter(completer)

    def _commit_model_data(self, row, column, role=Qt.EditRole):
        return self._commites_model.index(row, column).data(role)

    @pyqtSlot()
    def refresh(self):
        menu = QtWidgets.QMenu(self._menu_button)

        count = min(10, self._commites_model.rowCount())
        for i in range(count):
            commit_message_action = QtWidgets.QAction(self)

            commit = Commit(
                self._git,
                self._commit_model_data(i, 0),
                self._commit_model_data(i, 1)
            )

            commit_message_action.setObjectName(commit.id())

            commit_message_action.setText(
                self.fontMetrics().elidedText(
                    commit.name(),
                    Qt.ElideRight,
                    500
                )
            )
            commit_message_action.triggered.connect(
                self.set_old_message
            )
            menu.addAction(commit_message_action)
            if count < 0:
                break
            count -= 1

        menu.addSeparator()
        menu.addAction(self.save_action)
        menu.addAction(self.ammend_action)

        self._menu_button.setMenu(menu)
        self.load_commit_message()

    def set_old_message(self):
        id = self.sender().objectName()
        text = Commit(self._git, id).full_name()
        self._commit_name_edit.setText(text.splitlines()[0])
        self._commit_description_edit.setPlainText(
            "\n".join(text.splitlines()[1:])
        )

    def load_commit_message(self):
        if self._message_empty():
            self._commit_description_edit.setPlainText(
                self._git.commit_message()
            )

    def _message_empty(self):
        return not (
            self._commit_name_edit.text()
            + self._commit_description_edit.toPlainText()
        )
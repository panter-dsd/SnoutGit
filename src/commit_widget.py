# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PyQt4 import QtCore, QtGui
import git
import commit


class CommitWidget(QtGui.QWidget):
    commited = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CommitWidget, self).__init__(parent)

        self._menu_button = QtGui.QToolButton(self)
        self._menu_button.setAutoRaise(True)
        self._menu_button.setPopupMode(
            QtGui.QToolButton.MenuButtonPopup
        )

        self._commit_name_edit = QtGui.QLineEdit(self)

        self._save_button = QtGui.QToolButton(self)
        self._save_button.setAutoRaise(True)
        self._save_button.setText("Save")
        self._save_button.clicked.connect(self._commit)

        style = super(CommitWidget, self).style()
        icon = style.standardIcon(QtGui.QStyle.SP_DialogSaveButton)
        self._save_button.setIcon(icon)

        self._commit_description_edit = QtGui.QPlainTextEdit(self)

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(self._menu_button)
        top_layout.addWidget(self._commit_name_edit)
        top_layout.addWidget(self._save_button)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self._commit_description_edit)
        super(CommitWidget, self).setLayout(layout)

        self.save_action = QtGui.QAction(self)
        self.save_action.setText("Save")
        self.save_action.triggered.connect(self._commit)
        self.save_action.setShortcut(QtCore.Qt.CTRL
                                     | QtCore.Qt.Key_Return)

        self.ammend_action = QtGui.QAction(self)
        self.ammend_action.setText("Ammend last commit")
        self.refresh()

    def _commit(self):
        commit_name = self._commit_name_edit.text()
        if len(commit_name) > 0:
            description = self._commit_description_edit.toPlainText()
            if git.Git().commit(commit_name, description):
                self._commit_name_edit.clear()
                self._commit_description_edit.clear()
                self.commited.emit()
                self.refresh()
        else:
            QtGui.QMessageBox.critical(self,
                                       "Error",
                                       "Commit name is empty.")

    @QtCore.pyqtSlot()
    def refresh(self):
        menu = QtGui.QMenu(self._menu_button)

        count = 10
        for commit in git.Git().commites():
            commit_message_action = QtGui.QAction(self)
            commit_message_action.setText(commit.name())
            commit_message_action.setObjectName(commit.id())
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

    def set_old_message(self):
        id = self.sender().objectName()
        text = commit.Commit(id).full_name()
        self._commit_name_edit.setText(text.splitlines()[0])
        self._commit_description_edit.setPlainText(
            "\n".join(text.splitlines()[1:])
        )
# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'

from PySide import QtGui
import git


class ActionsWidget(QtGui.QWidget):

    def __init__(self, path, parent=None):
        super(ActionsWidget, self).__init__(parent)

        _push_button = QtGui.QPushButton(self)
        _push_button.setText("Push")
        _push_button.clicked.connect(self.push)

        _pull_button = QtGui.QPushButton(self)
        _pull_button.setText("Pull")
        _pull_button.clicked.connect(self.pull)

        _svn_button = QtGui.QToolButton(self)
        _svn_button.setText("Svn")
        _svn_button.setSizePolicy(QtGui.QSizePolicy.Preferred,
                                  QtGui.QSizePolicy.Preferred)
        _svn_button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)

        rebase_action = QtGui.QAction(self)
        rebase_action.setText("Rebase")
        rebase_action.triggered.connect(self._svn_rebase)
        _svn_button.addAction(rebase_action)

        dcommit_action = QtGui.QAction(self)
        dcommit_action.setText("Dcommit")
        dcommit_action.triggered.connect(self._svn_dcommit)
        _svn_button.addAction(dcommit_action)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(_push_button)
        layout.addWidget(_pull_button)
        layout.addWidget(_svn_button)
        layout.addSpacerItem(QtGui.QSpacerItem(0,
                                               0,
                                               QtGui.QSizePolicy.Preferred,
                                               QtGui.QSizePolicy.Expanding))
        super(ActionsWidget, self).setLayout(layout)

    def push(self):
        git.Git().push()

    def pull(self):
        git.Git().pull()

    def _svn_rebase(self):
        git.Git().svn_rebase()

    def _svn_dcommit(self):
        git.Git().svn_dcommit()

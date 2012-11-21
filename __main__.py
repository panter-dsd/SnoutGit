# -*- coding: utf-8 -*-
__author__ = 'panter.dsd@gmail.com'


PATH = "/media/work/other/phradar"

import sys
from PySide import QtGui
import commites_model

def main():
    """main"""
    app = QtGui.QApplication(sys.argv)

    dialog = QtGui.QDialog()
    table = QtGui.QTableView(dialog)
    model = commites_model.CommitesModel(PATH, dialog)
    table.setModel(model)
    layout = QtGui.QHBoxLayout()
    layout.addWidget(table)
    dialog.setLayout(layout)
    dialog.show()
    dialog.resize(640, 480)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
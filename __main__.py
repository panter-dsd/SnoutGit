import setuptools.command

__author__ = 'panter'


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

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
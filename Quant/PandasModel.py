# -*- coding: utf-8 -*-
"""
@author: Taar
"""

# conversion of https://github.com/openwebos/qt/tree/master/examples/tutorials/modelview/2_formatting

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt as qt, Qt
from PyQt5.QtWidgets import QHeaderView
import pandas as pd
import tushare as ts
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self,  data):
        super(PandasModel, self).__init__()
        self.data = data

    def rowCount(self, n):
        return self.data.shape[0]

    def columnCount(self, n):
        return self.data.shape[1]

    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.data.columns[col]
        return None
        # logger.debug('row {}, col {}, role {}'.format(row, col, role))
        # if role == qt.DisplayRole:
        #     if row == 0 and col == 1:
        #         return '<--left'
        #     if row == 1 and col == 1:
        #         return 'right-->'
        #     return 'Row{}, Column{}'.format(row + 1, col + 1)
        # elif role == qt.FontRole:
        #     if row == 0 and col == 0:  # change font only for cell(0,0)
        #         boldFont = QtGui.QFont()
        #         boldFont.setBold(True)
        #         return boldFont
        # elif role == qt.BackgroundRole:
        #     if row == 1 and col == 2:  # change background only for cell(1,2)
        #         redBackground = QtGui.QBrush(qt.red)
        #         return redBackground
        # elif role == qt.TextAlignmentRole:
        #     if row == 1 and col == 1:  # change text alignment only for cell(1,1)
        #         return qt.AlignRight + qt.AlignVCenter
        # elif role == qt.CheckStateRole:
        #     if row == 1 and col == 0:  # add a checkbox to cell(1,0)
        #         return qt.Checked
    def sort(self, column, order):
        colname = self.data.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self.data.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self.data.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    # tableView = QtWidgets.QTableView()
    tableView = QtWidgets.QTableView()
    pro = ts.pro_api('ac147953b15f6ee963c164fc8ee8ef5228e58b75e5953ba5997ef117')
    data = pro.cyq_perf(ts_code='600000.SH')
    myModel = PandasModel(data)
    tableView.setModel(myModel)
    tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    tableView.show()
    tableView.resize(560, 200)
    app.exec_()



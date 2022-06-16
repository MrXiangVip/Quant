import threading
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QLCDNumber, QAbstractItemView, QHeaderView, QTableWidgetItem

# import Utils
from OptionalWidget_View import Optional_Ui_Form
import pandas as pd

from db.DataManager import DataManager
import tushare as ts

class OptionalFormWidget(QWidget, Optional_Ui_Form):
    def __init__(self, root):
        super(OptionalFormWidget, self).__init__(root)
        self.root = root
        self.setupUi(self)
        self.initWidget()
    def initWidget(self):
        # primary 列中的数据读取为str
        self.data =  DataManager().getOptional()

        table_rows = self.data.shape[0]
        table_columns = self.data.shape[1]
        input_table_header = self.data.columns.values.tolist()
        # 设置表格列数
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(table_rows)
        # 给tablewidget设置行列表头========================
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.hideColumn(1)
        self.updateTableWidget()
    def updateTableWidget(self):
        print("updateTableWidget")
        self.data = DataManager().getOptional()
        self.primaylist = self.data['primary'].tolist()
        print(self.primaylist)
        if len(self.primaylist)==0:
            print(" primary empty ")
        try:
            self.realData = ts.get_realtime_quotes(self.primaylist)
            self.realData = self.realData[['name', 'open', 'pre_close', 'price', 'high', 'low']]
            print("1.获取实时数据", self.realData)
            # 2. 更新df
            print("2.更新df")
            self.data['open'] = self.realData['open']
            self.data['pre_close'] = self.realData['pre_close']
            self.data['price'] = self.realData['price']
            self.data['high'] = self.realData['high']
            self.data['low'] = self.realData['low']
        except Exception as e:
            print("error", e)
        table_rows = self.data.shape[0]
        table_columns = self.data.shape[1]
        # 设置表格列数
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(table_rows)

        for row in range(self.data.shape[0]):
            for col in range(0, 11):
                if col in [0, 1, 2, 3, 4, 6, 7]:
                    # item = self.tableWidget.item(row, col)
                    # item.setText( str(self.df.loc[row][col]))
                    newItem = QTableWidgetItem()
                    newItem.setText(str(self.data.loc[row][col]))
                    self.tableWidget.setItem(row, col, newItem)
                elif  col in[5]:
                    # item = self.tableWidget.item(row, col)
                    # item.setText( str(self.df.loc[row][col]))
                    # item.setBackground( QColor(230,230,230,255) )
                    newItem = QTableWidgetItem()
                    newItem.setText(str(self.data.loc[row][col]))
                    newItem.setBackground( QColor(230,230,230,255) )
                    self.tableWidget.setItem(row, col, newItem)
        self.createTickTimer()

    def createTickTimer(self):
        print("create tick timer")
        timer = threading.Timer(1, self.updateTableWidget)
        timer.start()
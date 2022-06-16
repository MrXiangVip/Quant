import datetime
import threading

from PyQt5.QtWidgets import QWidget, QLCDNumber, QAbstractItemView, QHeaderView, QTableWidgetItem

# import Utils
from NewsWidget_View import News_Ui_Form
import pandas as pd

from db.DataManager import DataManager


class NewsEngineWidget(QWidget, News_Ui_Form):
    def __init__(self, root):
        super(NewsEngineWidget, self).__init__(root)
        self.root = root
        self.setupUi(self)
        self.initWindow()

    def initWindow(self):
        today = datetime.datetime.today()
        try:
            # primary 列中的数据读取为str
            self.df =  DataManager().getNews(today)
        except Exception as e:
            print("error", e)
        print("news ", self.df)
        table_rows = self.df.shape[0]
        table_columns = self.df.shape[1]
        input_table_header = self.df.columns.values.tolist()
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
        print("update table widget")
        today = datetime.datetime.today()

        # self.data = DataManager().getNews(today)

        self.createTickTimer()

    def createTickTimer(self):
        print("create tick timer")
        timer = threading.Timer(1, self.updateTableWidget)
        timer.start()

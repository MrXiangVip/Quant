import datetime
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QLCDNumber, QAbstractItemView, QHeaderView, QTableWidgetItem, QLabel

# import Utils
import settings
from NewsWidget_View import News_Ui_Form
import pandas as pd

from db.DataManager import DataManager


class NewsWidget(QWidget, News_Ui_Form):
    def __init__(self, root):
        super(NewsWidget, self).__init__(root)
        self.root = root
        self.setupUi(self)
        self.initWindow()

    def initWindow(self):
        today = datetime.datetime.today().date()
        # primary 列中的数据读取为str
        self.news_df =  DataManager().getNews(today)
        self.news_df.drop(columns='title', inplace=True)
        print("news_df ", self.news_df.shape)
        table_rows = self.news_df.shape[0]
        table_columns = self.news_df.shape[1]
        input_table_header = self.news_df.columns.values.tolist()
        # 设置表格列数
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(table_rows)
        # 给tablewidget设置行列表头========================
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setDefaultSectionSize( 60)
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        # self.tableWidget.hideColumn(1)
        # 1 显示 新闻widget
        for row in range(table_rows):
            for col in range(table_columns):
                if col in [2]:
                    widget = QWidget()
                    horizontalLayout = QtWidgets.QHBoxLayout()
                    items = self.news_df.loc[row][col]
                    print( type(items), items)
                    for item in items:
                        label = QLabel()
                        palete = QPalette()
                        palete.setColor(QPalette.Base, QColor(230, 20, 20, 100))
                        label.setPalette( palete )
                        label.setText( item )
                        label.setAutoFillBackground(True)
                        horizontalLayout.addWidget(label)
                    widget.setLayout(horizontalLayout)
                    self.tableWidget.setCellWidget(row, col, widget)

                else:
                    newItem = QTableWidgetItem(str(self.news_df.loc[row][col]))
                    newItem.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                    self.tableWidget.setItem(row, col, newItem)

        self.tableWidget.resizeRowsToContents()
        # self.updateTableWidget()
        self.createTickTimer()

    def updateTableWidget(self):
        print("update table widget")
        today = datetime.datetime.today().date()
        self.news_df = DataManager().getNews(today)
        self.news_df.drop(columns='title', inplace=True)
        print("news_df ", self.news_df.shape)
        table_rows = self.news_df.shape[0]
        table_columns = self.news_df.shape[1]
        input_table_header = self.news_df.columns.values.tolist()
        # 设置表格列数
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(table_rows)
        # 给tablewidget设置行列表头========================
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setDefaultSectionSize( 60)
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        # 1 显示 新闻widget
        for row in range(table_rows):
            for col in range(table_columns):
                if col in [2]:
                    widget = QWidget()
                    horizontalLayout = QtWidgets.QHBoxLayout()
                    items = self.news_df.loc[row][col]
                    print(type(items), items)
                    for item in items:
                        label = QLabel()
                        palete = QPalette()
                        palete.setColor(QPalette.Base, QColor(230, 20, 20, 100))
                        label.setPalette(palete)
                        label.setText(item)
                        label.setAutoFillBackground(True)
                        horizontalLayout.addWidget(label)
                    widget.setLayout(horizontalLayout)
                    self.tableWidget.setCellWidget(row, col, widget)

                else:
                    newItem = QTableWidgetItem(str(self.news_df.loc[row][col]))
                    newItem.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                    self.tableWidget.setItem(row, col, newItem)
        self.tableWidget.resizeRowsToContents()

    def createTickTimer(self):
        print("create tick timer")
        self.timer = QTimer(self)
        self.timer.timeout.connect( self.updateTableWidget )
        self.timer.start(settings.news_tick)

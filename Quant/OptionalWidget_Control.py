import threading
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QCursor
from PyQt5.QtWidgets import QWidget, QLCDNumber, QAbstractItemView, QHeaderView, QTableWidgetItem, QLineEdit, QMenu, \
    QAction

# import Utils
import settings
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
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.tableWidget.customContextMenuRequested.connect(self.createRightMenu )  ####右键菜单
        # self.updateTableWidget()
        for row in range(table_rows):
            for col in range(table_columns):
                if col in [ 8, 9]:
                    lineEdit = QLineEdit()
                    lineEdit.setText(str(self.data.loc[row][col]))
                    lineEdit.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    lineEdit.editingFinished.connect(self.itemEdit)
                    self.tableWidget.setCellWidget(row, col, lineEdit)
        self.createTickTimer()
    def updateTableWidget(self):
        print("update optional table widget")
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
            for col in range(table_columns):
                if col in [0, 1, 2, 3, 4, 6, 7]:
                    # item = self.tableWidget.item(row, col)
                    # item.setText( str(self.data.loc[row][col]))
                    newItem = QTableWidgetItem()
                    newItem.setText(str(self.data.loc[row][col]))
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(row, col, newItem)
                elif  col in[5]:
                    # item = self.tableWidget.item(row, col)
                    # item.setText( str(self.data.loc[row][col]))
                    # item.setBackground( QColor(230,230,230,255) )
                    newItem = QTableWidgetItem()
                    newItem.setText(str(self.data.loc[row][col]))
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    newItem.setBackground( QColor(230,230,230,255) )
                    self.tableWidget.setItem(row, col, newItem)
                elif col in [8]:
                    print(row, col,'->',  self.data.loc[row][col] )
                    if  pd.notnull(self.data.loc[row][col]) and self.data.loc[row][col].isdecimal():
                        if self.data.loc[row][8] > self.data.loc[row][5]:
                            item = self.tableWidget.cellWidget( row, col)
                            palete = QPalette()
                            palete.setColor(QPalette.Base, QColor(230, 20, 20, 100))
                            item.setPalette(palete)
                        else:
                            item = self.tableWidget.cellWidget( row, col)
                            palete = QPalette()
                            palete.setColor(QPalette.Base, QColor(250, 250, 250, 100))
                            item.setPalette(palete)

                elif col in [9]:
                    print(row, col,'->',  self.data.loc[row][col] )
                    if pd.notnull(self.data.loc[row][col]) and self.data.loc[row][col].isdecimal():
                        if self.data.loc[row][9] < self.data.loc[row][5]:
                            item = self.tableWidget.cellWidget( row, col)
                            palete = QPalette()
                            palete.setColor(QPalette.Base, QColor(230,20,20,100))
                            item.setPalette( palete)
                        else:
                            item = self.tableWidget.cellWidget( row, col)
                            palete = QPalette()
                            palete.setColor(QPalette.Base, QColor(250, 250, 250, 100))
                            item.setPalette(palete)

        # self.createTickTimer()

    def createTickTimer(self):
        print("create tick timer")
        # self.timer = threading.Timer( settings.time_tick, self.updateTableWidget)
        # self.timer.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect( self.updateTableWidget )
        self.timer.start(settings.time_tick)
    def itemEdit(self):
        curRow = self.tableWidget.currentRow()
        curCol = self.tableWidget.currentColumn()
        print("编辑了 ", curRow, curCol)
        cell = self.tableWidget.cellWidget(curRow, curCol)
        print(type(cell), str(cell.text()))
        self.data.iloc[curRow, curCol] = str(cell.text())
        print(self.data)
        DataManager().updateOptional( self.data )

    def createRightMenu(self,position):
        # 菜单对象
        print("createRightMenu postion", position)
        self.groupBox_menu = QMenu(self)

        self.actionHead = QAction(QIcon('icons/up2Top.svg'), u'置顶',self)
        self.actionHead.setShortcut('Ctrl+S')  # 设置快捷键
        self.groupBox_menu.addAction(self.actionHead)  # 把动作A选项添加到菜单

        self.actionUp = QAction(QIcon('icons/up.svg'), u'上移',self)
        self.actionUp.setShortcut('Ctrl+S')  # 设置快捷键
        self.groupBox_menu.addAction(self.actionUp)  # 把动作A选项添加到菜单

        self.actionDown = QAction(QIcon('icons/down.svg'), u'下移', self)
        self.groupBox_menu.addAction(self.actionDown)

        self.actionDelete = QAction(QIcon('icons/deleteRow.svg'), u'删除', self)
        self.groupBox_menu.addAction(self.actionDelete)

        self.actionHead.triggered.connect(self.swapHead )  # 将动作A触发时连接到槽函数 button
        self.actionUp.triggered.connect(self.swapForward )  # 将动作A触发时连接到槽函数 button
        # self.actionDown.triggered.connect(self.button_2)
        self.actionDelete.triggered.connect(self.deleteRow )

        self.groupBox_menu.popup(QCursor.pos())  # 声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，

    def swapForward(self):
        print("swap ")
        curRow = self.tableWidget.currentRow()
        if curRow == -1:
            print("未选择一行")
        elif curRow == 0:
            print("")
        else:
            curData = self.data.iloc[curRow].copy()
            forwardData = self.data.iloc[curRow - 1].copy()
            self.data.iloc[curRow - 1] = curData
            self.data.iloc[curRow] = forwardData
            DataManager().updateOptional(self.data)
            # self.tableWidget.setCurrentIndex(curRow-1)
            self.tableWidget.rowAt(curRow - 1)
    def swapHead(self):
        print("swap head")
        curRow = self.tableWidget.currentRow()
        if curRow == -1:
            print("未选择一行")
        elif curRow == 0:
            print("")
        else:
            curData = self.data.iloc[curRow].copy()
            headData = self.data.iloc[0].copy()
            self.data.iloc[0] = curData
            self.data.iloc[curRow] = headData
            DataManager().updateOptional(self.data)
            # self.tableWidget.setCurrentIndex(curRow-1)
            self.tableWidget.rowAt(curRow)
    def deleteRow(self):
        print("delete a row ")
        row = self.tableWidget.currentRow()
        print(row)
        self.tableWidget.removeRow(row)
        self.data.drop(labels=row, inplace=True)
        DataManager().updateOptional( self.data )
import threading
from datetime import datetime

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QLineEdit, QComboBox, QCheckBox, QTableWidgetItem, \
    QLCDNumber

import Utils
from TradeAddDialog_Model import AddStockDialog
from RecordAddDialog_Model import RecordAddDilaog
from TradeFormWidget_UI import Trade_Ui_Form
import pandas as pd

from Trader import Trader
import tushare as ts

class TradeFormWidget(QWidget, Trade_Ui_Form):
    # updateSignal = pyqtSignal()  #pyqt5信号要定义为类属性
    TraderAlive = False
    def __init__(self, root):
        super(TradeFormWidget, self).__init__(root)
        self.root = root
        self.setupUi(self)
        self.initTradeForm()
        self.startRealTime()
        self.trader = Trader(self.root)


    def initTradeForm(self):
        self.open_time = datetime.strptime(str(datetime.now().date()) + '8:00', '%Y-%m-%d%H:%M')
        self.close_time = datetime.strptime(str(datetime.now().date()) + '18:00', '%Y-%m-%d%H:%M')
        # 让内容扁平化显示，颜色同窗口标题颜色相同
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display( datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
        # 绑定事件
        self.pushButton.clicked.connect(self.addDialogShow)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_3.clicked.connect( self.swapForward )
        self.pushButton_4.clicked.connect(self.startUnattend )
        self.pushButton_5.clicked.connect(self.tradeBuyDialogShow )
        self.pushButton_6.clicked.connect(self.tradeSellDialogShow )
        # add you code here
        print("填入数据")
        try:
            # primary 列中的数据读取为str
            self.df = pd.read_csv(Utils.realstock_csv, dtype={'primary':str, 'code':str})
        except Exception as e:
            print(e)
            self.df = pd.DataFrame(columns=Utils.realstock_column)
            self.df.to_csv(Utils.realstock_csv, index=False)
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
        for row in range(table_rows):
            for col in range(table_columns):
                # if col in [1]:
                #     print(col, "set invisible")

                if col in [ 8, 9, 10,11]:
                    lineEdit = QLineEdit()
                    lineEdit.setText(str(self.df.loc[row][col]))
                    lineEdit.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    lineEdit.editingFinished.connect(self.itemEdit)
                    self.tableWidget.setCellWidget(row, col, lineEdit)

                elif col in [12]:
                    comBox = QComboBox()
                    comBox.addItems(Utils.combobox_text)
                    comboText=self.df.loc[row][col]
                    print("combo text ", comboText)
                    if pd.isnull(comboText):
                        comboIndex=0
                        comBox.setCurrentIndex(comboIndex)
                    else:
                        comBox.setCurrentText( comboText )
                    comBox.currentIndexChanged.connect(self.comboChange)
                    self.tableWidget.setCellWidget(row, col, comBox)

                elif col in [14]:
                    state = self.df.loc[row][col]
                    if state != True:
                        state = False
                    print("state", state)
                    checkBox = QCheckBox()
                    checkBox.setChecked(state)
                    checkBox.stateChanged.connect(self.checkChange)
                    self.tableWidget.setCellWidget(row, col, checkBox)

                else:
                    newItem = QTableWidgetItem(str(self.df.loc[row][col]))
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(row, col, newItem)



    def updateTradeForm(self):
        print("4. 刷新表格控件")
        print(self.df.shape, self.df)
        table_rows = self.df.shape[0]
        table_columns = self.df.shape[1]
        # 设置表格列数
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(table_rows)

        for row in range(self.df.shape[0]):
            for col in range(0, 11):
                if col in [0, 1, 2, 3, 4, 6, 7]:
                    # item = self.tableWidget.item(row, col)
                    # item.setText( str(self.df.loc[row][col]))
                    newItem = QTableWidgetItem()
                    newItem.setText(str(self.df.loc[row][col]))
                    self.tableWidget.setItem(row, col, newItem)
                elif  col in[5]:
                    # item = self.tableWidget.item(row, col)
                    # item.setText( str(self.df.loc[row][col]))
                    # item.setBackground( QColor(230,230,230,255) )
                    newItem = QTableWidgetItem()
                    newItem.setText(str(self.df.loc[row][col]))
                    newItem.setBackground( QColor(230,230,230,255) )
                    self.tableWidget.setItem(row, col, newItem)
                # elif col in[8]:
                #     print( self.df.loc[row][col])
                    # lineEditItem = self.tableWidget.cellWidget(row, col)
                    # lineEditText = lineEditItem.text()
                    # print( lineEditText, type(lineEditItem.text()))
                    # if pd.isnull( self.df.loc[row][col] ) :
                    #     lineEditItem.setStyleSheet("QLineEdit { background-color : black; color : gray; }")
                    # else:
                    #     textColor=255 -( float(lineEditText) -float(self.df.loc[row][4]) )/float(self.df.loc[row][4])*100
                    #     lineEditItem.setStyleSheet("QLineEdit { background-color : red; color : gray; }")

    def itemEdit(self):
        curRow = self.tableWidget.currentRow()
        curCol = self.tableWidget.currentColumn()
        print("编辑了 ", curRow, curCol)
        cell = self.tableWidget.cellWidget(curRow, curCol)
        print(type(cell), str(cell.text()))
        self.df.iloc[curRow, curCol] = str(cell.text())
        print(self.df)
        self.df.to_csv(Utils.realstock_csv, index=False)

    def checkChange(self, state):
        curRow = self.tableWidget.currentRow()
        curCol = self.tableWidget.currentColumn()
        print("选择框 ", curRow, curCol)
        cell = self.tableWidget.cellWidget(curRow, curCol)
        print(type(cell), cell.isChecked())
        self.df.iloc[curRow, curCol] = cell.isChecked()
        print(self.df)
        self.df.to_csv(Utils.realstock_csv, index=False)

    def comboChange(self, index):
        curRow = self.tableWidget.currentRow()
        curCol = self.tableWidget.currentColumn()
        print("列表框 ", curRow, curCol, index)
        cell = self.tableWidget.cellWidget(curRow, curCol)
        print(cell.currentText())
        self.df.iloc[curRow, curCol]= cell.currentText()
        self.df.to_csv(Utils.realstock_csv, index=False)

    def addDialogShow(self):
        print("点击了add")
        self.addDialog = AddStockDialog()
        self.addDialog.addStockSignal.connect(self.addStock)
        self.addDialog.show()

    def addStock(self, newdf):
        print("增加了", newdf)
        self.df = self.df.append(newdf, ignore_index=True)
        self.df.to_csv(Utils.realstock_csv, index=False)
        print("保存到csv")

    def delete(self):
        print("点击了删除")
        row = self.tableWidget.currentRow()
        print(row)
        self.tableWidget.removeRow(row)
        self.df.drop(labels=row, inplace=True)
        self.df.to_csv(Utils.realstock_csv, index=False)
		
    def swapForward(self):
        print("swap ")
        curRow = self.tableWidget.currentRow()
        if curRow == -1 :
            print("未选择一行")
        elif curRow==0:
            print("")
        else:
            curDF = self.df.loc[curRow]
            forwardDF = self.df.loc[curRow-1]
            self.df.loc[curRow-1]= curDF
            self.df.loc[curRow]= forwardDF
            self.df.to_csv(Utils.realstock_csv, index=False)
            # self.tableWidget.setCurrentIndex(curRow-1)
            self.tableWidget.rowAt(curRow-1)
			
    def startUnattend(self):
        if self.pushButton_4.isChecked() :
            print("开启无人值守")
            self.TraderAlive = True
        else:
            print("停止无人值守")
            self.TraderAlive = False

    def stopUnattend(self):
        print("停止无人值守")
        self.TraderAlive = False

    def tradeBuyDialogShow(self):
        print("点击了买入或卖出")
        curRow = self.tableWidget.currentRow()
        if curRow == -1 :
            print("未选择一行")
        else:
            rowData=self.df.loc[curRow]

            self.traderDialog = RecordAddDilaog(0, rowData, self.root)
            self.traderDialog.show()
    def tradeSellDialogShow(self):
        print("点击了买入或卖出")
        curRow = self.tableWidget.currentRow()
        if curRow == -1 :
            print("未选择一行")
        else:
            rowData=self.df.loc[curRow]

            self.traderDialog = RecordAddDilaog(1, rowData, self.root)
            self.traderDialog.show()
    def startRealTime(self):
        print("开启实时监测")
        self.updateTradeForm()
        # self.updateSignal.connect(self.updateTradeForm)
        global timer
        timer = threading.Timer(1, self.realtdata_timer)
        timer.start()

    def realtdata_timer(self):
        print("每秒钟运行检测")
        self.lcdNumber.display( datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
        # 1.获取数据
        self.primaylist = self.df['primary'].tolist()
        print(self.primaylist)
        try:
            self.realData = ts.get_realtime_quotes(self.primaylist)
            self.realData = self.realData[['name', 'open', 'pre_close', 'price', 'high', 'low']]
            print("1.获取实时数据", self.realData)
            # 2. 更新df
            print("2.更新df")
            self.df['open'] = self.realData['open']
            self.df['pre_close'] = self.realData['pre_close']
            self.df['price'] = self.realData['price']
            self.df['high'] = self.realData['high']
            self.df['low'] = self.realData['low']
        except Exception as e:
            print("error",e)

        # 3. 是否执行无人值守
        if self.TraderAlive == True:
            print("3.无人值守 working")
            table_rows = self.df.shape[0]
            table_columns = self.df.shape[1]
            for index, row in self.df.iterrows():
                print(index, row)
                if row['选中'] == True:
                    # 如果交易规则是买入, 还没有执行, 当前的价格小于等于 设置的买入价格 .则执行买入
                    if row['交易规则'] == '买入' and  pd.isnull(row['执行结果']) and pd.to_numeric(row['price']) <= row['买入价格']:
                        self.trader.buy(row['code'], row['name'], row['price'], row['买入数量'])
                    # 如果交易规则是先买后卖, 还没有执行, 当前的价格小于等于 设置的买入价格 .则执行买入
                    elif row['交易规则'] == '先买后卖' and pd.isnull(row['执行结果']) and pd.to_numeric(row['price']) <= row['买入价格']:
                        self.trader.buy(row['code'], row['name'], row['price'], row['买入数量'])
                    # 如果交易规则是先卖后买, 还没有执行, 当前的价格小于等于 设置的买入价格 .则执行买入
                    elif row['交易规则'] == '先卖后买' and row['执行结果'] == '已卖' and pd.to_numeric(row['price']) <= row['买入价格']:
                        self.trader.buy(row['code'], row['name'], row['price'], row['买入数量'])

                    elif row['交易规则'] == '卖出' and pd.isnull(row['执行结果']) and pd.to_numeric(row['price']) >= row['卖出价格']:
                        self.trader.sell(row['code'], row['name'], row['price'], row['买入数量'])
                    elif row['交易规则'] == '先卖后买' and pd.isnull(row['执行结果']) and pd.to_numeric(row['price']) >= row['卖出价格']:
                        self.trader.sell(row['code'], row['name'], row['price'], row['买入数量'])
                    elif row['交易规则'] == '先买后卖' and row['执行结果'] == '已买' and pd.to_numeric(row['price']) >= row['卖出价格']:
                        self.trader.sell(row['code'], row['name'], row['price'], row['买入数量'])
                else:
                    print("未选中")

        else:
            print("3.无人值守 Sleep")
        # 4. 是否更新表格
        print("4. 是否更新表格")
        if  datetime.now()> self.open_time and datetime.now()<self.close_time :
            # self.updateSignal.emit()  # 发射信号
            self.updateTradeForm()
        global timer
        timer = threading.Timer(Utils.ticktime, self.realtdata_timer)
        timer.start()

    def stopRealTime(self):
        print("停止实时监测")
        timer.cancel()



    def closeEvent(self, event):
        print("退出主窗口")
        self.stopRealTime()
        self.df.to_csv(Utils.realstock_csv, index=False)



from PyQt5.QtCore import  *
from PyQt5.QtGui import  *
from PyQt5.QtWidgets import  *
import sys
import tushare as ts
import time

from samples.DetailDialog import DetailDialog


class MyWin( QWidget ):
    def __init__(self):
        super().__init__()
        self.title = "复盘"
        self.top =100
        self.left =100
        self.width =800
        self.height =600
        self.initData()
        self.initWindow()
        self.initShortCut()

    def initData(self):
        print("initData")
        self.pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
        self.today = time.strftime("%Y%m%d", time.localtime())
        self.stock_basic = self.pro.stock_basic()
        self.stock_basic2 = self.stock_basic[['ts_code', 'name']]
        self.daily =self.pro.daily_basic(trade_date=self.today)
        self.data = self.daily.merge(self.stock_basic2)
        self.data['dv_ratio'] = self.data['dv_ratio'].astype(float)
        self.data['pe'] = self.data['pe'].astype(float)
        self.data.sort_values('dv_ratio', ascending=False, inplace=True)
        print( self.data.shape )

    def initWindow(self):
        print("initWindow")
        self.setWindowTitle( self.title)
        self.setGeometry( self.top, self.top, self.width, self.height)
        self.vBoxLayout=QVBoxLayout()
        self.hBoxLayout =QHBoxLayout()
        self.createTable()
        self.checkboxs = []
        for i in range(len(self.data.columns)):
            checkbox = QCheckBox( self )
            checkbox.setObjectName(self.data.columns[i])
            checkbox.setText( self.data.columns[i])
            self.checkboxs.append(checkbox)
        for i in range(len(self.checkboxs)):
            self.hBoxLayout.addWidget( self.checkboxs[i] )
        self.vBoxLayout.addLayout( self.hBoxLayout )
        self.vBoxLayout.addWidget( self.table )
        self.setLayout( self.vBoxLayout )
        self.show()

    def initShortCut(self):
        print("initShortCut")
        self.shortCutF = QShortcut( QKeySequence("Ctrl+G"), self)
        self.shortCutF.activated.connect( self.showTick )

    def showTick(self):
        print("showTick")
        dialog = DetailDialog( )
        dialog.show()
        print("show dialog")
    def createTable(self):
        print("createTable")
        self.table = QTableWidget()
        self.table.setRowCount( self.data.shape[0])
        self.table.setColumnCount( self.data.shape[1])
        self.table.setShowGrid(True)
        self.table.setHorizontalHeaderLabels( list(self.data.columns) )
        self.table.horizontalHeader().setSectionResizeMode( 1, QHeaderView.Stretch)
        #
        for row in range(self.data.shape[0]):
            for col in range( self.data.shape[1]):
                newItem = QTableWidgetItem()
                newItem.setText(str(self.data.loc[row][col]))
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.table.setItem(row, col, newItem)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.table_double_clicked)

    def addTableRow(self, table, row_data):
        # 功能： 在末尾添加新行
        row = table.rowCount()
        table.setRowCount(row + 1)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
        print(f"Added one row: {row_data}")
        print(f"totally, {row + 1} rows")

    def table_double_clicked(self, row, col):
        # 打印选中单元格的内容
        print(f" Value of cell ({row},{col}) is {self.table.item(row, col).text()}  ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWin()
    sys.exit(app.exec())

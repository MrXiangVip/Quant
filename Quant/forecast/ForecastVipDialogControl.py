

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHeaderView, QAbstractItemView, QTableWidgetItem

from forecast.ForecastVipDialog import ForecastVip_Ui_Dialog
from db.DataManager import DataManager


class ForecastVipDialogControl(QDialog,ForecastVip_Ui_Dialog):

    def __init__(self ):
        super(ForecastVipDialogControl,self).__init__()
        # self.root = root
        self.setupUi(self)

        # self.label.setText( "forecast " )
        self.init_dialog()

    def init_dialog(self):
        print("init dialog")
        self.update_dialog()

    def update_dialog(self):
        print("update dialog")
        self.data = DataManager().get_forecast_vip()
        self.table_rows = self.data.shape[0]
        table_columns = self.data.shape[1]
        input_table_header = self.data.columns.values.tolist()
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(self.table_rows)
        # 给tablewidget设置行列表头========================
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        # 水平方向，表格大小拓展到适当的尺寸
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().resizeSection(0,100)
        # self.tableWidget.horizontalHeader().resizeSection(2,100)

        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setDefaultSectionSize( 60)
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tableWidget.setSortingEnabled( True )
        # self.tableWidget.hideColumn(0)
        for row in range(self.table_rows):
            for col in range(table_columns):
                newItem = QTableWidgetItem(str(self.data.loc[row][col]))
                newItem.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.tableWidget.setItem(row, col, newItem)
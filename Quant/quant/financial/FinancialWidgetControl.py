from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QTableWidgetItem

import datetime


from .FinancialWidgetView import *
from .FinancialWidgetModel import *
from quant.financial.ForecastVipDialogControl import ForecastVipDialogControl


class BrokerWidget(QWidget, Broker_Ui_Form):
    def __init__(self, root):
        super(BrokerWidget, self).__init__(root)
        self.root = root
        self.model = BrokerWidgetModel();
        self.setupUi(self)
        self.initWindow()

    def initWindow(self):
        today = datetime.datetime.today().date()
        self.dateEdit.setDate(  today )
        self.dateEdit.setDisplayFormat('yyyy-MM-dd')

        # 设置日期的最大与最小值，在当前日期上，前后大约偏移10年
        self.dateEdit.setMinimumDate(QDate.currentDate().addDays(-3650))
        self.dateEdit.setMaximumDate(QDate.currentDate().addDays(3650))

        # 允许弹出日历控件
        self.dateEdit.setCalendarPopup(True)

        # 日期改变时触发
        self.dateEdit.dateChanged.connect(self.onDateChanged)

        self.pushButton.setText("业绩预告")
        self.pushButton.clicked.connect( self.showForecastVipDialog )

        self.pushButton_2.setText("财务指标")
        self.pushButton_2.clicked.connect(self.showIndicatorDialog )
        self.updateWindow( today )



    def updateWindow(self, date ):
        logger.debug("update window")
        # self.data = DataManager().getBrokerReport( date )
        if isinstance(date, QDate):
            date = date.toPyDate()
        # self.data = self.model.getBrokerReportData( date )
        self.data = self.model.get_forecast_vip(  )
        # 删除日期这列
        if self.data.empty :
            return
        # self.data.drop( labels='report_date', axis =1, inplace=True )
        self.table_rows = self.data.shape[0]
        table_columns = self.data.shape[1]
        input_table_header = self.data.columns.values.tolist()
        self.tableWidget.setColumnCount(table_columns)
        # 设置表格行数
        self.tableWidget.setRowCount(self.table_rows)
        # 给tablewidget设置行列表头========================
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
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

        # self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
    def onDateChanged(self, date):
        logger.debug( "date ",date)
        self.updateWindow( date )

    def showForecastVipDialog(self):
        self.forecast_vip_dialog = ForecastVipDialogControl()
        self.forecast_vip_dialog.show()

    def showIndicatorDialog(self):
        logger.info("showIndicatorDialog")

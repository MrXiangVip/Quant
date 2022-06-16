import threading
from datetime import datetime

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QCompleter, QLCDNumber
from PyQt5 import QtCore, QtWidgets

from MainWindow_View import Ui_MainWindow
from NewsWidget_Control import NewsEngineWidget

from OptionalWidget_Control import OptionalFormWidget
# from TradeFormWidget_Model import TradeFormWidget
from StockFundament_Control import StockFundamentControl
# from db.DBManager import stock_abbrev
from db.DataManager import DataManager


class MainWindow(QMainWindow, Ui_MainWindow):
    updateRecordSignal = pyqtSignal( object )

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.initWindow()

    def initWindow(self):
        print("init main window")
        # self.tab = QtWidgets.QWidget()
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("MainWindow", "Quant"))
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display( datetime.now().strftime('%Y-%m-%d %H:%M:%S') )

        # self.tab = QtWidgets.QWidget()
        self.tab = OptionalFormWidget(self)
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        # self.tab_2 = OptionalFormWidget(self)
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        # self.tab_2 = QtWidgets.QWidget()
        self.tab_3 = QtWidgets.QWidget()
        # self.tab_3 = NewsEngineWidget(self)
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "自选"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "行业"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "事件"))
        self.tabWidget.setCurrentIndex(0)

        self.stock_basic =  DataManager().getStockBasic()
        print("stock basic shape ", self.stock_basic.shape )
        self.index_basic = DataManager().getIndexBasic()
        print("index basic shape", self.index_basic.shape )
        self.completer = QCompleter( list(self.stock_basic['abbrevation']) +list(self.index_basic['abbrevation']) )
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.lineEdit.setCompleter( self.completer)
        #
        self.lineEdit.returnPressed.connect(self.showStockDialog )
        self.updateRecordSignal.connect( self.updateRecordForm )
        self.updateMainWindow()

    def updateMainWindow(self):
        print("更新窗口")
        self.lcdNumber.display(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.createTickTimer()

    def createTickTimer(self):
        # self.updateTableWidget()
        # global timer
        # 每天最多访问该接口2次  ,将定时器的间隔设置为12 个小时
        timer = threading.Timer(1, self.updateMainWindow)
        timer.start()

    def updateRecordForm(self, df):
        print("更新record 表单")
        self.tab_2.updateRecordForm(df)
    def closeEvent(self,event):
        print("窗体关闭")

    def showStockDialog(self):
        print("show stock dialog",self.lineEdit.text())
        self.name_row = self.stock_basic.loc[self.stock_basic['abbrevation']== self.lineEdit.text()]
        if self.name_row.empty:
            self.name_row = self.index_basic.loc[self.index_basic['abbrevation']== self.lineEdit.text()]
        if self.name_row.empty:
            print(" empty name ")
            return
        self.stockFundamentDailog = StockFundamentControl( self.name_row )
        # self.addDialog.addStockSignal.connect(self.addStock)
        self.stockFundamentDailog.show()
        self.lineEdit.clear()




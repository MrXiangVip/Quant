import threading
from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QCompleter, QLCDNumber
from PyQt5 import QtCore, QtWidgets

import settings
from IndustryWidget_Control import IndustryFormWidget

from MainWindow_View import Ui_MainWindow
from BrokerWidget_Control import BrokerWidget
from NewsWidget_Control import NewsWidget
from OptionalWidget_Control import OptionalFormWidget
# from TradeFormWidget_Model import TradeFormWidget
from StockFundament_Control import StockFundamentControl
# from db.DBManager import stock_abbrev
from db.DataManager import DataManager
import tushare as ts
from decimal import  *

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

        self.sz_data= ts.get_realtime_quotes('sh')
        self.label.setText('SZ: '+ self.sz_data.loc[0].price  )

        self.hs_data= ts.get_realtime_quotes('hs300')
        self.label_2.setText('HS: ' +self.hs_data.loc[0].price  )

        # self.tab = QtWidgets.QWidget()
        self.tab = OptionalFormWidget(self)
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")

        # self.tab_2 = QtWidgets.QWidget()
        self.tab_2 = IndustryFormWidget(self)
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        # self.tab_3 = QtWidgets.QWidget()
        self.tab_3 = NewsWidget(self)
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        # self.tab_4 = QtWidgets.QWidget()
        self.tab_4 = BrokerWidget(self)
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "??????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "??????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "??????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "??????"))
        self.tabWidget.setCurrentIndex(0)

        self.stock_basic =  DataManager().stock_basic
        print("stock basic shape ", self.stock_basic.shape )
        self.index_basic = DataManager().index_basic
        print("index basic shape", self.index_basic.shape )
        self.completer = QCompleter( list(self.stock_basic['abbrevation']) +list(self.index_basic['abbrevation']) )
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.lineEdit.setCompleter( self.completer)
        #
        self.lineEdit.returnPressed.connect(self.showStockDialog )
        self.updateRecordSignal.connect( self.updateRecordForm )
        self.createTickTimer()
    def updateMainWindow(self):
        print("????????????")
        self.lcdNumber.display(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.sz_data= ts.get_realtime_quotes('sh')
        # self.label.setText('SZ: ' +self.sz_data.loc[0].price  )
        if self.sz_data.loc[0].price >self.sz_data.loc[0].pre_close:
            self.label.setStyleSheet("color:red")
            self.label.setText( 'SZ: '+self.sz_data.loc[0].price  +'???'+str( Decimal(self.sz_data.loc[0].price) - Decimal(self.sz_data.loc[0].pre_close) ) )
        else:
            self.label.setStyleSheet("color:green")
            self.label.setText( 'SZ: '+self.sz_data.loc[0].price  +'???'+str( Decimal(self.sz_data.loc[0].price)- Decimal(self.sz_data.loc[0].pre_close) ) )

        self.hs_data= ts.get_realtime_quotes('hs300')
        # self.label_2.setText( 'HS: '+self.hs_data.loc[0].price  )
        if self.hs_data.loc[0].price >self.hs_data.loc[0].pre_close:
            self.label_2.setStyleSheet("color:red")
            self.label_2.setText( 'HS: '+self.hs_data.loc[0].price  +'???'+str( Decimal(self.hs_data.loc[0].price)- Decimal(self.hs_data.loc[0].pre_close) ) )
        else:
            self.label_2.setStyleSheet("color:green")
            self.label_2.setText( 'HS: '+self.hs_data.loc[0].price  +'???'+str( Decimal(self.hs_data.loc[0].price)- Decimal(self.hs_data.loc[0].pre_close) ) )

    def createTickTimer(self):
        # self.updateTableWidget()
        # global timer
        # ???????????????????????????2???  ,??????????????????????????????12 ?????????
        # timer = threading.Timer(settings.time_tick, self.updateMainWindow)
        # timer.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect( self.updateMainWindow )
        self.timer.start(settings.time_tick)

    def updateRecordForm(self, df):
        print("??????record ??????")
        self.tab_2.updateRecordForm(df)
    def closeEvent(self,event):
        print("????????????")

    def showStockDialog(self):

        print("show stock dialog",self.lineEdit.text())
        self.ts_code=None
        self.index_code=None
        ts_codes = self.stock_basic.loc[self.stock_basic['abbrevation']== self.lineEdit.text()].ts_code
        self.ts_code = ts_codes.iloc[0]

        if self.ts_code ==None:
            index_codes = self.index_basic.loc[self.index_basic['abbrevation']== self.lineEdit.text()].ts_code
            self.index_code = index_codes.iloc[0]
        if self.ts_code ==None and self.index_code ==None:
            print(" empty name ")
            return
        # self.name_row = self.name_row.reset_index()
        self.stockDailog = StockFundamentControl( ts_code=self.ts_code, index_code=self.index_code )
        # self.addDialog.addStockSignal.connect(self.addStock)
        self.lineEdit.setText("")
        self.stockDailog.show()





from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QLCDNumber

import tushare as ts

from Quant import settings
from Quant.financial import *
from Quant.optional import  *
from Quant.main  import *
from Quant.news import *
from Quant.settings import market
from Quant.strategy import *
from Quant.macro import *
class MainWindow(QMainWindow, Ui_MainWindow):
    updateSignal =pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setupUI(self)
        self.defaultMarket=settings.market[0]
        self.model = MainWindowModel()
        self.initWindow()

    def initWindow(self):
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("MainWindow", "Quant"))
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display( datetime.now().strftime('%Y-%m-%d %H:%M:%S') )

        # self.sz_data= ts.get_realtime_quotes('sh')
        # self.label.setText('SZ: '+ self.sz_data.loc[0].price  )
        #
        # self.hs_data= ts.get_realtime_quotes('hs300')
        # self.label_2.setText('HS: ' +self.hs_data.loc[0].price  )
        self.label.clicked.connect( self.updateMarket )
        self.label_2.clicked.connect( self.updateMarket )
        self.label_3.clicked.connect( self.updateMarket )
        # 自选
        # self.tab = QtWidgets.QWidget()
        self.tab = OptionalFormWidget(self)
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        # 财报
        # self.tab_2 = QtWidgets.QWidget()
        self.tab_2 = FinancialWidget(self)
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        # 新闻
        # self.tab_3 = QtWidgets.QWidget()
        self.tab_3 = NewsWidget(self)
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        # 策略
        # self.tab_4 = QtWidgets.QWidget()
        self.tab_4 = StrategyFormWidget(self)
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        # 宏观
        self.tab_5 = MacroFormWidget(self)
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5,"")

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "自选"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "财报"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "新闻"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "策略"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "宏观"))
        self.tabWidget.setCurrentIndex(0)

        self.createTickTimer()
    def createTickTimer(self):
        # self.updateTableWidget()
        # global timer
        # 每天最多访问该接口2次  ,将定时器的间隔设置为12 个小时
        # timer = threading.Timer(settings.time_tick, self.updateMainWindow)
        # timer.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect( self.updateMainWindow )
        self.timer.start(settings.index_tick)
    def updateMainWindow(self):
        # logger.debug("更新指数")
        print("更新指数")
        self.lcdNumber.display(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # self.sz_data= self.model.getSZRealtime()
        # # self.label.setText('SZ: ' +self.sz_data.loc[0].price  )
        # if self.sz_data.loc[0].price >self.sz_data.loc[0].pre_close:
        #     self.label.setStyleSheet("color:red")
        #     self.label.setText( 'SZ: '+self.sz_data.loc[0].price  +'↑'+str( Decimal(self.sz_data.loc[0].price) - Decimal(self.sz_data.loc[0].pre_close) ) )
        # else:
        #     self.label.setStyleSheet("color:green")
        #     self.label.setText( 'SZ: '+self.sz_data.loc[0].price  +'↓'+str( Decimal(self.sz_data.loc[0].price)- Decimal(self.sz_data.loc[0].pre_close) ) )
        #
        # self.hs_data= ts.get_realtime_quotes('hs300')
        # # self.label_2.setText( 'HS: '+self.hs_data.loc[0].price  )
        # if self.hs_data.loc[0].price >self.hs_data.loc[0].pre_close:
        #     self.label_2.setStyleSheet("color:red")
        #     self.label_2.setText( 'HS: '+self.hs_data.loc[0].price  +'↑'+str( Decimal(self.hs_data.loc[0].price)- Decimal(self.hs_data.loc[0].pre_close) ) )
        # else:
        #     self.label_2.setStyleSheet("color:green")
        #     self.label_2.setText( 'HS: '+self.hs_data.loc[0].price  +'↓'+str( Decimal(self.hs_data.loc[0].price)- Decimal(self.hs_data.loc[0].pre_close) ) )
        self.sz_data= self.model.getSZRealtime()
        print( self.sz_data.iloc[0]['涨跌幅'])
        if self.sz_data.iloc[0]['涨跌幅'] >0:
            self.label.setStyleSheet("color:red")
            self.label.setText('SZ: '+str(self.sz_data.iloc[0]['最新价']) +'↑' +str(self.sz_data.iloc[0]['涨跌幅']))
        else:
            self.label.setStyleSheet("color:green")
            self.label.setText('SZ: '+str(self.sz_data.iloc[0]['最新价']) +'↓' +str(self.sz_data.iloc[0]['涨跌幅']))
        self.hk_data= self.model.getHKRealtime()
        print( self.hk_data.iloc[0]['涨跌幅'])
        if self.hk_data.iloc[0]['涨跌幅'] >0:
            self.label_2.setStyleSheet("color:red")
            self.label_2.setText('HK: '+str(self.hk_data.iloc[0]['最新价']) +'↑' +str(self.hk_data.iloc[0]['涨跌幅']))
        else:
            self.label_2.setStyleSheet("color:green")
            self.label_2.setText('HK: '+str(self.hk_data.iloc[0]['最新价']) +'↓' +str(self.hk_data.iloc[0]['涨跌幅']))

        self.us_data= self.model.getUSRealtime()
        usRate=round(( (self.us_data.iloc[-1]['close'] -self.us_data.iloc[-2]['close'])/self.us_data.iloc[-2].close), 4)
        if usRate >0:
            self.label_3.setStyleSheet("color:red")
            self.label_3.setText('IXIC: '+str(self.us_data.iloc[-1].close) +'↑' +str( usRate ))
        else:
            self.label_3.setStyleSheet("color:green")
            self.label_3.setText('IXIC: '+str(self.us_data.iloc[-1].close) +'↓' +str( usRate ))

    def updateMarket(self):
        name = self.sender().objectName()
        if name == "label":
            self.defaultMarket="A"
        elif name == "label_2":
            self.defaultMarket ="HK"
        elif name=="label_3":
            self.defaultMarket ="US"
        self.updateSignal.connect( self.tab.initWidget )
        self.updateSignal.emit( self.defaultMarket)
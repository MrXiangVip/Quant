#
#
#
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QHeaderView
import pandas as pd

import settings

from ..optional import OptionalWidgetModel
from ..settings import logger
from db import DataManager

from .PandasModel import *
from .StockFundamentModel import  *
from .StockFundamentDialog import *

class StockFundamentControl(QDialog,StockFundament_Dialog):

    def __init__(self, ts_code=None, fund_code=None, name=None):
        super(StockFundamentControl,self).__init__()
        # self.root = root
        self.model =StockFundamentModel()
        self.setupUi(self)
        logger.debug(( ts_code, fund_code, name ))

        self.ts_code = ts_code
        self.fund_code = fund_code
        self.name = name
        self.stock_basic = DataManager().stock_basic
        self.fund_basic = DataManager().fund_basic
        if self.ts_code!=None :
            self.name = self.stock_basic.loc[ self.stock_basic.ts_code == self.ts_code].name.item()
            self.label.setText( ts_code+" "+str(self.name) )

        if self.fund_code !=None:
            self.name = self.fund_basic.loc[ self.fund_basic.ts_code == self.fund_code].name.item()
            self.label.setText( self.fund_code +" "+str(self.name) )

        #xshx add
        self.pushButton.setText( "加自选")
        self.pushButton.setIcon(QIcon(QPixmap("../icons/sub.svg")))
        self.pushButton.clicked.connect( self.addOption )

        self.tabWidget.setTabText(0, "财报")
        self.tabWidget.setTabText(1, "行业")
        self.tabWidget.setTabText(2, "券商")
        self.updateWindow()

    def updateWindow(self):
        #
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.tableview = QtWidgets.QTableView(self.tab)
        data = self.model.get_stock_fund_data( ts_code= self.ts_code, fund_code=self.fund_code )
        logger.debug( data )
        myModel = PandasModel(data)
        self.tableview.setModel(myModel)
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.tableview)

    def addOption(self):
        logger.debug( "addOption")
        # self.new_df = pd.DataFrame(data=None, columns=settings.optional_columns)
        # if self.ts_code!=None:
        #     self.new_df['name'] = self.name
        #     self.new_df['primary']= self.stock_basic.loc[ self.stock_basic.ts_code == self.ts_code].symbol
        #     self.new_df['code']= self.ts_code
        #
        # if self.fund_code!=None:
        #     self.new_df['name'] = self.name
        #     self.new_df['primary']= self.fund_basic.loc[self.fund_basic.ts_code==self.fund_code].symbol
        #     self.new_df['code']= self.fund_code
        # # self.new_df.fillna( value=None)
        # print( "new_df \n", self.new_df)
        # OptionalModel().addOptional( self.new_df.head(0) )
        # return

        self.newOption = dict.fromkeys( settings.optional_columns, None)
        logger.info(( self.ts_code, self.fund_code))
        if  self.ts_code:
            self.newOption['name'] = self.name
            self.newOption['code'] = self.ts_code
            self.newOption['primary'] = self.ts_code[:6]

        if  self.fund_code:
            self.newOption['name'] = self.name
            self.newOption['code'] = self.fund_code
            self.newOption['primary'] =self.fund_code[:6]
        print( self.newOption )
        OptionalWidgetModel().addOptional( self.newOption )

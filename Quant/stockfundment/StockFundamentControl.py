#
#
#
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QHeaderView

import settings
from PandasModel import PandasModel
from db.DataManager import DataManager
from stockfundment.StockFundamentDialog import StockFundament_Dialog
import pandas as pd
from settings import logger

from stockfundment.StockFundamentModel import StockFundamentModel


class StockFundamentControl(QDialog,StockFundament_Dialog):

    def __init__(self, ts_code=None, index_code=None, name=None):
        super(StockFundamentControl,self).__init__()
        # self.root = root
        self.setupUi(self)
        logger.debug( ts_code, index_code, name )

        self.ts_code = ts_code
        self.index_code = index_code
        self.name = name
        self.stock_basic = DataManager.stock_basic
        self.index_basic = DataManager.index_basic
        if self.ts_code!=None :
            self.name = self.stock_basic.loc[ self.stock_basic.ts_code == self.ts_code].name
            self.label.setText( ts_code+" "+str(self.name.values) )

        if self.index_code !=None:
            self.name = self.index_basic.loc[ self.index_basic.ts_code == self.index_code].name
            self.label.setText( self.index_code +" "+str(self.name.values) )

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
        data = StockFundamentModel().get_stock_zygc( ts_code= self.ts_code )
        logger.debug( data )
        myModel = PandasModel(data)
        self.tableview.setModel(myModel)
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.tableview)

    def addOption(self):
        logger.debug( "addOption")
        self.new_df = pd.DataFrame(data=None, columns=settings.optional_columns)
        if self.ts_code!=None:
            self.new_df['name'] = self.name
            self.new_df['primary']= self.stock_basic.loc[ self.stock_basic.ts_code == self.ts_code].symbol
            self.new_df['code']= self.ts_code

        if self.index_code!=None:
            self.new_df['name'] = self.name
            self.new_df['primary']= settings.stock_dic.get(self.name)
            self.new_df['code']= self.index_code
            logger.debug('name',  self.new_df['name'])
        # self.new_df.fillna( value=None)
        logger.debug( "new_df \n", self.new_df)
        StockFundamentModel.addOptional( self.new_df )
        return

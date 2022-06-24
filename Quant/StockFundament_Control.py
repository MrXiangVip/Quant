from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog

import settings
from StockFundament_Dialog import StockFundament_Dialog
import pandas as pd

from db.DataManager import DataManager


class StockFundamentControl(QDialog,StockFundament_Dialog):

    def __init__(self, basic_row):
        super(StockFundamentControl,self).__init__()
        # self.root = root
        self.setupUi(self)
        print("basic row \n", basic_row )
        self.basic_row= basic_row
        print( "self.basic_row", self.basic_row)
        self.label.setText( "".join( basic_row['name'].tolist() ) )

        #xshx add
        self.pushButton.setText( "加自选")
        self.pushButton.setIcon( QIcon(QPixmap("./icons/sub.svg")))
        self.pushButton.clicked.connect( self.addOption )

    def addOption(self):
        print( "addOption")
        if 'symbol' in list(self.basic_row.columns):
            self.new_df = pd.DataFrame( data=None, columns=settings.optional_columns)
            self.new_df['primary']= self.basic_row['symbol']
            self.new_df['code']= self.basic_row['ts_code']
            self.new_df['name'] = self.basic_row['name']
        else:
            self.new_df = pd.DataFrame( data=None, columns=settings.optional_columns)
            name = self.basic_row.loc[0, 'name']
            print('name', name,'->',settings.stock_dic.get(name))
            self.new_df['code']= self.basic_row['ts_code']
            self.new_df['name'] = self.basic_row['name']
            self.new_df['primary']= settings.stock_dic.get(name)
            print('name',  self.new_df['name'])
        # self.new_df.fillna( value=None)
        print( "new_df \n", self.new_df)
        DataManager().addOptional( self.new_df )
        return

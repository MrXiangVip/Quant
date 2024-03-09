# xshx add 20231117
# xshx mod 20240307
import os
import datetime

import pandas as pd
import numpy as np
import sqlalchemy
import tushare as ts
# import akshare as ak
import xpinyin
from xpinyin import  Pinyin


from quant.db import DataManager
from quant.settings import logger


class MainWindowModel():

    def __init__(self):
        self.dm = DataManager()
        self.stock_basic =self.dm.stock_basic
        self.fund_basic =self.dm.fund_basic
        self.getAbbrevationList()
        logger.info("data ready")
    def getAbbrevationList(self):
        logger.info("创建缩写词")
        # self.abbrevationStockList = list( self.dm.stock_basic['name'].apply(DataManager.getAbbrevation) )
        # self.abbrevationFundList = list( self.dm.fund_basic['name'].apply(DataManager.getAbbrevation) )
        self.stock_basic['abbrevation'] = self.stock_basic['name'].apply(DataManager.getAbbrevation)
        self.fund_basic['abbrevation'] = self.fund_basic['name'].apply(DataManager.getAbbrevation)
        self.abbrevationList = list(self.stock_basic['abbrevation']) + list(self.fund_basic['abbrevation'])
        logger.info( len(self.abbrevationList) )


if __name__ == '__main__':
            mainWindowModel = MainWindowModel()
            mainWindowModel.getAbbrevationList()
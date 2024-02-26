# 20231117
# data
import os
import datetime

import pandas as pd
import numpy as np
import sqlalchemy
import tushare as ts
import akshare as ak
import xpinyin
from xpinyin import  Pinyin

from db import DataManager
from settings import logger


class MainWindowModel():
    logger.info("创建缩写列")
    def __init__(self):
        self.dm = DataManager()
        self.stock_basic =self.dm.stock_basic
        self.index_basic =self.dm.index_basic

    def getAbbrevationList(self):
        self.abbrevationStockList = list( self.dm.stock_basic['name'].apply(DataManager.getAbbrevation) )
        self.abbrevationIndexList = list( self.dm.index_basic['name'].apply(DataManager.getAbbrevation) )
        # DataManager().stock_basic['abbrevation'] = DataManager().stock_basic['name'].apply(DataManager.getAbbrevation)
        # DataManager().index_basic['abbrevation'] = DataManager().index_basic['name'].apply(DataManager.getAbbrevation)
        self.abbrevationList = self.abbrevationStockList +self.abbrevationIndexList
        logger.info( len(self.abbrevationList) )


if __name__ == '__main__':
            mainWindowModel = MainWindowModel()
            mainWindowModel.getAbbrevationList()
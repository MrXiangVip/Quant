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

from db.DataManager import DataManager
from settings import logger


class MainWindowModel(DataManager):
    logger.info("创建缩写列")
    DataManager.stock_basic['abbrevation'] = DataManager.stock_basic['name'].apply(DataManager.getAbbrevation)
    DataManager.index_basic['abbrevation'] = DataManager.index_basic['name'].apply(DataManager.getAbbrevation)
    abbrevationList = list(DataManager.stock_basic['abbrevation']) + list(DataManager.index_basic['abbrevation'])
    logger.info( len(abbrevationList) )



if __name__ == '__main__':
            mainWindowModel = MainWindowModel()
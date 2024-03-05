#
import os
import datetime

import pandas as pd
import numpy as np
import sqlalchemy
import tushare as ts
# import akshare as ak
import xpinyin
from xpinyin import Pinyin
import  jieba
import settings
from .MetaBase import SingleMetaBase
from settings import logger

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
prefix = 'sqlite:///'
absPath=os.path.abspath('.')
dbName="tushare.db"
DataFile =  absPath +"/"+ dbName
print(DataFile)



class DataManager(metaclass=SingleMetaBase):

    def __init__(self):
        logger.debug("init datamanager")
        self.engine = sqlalchemy.create_engine(prefix + DataFile)
        self.pro = ts.pro_api('5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88')
        jieba.load_userdict('./company.csv')
        # stock_basic 每小时最多访问该接口一次, 先从网络获取列表信息, 如果网络上没有 从本地数据查找, 最后 再将列表保存到数据库中
        self.stock_basic = pd.DataFrame()
        self.fund_basic = pd.DataFrame()
        try:
            self.stock_basic = self.pro.stock_basic()
            # 场内基金
            self.fund_basic = self.pro.fund_basic(market='E')
            self.stock_basic.to_sql('stock_constant', self.engine, if_exists="replace")
            self.fund_basic.to_sql('fund_constant', self.engine, if_exists="replace")
            # 焦点词
            self.focus_words = self.stock_basic.name.tolist()
        except Exception as e:
            sql = '''select * from stock_constant'''
            self.stock_basic = pd.read_sql_query(sql, self.engine)
            sql = '''select * from fund_constant'''
            self.fund_basic = pd.read_sql_query(sql, self.engine)
        finally:
            logger.debug(("初始化 stock_basic ", self.stock_basic.shape, self.stock_basic.columns))
            logger.debug(("初始化 fund_basic ", self.fund_basic.shape, self.fund_basic.columns))
    # 将名称转成拼音
    def getAbbrevation( word):
        word = word.replace('-','')
        wordList = Pinyin().get_pinyin( word ).split('-')
        # logger.debug( wordList )
        wordAbbrevation = ''.join( i[0].lower() for i in wordList )
        wordAbbrevation +=' '
        wordAbbrevation += word
        return wordAbbrevation
    #
    def getFocus(self, content):
        words = jieba.lcut(content)  # 默认是精确模式
        logger.debug("分词后 ", words)
        focus =[]
        for word in words:
            if (word in self.focus_words)  and (word not in focus):
                focus.append( word )
        return focus


    # 描述：获取财报披露计划日期
    def get_disclosure_date(self):
        df = self.pro.disclosure_date(end_date='20220630')
        return  df



if __name__ == '__main__':
    dataManager = DataManager()
    # dataManager.getStockBasic()
    dataManager.getIndexBasic()
    # dataManager.getNews( datetime.date.today() )

    # https: // www.zhihu.com / column / akshare
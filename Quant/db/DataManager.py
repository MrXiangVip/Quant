#
import os
import datetime

import pandas as pd
import numpy as np
import sqlalchemy
import tushare as ts
import akshare as ak
import xpinyin
from xpinyin import Pinyin
import  jieba
import settings
from settings import logger

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
prefix = 'sqlite:///'
absPath=os.path.abspath('.')
dbName="tushare.db"
DataFile =  absPath +"/"+ dbName
print(DataFile)



class DataManager():
    engine = sqlalchemy.create_engine(prefix + DataFile)
    pro = ts.pro_api('ac147953b15f6ee963c164fc8ee8ef5228e58b75e5953ba5997ef117')
    jieba.load_userdict('./company.csv')
    # 先从网络获取列表信息, 如果网络上没有 从本地数据查找, 最后 再将列表保存到数据库中
    stock_basic=pd.DataFrame()
    index_basic=pd.DataFrame()
    try:
        stock_basic = pro.stock_basic()
        index_basic = pro.index_basic()
        focus_words = stock_basic.name.tolist()
        stock_basic.to_sql('stock_constant', engine, if_exists="replace")
        index_basic.to_sql('index_constant', engine, if_exists="replace")
    except Exception as e:
        sql = '''select * from stock_constant'''
        stock_basic = pd.read_sql_query(sql, engine)
        sql ='''select * from index_constant'''
        index_basic = pd.read_sql_query(sql, engine)
    finally:
        logger.debug(("stock_basic ", stock_basic.shape, stock_basic.columns))
        logger.debug(("index_basic ", index_basic.shape, index_basic.columns))


    def __init__(self):
        logger.debug("init datamanager")
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
    # def getStockBasic(self):
    #     logger.debug("getStockBasic")
    #     # 先从数据库中查表， 如果表不存在则从tushare 获取并replace到数据库
    #     try:
    #         sql ='''select * from stock_constant'''
    #         stock_basic = pd.read_sql_query(sql,self.engine)
    #         logger.debug("sql ", sql)
    #     except Exception as e:
    #         logger.debug("error ", e)
    #         stock_basic = self.pro.stock_basic()
    #         stock_basic['abbrevation']=stock_basic['name'].apply( self.getAbbrevation )
    #         stock_basic.to_sql('stock_constant',self.engine, if_exists="replace")
    #         logger.debug("get from tushare.stock_basic ")
    #     return  stock_basic
    #

    # def getIndexBasic(self):
    #     logger.debug("getIndexBasic")
    #     try:
    #         sql ='''select * from index_constant'''
    #         self.index_basic = pd.read_sql_query(sql, self.engine)
    #         logger.debug("sql ", sql)
    #     except Exception as e:
    #         logger.debug("error ", e)
    #         self.index_basic = self.pro.index_basic()
    #         self.index_basic['abbrevation'] = self.index_basic['name'].apply( self.getAbbrevation )
    #         self.index_basic.to_sql('index_constant',self.engine, if_exists="replace")
    #         logger.debug("get from tushare.index_basic ")
    #     return  self.index_basic


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

# 单例模式
# DataManagerInstance =DataManager()

if __name__ == '__main__':
    dataManager = DataManager()
    # dataManager.getStockBasic()
    dataManager.getIndexBasic()
    # dataManager.getNews( datetime.date.today() )

    # https: // www.zhihu.com / column / akshare
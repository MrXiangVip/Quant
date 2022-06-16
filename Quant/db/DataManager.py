import os
import datetime

import pandas as pd
import numpy as np
import sqlalchemy
import tushare as ts
import xpinyin
from xpinyin import Pinyin

import settings

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
prefix = 'sqlite:///'
absPath=os.path.abspath('.')
dbName="tushare.db"
DataFile =  absPath +"/"+ dbName
print( DataFile )
class DataManager():

    def __init__(self):
        self.engine = sqlalchemy.create_engine(prefix+DataFile)
        self.pro = ts.pro_api('ac147953b15f6ee963c164fc8ee8ef5228e58b75e5953ba5997ef117')

    # 将名称转成拼音
    def getAbbrevation(self, word):
        word = word.replace('-','')
        wordList = Pinyin().get_pinyin( word ).split('-')
        # print( wordList )
        wordAbbrevation = ''.join( i[0].lower() for i in wordList )
        wordAbbrevation +=' '
        wordAbbrevation += word
        return wordAbbrevation

    def getStockBasic(self):
        print("getStockBasic")
        # 先从数据库中查表， 如果表不存在则从tushare 获取并replace到数据库
        try:
            sql ='''select * from stock_constant'''
            self.stock_baic = pd.read_sql_query(sql,self.engine)
            print("sql ", sql)
        except Exception as e:
            print("error ", e)
            self.stock_baic = self.pro.stock_basic()
            self.stock_baic['abbrevation']=self.stock_baic['name'].apply( self.getAbbrevation )
            self.stock_baic.to_sql('stock_constant',self.engine, if_exists="replace")
            print("get from tushare.stock_basic ")
        return  self.stock_baic
    def getIndexBasic(self):
        try:
            sql ='''select * from index_constant'''
            self.index_basic = pd.read_sql_query(sql, self.engine)
            print("sql ", sql)
        except Exception as e:
            print("error ", e)
            self.index_basic = self.pro.index_basic()
            self.index_basic['abbrevation'] = self.index_basic['name'].apply( self.getAbbrevation )
            self.index_basic.to_sql('index_constant',self.engine, if_exists="replace")
            print("get from tushare.index_basic ")
        return  self.index_basic
    # 获取新闻数据
    def getNews(self, datestamp):
        print("get news", datestamp )

        # 先从数据库中查询 这天的新闻,如果数据库中不存在表，则去tushare 获取并插入表中
        start_date=str(datestamp - datetime.timedelta(days=1))
        end_date= str(datestamp)
        print( start_date, end_date )
        try:
            sql = '''select * from news where  datetime between {} and {}'''.format([start_date, end_date])
            print("sql ",sql)
            self.news_df = pd.read_sql_query( sql, self.engine )
        except Exception as e:
            print("error ", e )
            self.news_df = self.pro.news(start_date=start_date, end_date=end_date)
        #如果数据库中没有这天的新闻, 则去 tushare 获取并插入表中
        if self.news_df.empty :
                self.news_df = self.pro.news( start_date=start_date, end_date=end_date)
                self.news_df.to_sql('news', self.engine)
        return  self.news_df
    # 获取自选表数据
    def getOptional(self):
        print("getOptional")
        try:
            sql = '''select * from optional'''
            self.optional = pd.read_sql(sql, self.engine)
        except Exception as e:
            # 如果表不存在, 则创建空表 并写回数据库
            print("error ", e)
            self.optional = pd.DataFrame( data=None, columns=settings.optional_columns)
            self.optional.to_sql( 'optional', self.engine, index=False)
        return  self.optional
    def addOptional(self, new_optional):
        print( "addOptional")
        try:
            new_optional.to_sql( 'optional', self.engine, index=False, if_exists='append')
        except Exception as e:
            print("error ", e)
        return
if __name__ == '__main__':
    dataManager = DataManager()
    # dataManager.getStockBasic()
    dataManager.getIndexBasic()
    # dataManager.getNews( datetime.date.today() )
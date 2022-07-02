import os
import datetime

import pandas as pd
import numpy as np
import sqlalchemy
import tushare as ts
import xpinyin
from xpinyin import Pinyin
import  jieba
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
        jieba.load_userdict('./company.csv')
        self.stock_baic = self.getStockBasic()
        self.focus_words= self.stock_baic.name.tolist()
    # 将名称转成拼音
    def getAbbrevation(self, word):
        word = word.replace('-','')
        wordList = Pinyin().get_pinyin( word ).split('-')
        # print( wordList )
        wordAbbrevation = ''.join( i[0].lower() for i in wordList )
        wordAbbrevation +=' '
        wordAbbrevation += word
        return wordAbbrevation
#    #
    def getStockBasic(self):
        print("getStockBasic")
        # 先从数据库中查表， 如果表不存在则从tushare 获取并replace到数据库
        try:
            sql ='''select * from stock_constant'''
            stock_baic = pd.read_sql_query(sql,self.engine)
            print("sql ", sql)
        except Exception as e:
            print("error ", e)
            stock_baic = self.pro.stock_basic()
            stock_baic['abbrevation']=self.stock_baic['name'].apply( self.getAbbrevation )
            stock_baic.to_sql('stock_constant',self.engine, if_exists="replace")
            print("get from tushare.stock_basic ")
        return  stock_baic
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
    def updateOptional(self, new_optional):
        print("update optional")
        try:
            new_optional.to_sql( 'optional', self.engine, index=False, if_exists='replace')
        except Exception as e:
            print("error ", e)
        return
#   #
    def getFocus(self, content):
        words = jieba.lcut(content)  # 默认是精确模式
        print("分词后 ", words)
        focus =[]
        for word in words:
            if (word in self.focus_words)  and (word not in focus):
                focus.append( word )
        return focus
    # 获取新闻数据
    def getNews(self, start_date, end_date=0):
        print("get news","start date ->", start_date, "end date ->", end_date )
        today = datetime.datetime.today().date()
        # 先从数据库中查询 这天的新闻,如果数据库中不存在表，则去tushare 获取并插入表中
        self.news_df = pd.DataFrame()
        if start_date.date() ==  today:
            if end_date==0:
                self.news_df = self.pro.news( start_date = str(start_date.date()) )
                self.news_df['focus'] = self.news_df['content'].apply( self.getFocus )

            else:
                self.news_df = self.pro.news( start_date=str(start_date), end_date= str(end_date) )
                self.news_df['focus'] = self.news_df['content'].apply( self.getFocus )
                # try:
                #     sql = '''select * from news where  datetime between {} and {}'''.format([start_date, end_date])
                #     print("sql ",sql)
                #     self.news_df = pd.read_sql_query( sql, self.engine )
                # except Exception as e:
                #     print("error ", e )
                #     self.news_df = self.pro.news(start_date=start_date, end_date=end_date)
                # #如果数据库中没有这天的新闻, 则去 tushare 获取并插入表中
                # if self.news_df.empty :
                #         self.news_df = self.pro.news( start_date=start_date, end_date=end_date)
                #         self.news_df.to_sql('news', self.engine)

        else:
            print( "start ", start_date, " end ",end_date)
        return  self.news_df
    #

    #
    def getBrokerReportData(self, report_date=0, ts_code=0):
        print("卖方盈利预测数据 ",  report_date )
        if ts_code==0:
            data = self.pro.report_rc( report_date= report_date.strftime("%Y%m%d") )
        elif report_date ==0:
            data = self.pro.report_rc( ts_code= ts_code )
        else:
            data = self.pro.report_rc( ts_code= ts_code, report_date= report_date.strftime("%Y%m%d") )

        return data


    def get_ths_index(self):
        print("get ths index ")
        df = self.pro.ths_index(**{
            "ts_code": "",
            "exchange": "",
            "type": "",
            "limit": "",
            "offset": ""
        }, fields=[
            "ts_code",
            "name",
            "count",
            "exchange",
            "list_date",
            "type"
        ])
        # print(df)
        return df

    def get_ths_member(self , ts_code):
        print("get ths member")
        df = self.pro.ths_member( ts_code= ts_code)
        return  df

    def get_forecast_vip(self):
        df = self.pro.forecast_vip()
        return  df
if __name__ == '__main__':
    dataManager = DataManager()
    # dataManager.getStockBasic()
    dataManager.getIndexBasic()
    # dataManager.getNews( datetime.date.today() )
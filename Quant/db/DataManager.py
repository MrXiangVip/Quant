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
        self.stock_basic = self.getStockBasic()
        self.index_basic = self.getIndexBasic()
        self.focus_words= self.stock_basic.name.tolist()
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
            stock_basic = pd.read_sql_query(sql,self.engine)
            print("sql ", sql)
        except Exception as e:
            print("error ", e)
            stock_basic = self.pro.stock_basic()
            stock_basic['abbrevation']=stock_basic['name'].apply( self.getAbbrevation )
            stock_basic.to_sql('stock_constant',self.engine, if_exists="replace")
            print("get from tushare.stock_basic ")
        return  stock_basic

    def getIndexBasic(self):
        print("getIndexBasic")
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
        try:
            if start_date.date() ==  today:
                if end_date==0:
                    self.news_df = self.pro.news( start_date = str(start_date.date()) )
                    self.news_df['focus'] = self.news_df['content'].apply( self.getFocus )

                else:
                    self.news_df = self.pro.news( start_date=str(start_date), end_date= str(end_date) )
                    self.news_df['focus'] = self.news_df['content'].apply( self.getFocus )

            else:
                print( "start ", start_date, " end ",end_date)
        except Exception as e:
            print("error", e)
        return  self.news_df
    #

    #
    def getBrokerReportData(self, report_date=0, ts_code=0):
        print("卖方盈利预测数据 ",  report_date )
        data = pd.DataFrame()
        try:
            if ts_code==0:
                data = self.pro.report_rc( report_date= report_date.strftime("%Y%m%d") )
            elif report_date ==0:
                data = self.pro.report_rc( ts_code= ts_code )
            else:
                data = self.pro.report_rc( ts_code= ts_code, report_date= report_date.strftime("%Y%m%d") )
        except Exception as e:
            print("error ", e)
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
    # 用akshare 获取实时的指数行情
    def get_real_ths_member(self , ts_code):
        print("get real ths member ")
        index_code= ts_code[0:6]

        stock_board_cons_ths_df = ak.stock_board_cons_ths(symbol= index_code)
        stock_board_cons_ths_df['流通市值'] = stock_board_cons_ths_df['流通市值'].str.replace('亿', '').astype(float)
        stock_board_cons_ths_df = stock_board_cons_ths_df.sort_values( by='流通市值').drop(columns='序号').reset_index()
        stock_board_cons_ths_df['流通市值'] = stock_board_cons_ths_df['流通市值'].apply(lambda x: str(x) + '亿')

        return  stock_board_cons_ths_df

    def get_forecast_vip(self):
        df = self.pro.forecast_vip()
        data = self.stock_basic[['ts_code','name']]
        df = data.merge(df, how='right', on='ts_code')
        return  df

    # 描述：获取财报披露计划日期
    def get_disclosure_date(self):
        df = self.pro.disclosure_date(end_date='20220630')
        return  df
    # 主营
    def get_stock_zygc(self, ts_code):
        print( "get stock zygc", ts_code)
        code = ts_code[0:6]
        stock_zygc_ym_df = ak.stock_zygc_ym(symbol = code)
        return  stock_zygc_ym_df
# 单例模式
DataManagerInstance =DataManager()

if __name__ == '__main__':
    dataManager = DataManager()
    # dataManager.getStockBasic()
    dataManager.getIndexBasic()
    # dataManager.getNews( datetime.date.today() )

    # https: // www.zhihu.com / column / akshare
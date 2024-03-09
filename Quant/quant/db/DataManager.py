# xshx add 20240307
from pymongo import MongoClient
from .MetaBase import SingleMetaBase
import tushare as ts
import pandas as pd
from xpinyin import Pinyin

# 用元类实现单例模式  , 用来保存数据库连接, 和tushare 的验证码
# from ..settings import logger


class DataManager(metaclass=SingleMetaBase):
    settings = {
        "host": 'mongodb://localhost:27017',
        "db_name": "tushare"
    }
    def __init__(self):
        print("init data manager")
        self.client = MongoClient(DataManager.settings['host'])
        self.db = self.client[DataManager.settings['db_name']]
        self.pro = ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
        self.stock_basic = self.pro.stock_basic()
        self.fund_basic = self.pro.fund_basic(market='E')


    # 将名称转成拼音
    def getAbbrevation( word):
        word = word.replace('-','')
        wordList = Pinyin().get_pinyin( word ).split('-')
        # logger.debug( wordList )
        wordAbbrevation = ''.join( i[0].lower() for i in wordList )
        wordAbbrevation +=' '
        wordAbbrevation += word
        return wordAbbrevation
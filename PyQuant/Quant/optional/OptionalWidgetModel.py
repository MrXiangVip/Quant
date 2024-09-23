from tarfile import data_filter

import akshare as ak

import pandas as pd
class OptionalWidgetModel( ):

    def __init__(self):
        print("OptionalModel")


    def getAData(self):
        # 目标地址: https://quote.eastmoney.com/center/gridlist.html#hs_a_board
        # 描述: 东方财富网-沪深京 A 股-实时行情数据
        # 限量: 单次返回所有沪深京 A 股上市公司的实时行情数据
        stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
        return  stock_zh_a_spot_em_df

    def getHKData(self):
        # 目标地址: http://quote.eastmoney.com/center/gridlist.html#hk_stocks
        # 描述: 所有港股的实时行情数据; 该数据有 15 分钟延时
        # 限量: 单次返回最近交易日的所有港股的数据
        stock_hk_spot_em_df = ak.stock_hk_spot_em()
        return stock_hk_spot_em_df

    def getUSData(self):
        # 目标地址: https://quote.eastmoney.com/center/gridlist.html#us_stocks
        # 描述: 东方财富网-美股-实时行情
        # 限量: 单次返回美股所有上市公司的实时行情数据
        stock_us_spot_em_df = ak.stock_us_spot_em()
        print(stock_us_spot_em_df)
        return  stock_us_spot_em_df

    def getMarketData(self, market):
        df=pd.DataFrame()
        if market =="A":
            df= self.getAData()
        elif market =="HK":
            df = self.getHKData()
        elif market =="US":
            df = self.getUSData()
        return df
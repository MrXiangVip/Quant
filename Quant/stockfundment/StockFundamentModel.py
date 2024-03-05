from db import DataManager

# import akshare as ak
from settings import logger

class StockFundamentModel():

    def __init__(self):
        self.dm = DataManager()
    # 主营
    def get_stock_fund_data(self, ts_code=None, fund_code=None):
        logger.debug( "get_stock_fund_data", ts_code, fund_code)
        if ts_code != None:
            company = self.dm.pro.stock_company( ts_code=ts_code )
            return  company
        elif fund_code !=None:
            fund = self.dm.pro.fund_portfolio( ts_code=ts_code )
            return  fund
        return None
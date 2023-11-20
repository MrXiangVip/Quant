from db.DataManager import DataManager

import akshare as ak
from settings import logger

class StockFundamentModel(DataManager):
    # 主营
    def get_stock_zygc(self, ts_code):
        logger.debug( "get stock zygc", ts_code)
        code = ts_code[0:6]
        stock_zygc_ym_df = ak.stock_zygc_ym(symbol = code)
        return  stock_zygc_ym_df
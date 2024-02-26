#
from db import DataManager

import akshare as ak
from settings import logger

class IndustryWidgetModel( ):

    def __init__(self):
        self.pro = DataManager()

    def get_ths_index(self):
        logger.debug("get ths index ")
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
        # logger.debug(df)
        return df

    def get_ths_member(self , ts_code):
        logger.debug("get ths member")
        df = self.pro.ths_member( ts_code= ts_code)
        return  df
    # 用akshare 获取实时的指数行情
    def get_real_ths_member(self , ts_code):
        logger.debug("get real ths member ")
        index_code= ts_code[0:6]

        stock_board_cons_ths_df = ak.stock_board_cons_ths(symbol= index_code)
        stock_board_cons_ths_df['流通市值'] = stock_board_cons_ths_df['流通市值'].str.replace('亿', '').astype(float)
        stock_board_cons_ths_df = stock_board_cons_ths_df.sort_values( by='流通市值').drop(columns='序号').reset_index()
        stock_board_cons_ths_df['流通市值'] = stock_board_cons_ths_df['流通市值'].apply(lambda x: str(x) + '亿')

        return  stock_board_cons_ths_df
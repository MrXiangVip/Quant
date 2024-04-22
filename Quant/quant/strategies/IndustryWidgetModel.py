#
from db import DataManager

# import akshare as ak
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
    # 获取股息率和pe 的排名数据
    def get_ratio_and_pe(self):
        # 描述：获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等。
        df =self.pro.daily_basic()
        stock_basic2=self.stock_basic[['ts_code','name']]
        df2=stock_basic2.merge(df)
        df2['dv_ratio'] =df2['dv_ratio'].astype(float)
        df2['pe']=df2['pe'].astype(float)
        # df2.sort_values('dv_ratio',ascending=False, inplace=True)
        # df2.to_excel('df2.xlsx')
        return  df2
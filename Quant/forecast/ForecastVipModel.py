#
#
#
from db import DataManager


class ForecastVipModel( ):
    def __init__(self):
        self.dm = DataManager()
        self.pro = self.dm.pro

    def get_forecast_vip(self):
        df = self.pro.forecast_vip()
        data = self.stock_basic[['ts_code','name']]
        df = data.merge(df, how='right', on='ts_code')
        return  df


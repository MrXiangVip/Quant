#
#
#
from db.DataManager import DataManager


class ForecastVipModel(DataManager):

    def get_forecast_vip(self):
        df = self.pro.forecast_vip()
        data = self.stock_basic[['ts_code','name']]
        df = data.merge(df, how='right', on='ts_code')
        return  df


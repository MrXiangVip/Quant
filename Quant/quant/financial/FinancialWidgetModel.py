#
#
#

import pandas as pd

from ..db import DataManager
from ..settings import logger


class BrokerWidgetModel():
    def __init__(self):
        self.dm = DataManager()
        self.pro = self.dm.pro
        self.stock_basic = self.dm.stock_basic
    #
    def getBrokerReportData(self, report_date=0, ts_code=0):
        logger.debug(("卖方盈利预测数据 ",  report_date ))
        data = pd.DataFrame()
        try:
            if ts_code==0:
                data = self.pro.report_rc( report_date= report_date.strftime("%Y%m%d") )
            elif report_date ==0:
                data = self.pro.report_rc( ts_code= ts_code )
            else:
                data = self.pro.report_rc( ts_code= ts_code, report_date= report_date.strftime("%Y%m%d") )
        except Exception as e:
            logger.debug(("error ", e))
        return data


    def get_forecast_vip(self):
        df = self.pro.forecast_vip()
        data = self.stock_basic[['ts_code','name']]
        df = data.merge(df, how='right', on='ts_code')
        return  df
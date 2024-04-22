
#

import tushare as ts
import  pandas as pd

if __name__ == '__main__':
    print("begin")
    pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    # 基础信息
    stock_basic =pro.stock_basic()
    stock_basic2 =stock_basic[['ts_code','name']]
    # 业绩预告
    forecastVip = pro.forecast_vip(period='20231231')
    forecastVip= stock_basic2.merge(forecastVip)
    # 获取每日指标
    dailyBaisc =pro.daily_basic()
    print( dailyBaisc.columns )
    forecastVip =forecastVip.merge( dailyBaisc )
    forecastVip.sort_values( by="ann_date", ascending=False)
    forecastVip.to_excel('/home/xshx/forecast-vip.xlsx')
    print("over")

#
import tushare as ts
import  pandas as pd

if __name__ == '__main__':
    print("begin")
    pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    # 获取基本信息
    stock_basic =pro.stock_basic()
    stock_basic2 =stock_basic[['ts_code','name']]
    # 获取业绩快报
    expressVip = pro.express_vip(period='20231231')
    expressVip= stock_basic2.merge(expressVip)
    # 获取每日指标
    dailyBaisc =pro.daily_basic()
    print( dailyBaisc.columns )
    expressVip =expressVip.merge( dailyBaisc )
    expressVip.sort_values( by="ann_date", ascending=False)
    expressVip.to_excel('/home/xshx/express-vip.xlsx')
    print("over")
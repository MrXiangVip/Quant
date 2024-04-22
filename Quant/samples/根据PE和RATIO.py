
# xshx add



import tushare as ts

import pandas as pd



if __name__ == '__main__':
    pro = ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    stock_basic =pro.stock_basic()
    # 选取出代码和名字
    stock_basic2 = stock_basic[['ts_code', 'name']]
    # 获取每日指标
    basic = pro.daily_basic()
    basic2 = stock_basic2.merge(basic)
    basic2['dv_ratio'] =basic2['dv_ratio'].astype(float)
    basic2['pe']=basic2['pe'].astype(float)
    basic2.sort_values('dv_ratio',ascending=False, inplace=True)
    basic2.to_excel('/home/xshx/pe+ratio.xlsx')
    print("over")
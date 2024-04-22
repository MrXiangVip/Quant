
import tushare as ts
import pandas as pd
if __name__ == '__main__':
    print("begin")
    pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    # 获取基本信息
    df = pro.hk_basic()
    df.to_excel('/home/xshx/港股.xlsx')
    print("over")
#  寻找中国版的美林时钟
from pyecharts.charts import  Line
from pyecharts import  options as opts
import pandas as pd
import tushare as ts


if __name__ == '__main__':
    pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    fund = pro.fund_basic( market="E")
    fund.sort_values(by="found_date", ascending=False, inplace=True)
    fund.to_excel('/home/xshx/fund.xlsx')

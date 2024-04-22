
#  寻找中国版的美林时钟
from pyecharts.charts import  Line
from pyecharts import  options as opts
import pandas as pd
import tushare as ts


if __name__ == '__main__':
    pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    cnm = pro.cn_m( start_m='19870101', end_m='202403')
    cnm.sort_values(by="month", ascending=True, inplace=True)
    line = Line()
    line.set_global_opts(title_opts=opts.TitleOpts(title="折线图示例"), datazoom_opts=opts.DataZoomOpts(range_start=10,range_end=90))
    line.add_xaxis( list(cnm.month) )
    line.add_yaxis( "M0", list(cnm.m0_yoy), is_symbol_show=True)
    line.add_yaxis( "M1", list(cnm.m1_yoy), is_symbol_show=True)
    line.add_yaxis( "M2", list(cnm.m2_yoy), is_symbol_show=True)
    line.render("line_chart.html")



#  寻找中国版的美林时钟
from pyecharts.charts import  Line
from pyecharts import  options as opts
import pandas as pd
import tushare as ts


if __name__ == '__main__':
    pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    lpr = pro.shibor_lpr( start_m='19870101', end_m='20240325')
    lpr.sort_values(by="date", ascending=True, inplace=True)
    line = Line()
    line.set_global_opts(title_opts=opts.TitleOpts(title="折线图示例"), datazoom_opts=opts.DataZoomOpts(range_start=10,range_end=90))
    line.add_xaxis( list(lpr.date) )
    line.add_yaxis( "1Y", list(lpr["1y"]), is_symbol_show=True)
    line.add_yaxis( "5Y", list(lpr["5y"]), is_symbol_show=True)
    line.render("lpr_line_chart.html")


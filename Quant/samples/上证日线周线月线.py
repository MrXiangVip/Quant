from pyecharts.charts import  Line
from pyecharts import  options as opts
import pandas as pd
import tushare as ts


if __name__ == '__main__':
    pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    daily = pro.index_daily( ts_code="000001.SH")
    daily.sort_values(by="trade_date", ascending=True, inplace=True)
    line = Line()
    line.set_global_opts(title_opts=opts.TitleOpts(title="折线图示例"), datazoom_opts=opts.DataZoomOpts(range_start=10,range_end=90))
    line.add_xaxis( list(daily.date) )
    line.add_yaxis( "1Y", list(daily["1y"]), is_symbol_show=True)
    line.add_yaxis( "5Y", list(daily["5y"]), is_symbol_show=True)
    line.render("lpr_line_chart.html")
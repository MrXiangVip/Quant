
import BackTrack as bt
import  pandas as pd
import tushare as ts

# xshx add  first strategy


#  在 如果今天收盘时  上证涨了1个点, 个股最低价跌了1个点则买入.  第二天收盘时卖出. 然后看收益

class MyStrategy(bt.Strategy ):

    def next(self):
        # print( self.lines[0][0], self.lines[1][0])
        series0=self.lines[0][0]
        series1=self.lines[1][0]
        if ((series0.high - series0.open)/series0.open > 0.01) and ((series1.open - series1.low) / series1.open > 0.01) :
            self.buy(series1)

if __name__ == '__main__':

    cerebro = bt.Cerebro()
    pro =ts.pro_api("5bf581802c21c8792cf2cf75d44e989d8fa484595252fe8be3399f88")
    # sz 日线数据
    start_date="20220421"
    end_date="20240301"
    df1 = pro.index_daily(ts_code='000001.SH', start_date=start_date, end_date=end_date)
    df1.sort_values(by='trade_date', ascending=True, inplace=True)
    # gg 日线数据
    df2 =pro.daily(ts_code='600938.SH', start_date=start_date, end_date=end_date)
    df2.sort_values(by='trade_date', ascending=True, inplace=True)
    data1 = bt.LineBuffer(df1)
    data2 = bt.LineBuffer(df2)

    cerebro.adddata( data1)
    cerebro.adddata( data2)

    cerebro.addstrategy( MyStrategy)
    cerebro.run()
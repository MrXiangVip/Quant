



import akshare as ak

class MainWindowModel():
    def __init__(self):
        print("OptionalModel")

    def getSZRealtime(self):
        #数据来源 https://akshare.akfamily.xyz/data/index/index.html#id9
        stock_hk_index_spot_sina_df = ak.stock_hk_index_spot_sina()
        szData=stock_hk_index_spot_sina_df.loc[stock_hk_index_spot_sina_df['名称'] == '上证综合指数']
        return szData

    def getHKRealtime(self):
        # 目标地址: https: // vip.stock.finance.sina.com.cn / mkt /  # zs_hk
        stock_hk_index_spot_sina_df = ak.stock_hk_index_spot_sina()
        hkData=stock_hk_index_spot_sina_df.loc[stock_hk_index_spot_sina_df['名称'] == '恒生指数']
        return hkData

    def getUSRealtime(self):
        # 目标地址: https://stock.finance.sina.com.cn/usstock/quotes/.IXIC.html
        usData = ak.index_us_stock_sina(symbol=".IXIC")
        return usData
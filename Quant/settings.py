import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_console = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_console.setFormatter(formatter)
logger.addHandler(log_console)

news_tick = 1000*60*1
time_tick =1000
optional_columns=['primary','code','name','open','pre_close','price','high','low','买入价格','卖出价格','重要事件']
stock_dic ={ '上证指数':'sh', '深证成指':'sz','沪深300':'hs300', '上证50':'sz50','创业板指':'cyb'} #'中小100':'zxb'
# 'sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb', 'zx300', 'zh500'
ths_member_columns=['序号', '代码', '名称', '现价', '涨跌幅', '涨跌', '涨速', '换手', '量比', '振幅', '成交额', '流通股', '流通市值', '市盈率']
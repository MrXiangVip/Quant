# 准备请求的固定格式代码
import requests
from bs4 import BeautifulSoup
import time
from pandas import DataFrame

# 请求头，用户表名自己的身份
t = time.localtime()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}
# 定义首次要访问的链接(这里访问的是一个js异步请求的链接)
url = "https://xueqiu.com/service/v5/stock/screener/quote/list"
# 设置参数 page:页数 size:每页几条数据（可以自己定） order：排序方式 orderby：根据什么排序 可以有两个 market：交易所地点 type：板块 _：时间戳
params = {
    "page":1,"size":1000,"order":"desc","orderby":"percent","order_by":"symbol","market":"CN","type":"sh_sz","_":1630408116747
}
# 定义一个空的列表存储股票信息
market_dict = { 'HK': 'hk', 'CN': 'sh_sz'}
# market_dict = { 'US': 'us'}
# market_dict = {'CN': 'sh_sz'}

for market in market_dict:
    page = 0
    stock_list = []
    while True:
        page += 1
        params['page'] = page
        params['market'] = market
        params['type'] = market_dict[market]
        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        stock_info = response_json['data']['list']
        if len(stock_info) == 0:
            print('循环完毕，共', len(stock_list), '条数据')
            break
        for stock in stock_info:
            stock_detail = {
                '交易市场':market,
                '股票名称':stock['name'],
                '股票代码':stock['symbol'],
                '当前价':stock['current'],
                '涨跌额':stock['chg'],
                '涨跌幅%':stock['percent'],
                '年初至今':stock['current_year_percent'],
                '成交量':stock['volume'],
                '成交额(元)':stock['amount'],
                '换手率':stock['turnover_rate'],
                '市盈率':stock['pe_ttm'],
                '股息率%':stock['dividend_yield'],
                '市值(元)':stock['market_capital'],
                'ROE':stock['roe_ttm'],
            }
            stock_list.append(stock_detail)
        print(len(stock_list))
        # 保存 dataframe
        df = DataFrame(data=stock_list)
        # 为了让每天写入数据时的文件不重名，也为了避免程序多次运行产生多个一样数据的文件，我们给文件名中加入时间年月日时
        file_name = f'{market}_stock{t.tm_year}年{t.tm_mon}月{t.tm_mday}日{t.tm_hour}时.csv'
        df.to_csv(file_name, encoding='gbk')
    # print(stock_hs)
    print('最终',len(stock_list))

# 写入数据
print('ok')
# https://blog.csdn.net/weixin_43521165/article/details/120046581
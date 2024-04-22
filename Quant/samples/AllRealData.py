
# 导入需要的库
import requests

# 导入headers
headers = {
    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

# 使用for循环遍历所有页面
for i in range(1, 281):
    # 提取页面数据
    param = {
        'cb': 'jQuery112404963477502250466_1683910217762',
        'pn': f'{i}',
        'pz': '20',
        'po': '0',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'wbp2u': '6255436770793316|0|0|0|web',
        'fid': 'f12',
        'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136'
                  ',f115,f152',
        '_': '1683910217985',
    }

    # 导入url
    url = 'http://96.push2.eastmoney.com/api/qt/clist/get'

    # 使用get方法获取数据
    response = requests.get(url, params=param, headers=headers)

    # 打印数据
    print("page",i, " - ",response.text)
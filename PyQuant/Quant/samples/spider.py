import array

import requests
import numpy as np
import sqliteoop
import json


url = 'https://apix.mega.tech/news/pull?'
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
}
response = requests.get(url, headers=headers, timeout=10)
print( response.text)
# 如何用python将  [[],[],[]]  这样一个字符串转成数组
messages = json.loads(response.text)
print( messages)
for message in messages:
    print( message)
    for text in message:
        print(text)
    print(message[1][:2])




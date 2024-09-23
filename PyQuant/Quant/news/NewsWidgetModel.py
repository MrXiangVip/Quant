import json

import requests
from pyexpat.errors import messages
from tushare.stock.histroy_divide import headers

from Quant.samples.spider import response


class NewsWidgetModel():
    def __init__(self):
        print("OptionalModel")
        self.messageList=list()
        self.url = 'https://apix.mega.tech/news/pull?'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        }
    def getCurrentMessage(self):
        print("初始化消息列表")
        response = requests.get(self.url, headers=self.headers, timeout=10)
        print(response.text)
        # 用python将  [[],[],[]]  这样一个字符串转成数组
        messages = json.loads(response.text)
        print(messages)
        for message in messages:
            print(message)
            self.messageList.append( message )
        return self.messageList
    def getNewMessage(self):
        print("更新消息列表")
        self.newMessageList=list()
        response = requests.get(self.url, headers=self.headers, timeout=10)
        print( response.text)
        messages =json.loads(response.text)
        for message in messages:
            # last_index = len(self.messageList) - 1
            print("当前message时间戳 ", message[0], " 列表中最后一条message 时间戳",self.messageList[-1][0])
            if message[0] > self.messageList[-1][0] :
                print("新增消息 ", message)
                self.newMessageList.append( message)
                self.messageList.append( message)
        return self.newMessageList
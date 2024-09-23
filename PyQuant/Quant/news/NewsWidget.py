from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from Quant import settings
from Quant.news.NewsWidgetModel import NewsWidgetModel
from Quant.news.NewsWidgetUI import News_Ui_Form


class NewsWidget(QWidget, News_Ui_Form):
    def __init__(self, root):
        super(NewsWidget, self).__init__(root)
        self.root = root
        self.model = NewsWidgetModel()
        self.setupUI()
        self.initWidget()

    def initWidget(self):
        print("初始化新闻")
        messages =self.model.getCurrentMessage()
        # 发送消息到列表控件
        for message in messages:
            self.listWidget.addItem( str(message[1]) )
        # 滚动到最新消息
        self.listWidget.scrollToBottom()
        self.createTickTimer()
    def createTickTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect( self.updateMessage )
        self.timer.start(settings.message_tick)

    def updateMessage(self):
        print("update message")
        newMessages =self.model.getNewMessage()
        for message in newMessages:
            self.listWidget.addItem( str(message[1]))
        self.listWidget.scrollToBottom()

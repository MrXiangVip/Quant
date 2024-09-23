import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton

class ScrollableMessageInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('可滚动的消息界面')
        self.setGeometry(100, 100, 300, 200)

        # 创建布局和控件
        layout = QVBoxLayout()
        self.listWidget = QListWidget()
        btnSend = QPushButton('发送')

        # 将控件添加到布局中
        layout.addWidget(self.listWidget)
        layout.addWidget(btnSend)

        # 设置窗口布局
        self.setLayout(layout)

        # 连接按钮点击信号
        btnSend.clicked.connect(self.sendMessage)

    def sendMessage(self):
        # 发送消息到列表控件
        self.listWidget.addItem("这是一条新消息")
        # 滚动到最新消息
        self.listWidget.scrollToBottom()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScrollableMessageInterface()
    ex.show()
    sys.exit(app.exec_())

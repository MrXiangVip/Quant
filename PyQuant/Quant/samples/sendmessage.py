import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject


# 定义自定义信号，用于发送字符串消息
class Communicate(QObject):
    send_message = pyqtSignal(str)

class MainWindow(QMainWindow):
    send_message2 = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.comm = Communicate()  # 创建自定义信号的实例

    def initUI(self):
        self.button = QPushButton('Open Second Window', self)
        self.button.clicked.connect(self.open_second_window)

        self.setCentralWidget(self.button)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('MainWindow')

    def open_second_window(self):
        self.second_window = SecondWindow()
        # self.comm.send_message.connect(self.second_window.receive_message)  # 连接信号到第二个窗口的槽
        # self.comm.send_message.emit("Hello from MainWindow!")  # 发送消息
        self.send_message2.connect(self.second_window.receive_message)
        self.send_message2.emit("hell world")
        self.second_window.show()

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel('Waiting for message...', self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setGeometry(600, 300, 300, 200)
        self.setWindowTitle('SecondWindow')

    def receive_message(self, message):
        self.label.setText(message)  # 更新标签以显示接收到的消息

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

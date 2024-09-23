
from system_hotkey import SystemHotkey
from PyQt5.QtWidgets import QApplication ,QWidget ,QDialog
from PyQt5.QtCore import QObject ,pyqtSignal

class HotKey(QWidget ,QObject):
    # 定义一个热键信号
    sigkeyhot = pyqtSignal(str)
    def __init__(self ):
        # 1. 简单的绘制一个窗口
        super().__init__()
        # 2. 设置我们的自定义热键响应函数
        self.sigkeyhot.connect(self.KeypressEvent)
        # 3. 初始化两个热键
        self.hk_start ,self.hk_stop = SystemHotkey() ,SystemHotkey()
        # 4. 绑定快捷键和对应的信号发送函数
        self.hk_start.register(('control' ,'6') ,callback=lambda x :self.sendkeyevent("control+6"))
        self.hk_stop.register(('control', '8'), callback=lambda x: self.sendkeyevent("control+8"))


    # 热键处理函数
    def KeypressEvent(self ,i_str):
        print("按下的按键是%s" % (i_str,))

    # 热键信号发送函数(将外部信号，转化成qt信号)
    def sendkeyevent(self ,i_str):
        self.sigkeyhot.emit(i_str)


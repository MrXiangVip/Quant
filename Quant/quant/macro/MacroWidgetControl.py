
# xshx add 20231212
from PyQt5.QtWidgets import QWidget

from settings import logger

from .MacroWidgetView import *
from .MacroWidgetModel import *

class MacroFormWidget(QWidget, Macro_Ui_Form):
    def __init__(self, root):
        super(MacroFormWidget, self).__init__(root)
        self.root = root
        self.setupUi(self)
        self.initWindow()

    def initWindow(self):
        self.updateWindow()

    def updateWindow(self):
        logger.debug("update window")
        worldMapHtml=MacroWidgetModel().create_world_chart()
        self.browser.load( worldMapHtml )

# 参考
# https://blog.csdn.net/m0_37967652/article/details/128645787#t6
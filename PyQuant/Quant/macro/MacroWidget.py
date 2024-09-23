#
from PyQt5.QtWidgets import QWidget

from Quant.macro.MacroWidgetModel import MacroWidgetModel
from Quant.macro.MacroWidgetUI import Macro_UI_Form


class MacroFormWidget(QWidget, Macro_UI_Form):
    def __init__(self, root):
        super(MacroFormWidget, self).__init__(root)
        self.root = root
        self.model =MacroWidgetModel()
        self.setupUi(self)

        self.initWindow()

    def initWindow(self):
        print("初始化全球")
        self.updateWindow()

    def updateWindow(self):
        worldMapHtml =self.model.createWorldChart()
        self.browser.load( worldMapHtml)
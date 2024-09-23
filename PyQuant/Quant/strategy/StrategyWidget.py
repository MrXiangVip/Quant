from PyQt5.QtWidgets import QWidget

from Quant.strategy.StrategyWidgetUI import Strategy_Ui_Form

class StrategyFormWidget(QWidget, Strategy_Ui_Form):
    def __init__(self, root):
        super(StrategyFormWidget, self).__init__(root)
        self.root = root
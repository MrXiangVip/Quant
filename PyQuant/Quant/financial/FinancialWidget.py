from PyQt5.QtWidgets import QWidget

from Quant.financial.FinancialWidgetUI import FinancialWidgetUI


class FinancialWidget(QWidget, FinancialWidgetUI):
    def __init__(self, root):
        super(FinancialWidget, self).__init__(root)
        self.root = root
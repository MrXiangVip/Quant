from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget

from Quant.optional.OptionalWidgetModel import OptionalWidgetModel
from Quant.optional.OptionalWidgetUI import Optional_Widget_Ui

class OptionalFormWidget(QWidget, Optional_Widget_Ui):

    def __init__(self, root):
        super(OptionalFormWidget, self).__init__(root)
        self.root = root
        self.dataModel =OptionalWidgetModel()
        self.setupUi(self)
        self.initWidget(self.root.defaultMarket)



    def initWidget(self, market="A"):
        print("初始化自选  ", market)
        self.df = self.dataModel.getMarketData( market)
        # 将DataFrame转换为QStandardItemModel
        self.model = self.loadDataToModel(self.df)
        self.tableView.setSortingEnabled(True)
        #  隐藏垂直表头, 将模型设置给QTableView
        self.tableView.verticalHeader().hide()
        self.tableView.setModel(self.model)

    def loadDataToModel(self, dataFrame):
        # 创建一个QStandardItemModel，其行数和列数与DataFrame相匹配
        model = QStandardItemModel(dataFrame.shape[0], dataFrame.shape[1])
        # 设置表头
        model.setHorizontalHeaderLabels(dataFrame.columns.tolist())
        # 将DataFrame中的数据填充到模型中
        for row in range(dataFrame.shape[0]):
            for column in range(dataFrame.shape[1]):
                item = QStandardItem(str(dataFrame.iloc[row, column]))
                model.setItem(row, column, item)

        return model
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化Pandas DataFrame
        self.df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie', 'David'],
            'Age': [24, 19, 30, 22],
            'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
        })

        # 初始化QTableView
        self.table_view = QTableView()
        self.setCentralWidget(self.table_view)

        # 将DataFrame转换为QStandardItemModel
        self.model = self.df_to_model(self.df)
        self.table_view.setSortingEnabled(True)
        # 将模型设置给QTableView
        self.table_view.verticalHeader().hide()
        self.table_view.setModel(self.model)

    def df_to_model(self, df):
        # 创建一个QStandardItemModel，其行数和列数与DataFrame相匹配
        model = QStandardItemModel(df.shape[0], df.shape[1])

        # 设置表头
        model.setHorizontalHeaderLabels(df.columns.tolist())

        # 将DataFrame中的数据填充到模型中
        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, column]))
                model.setItem(row, column, item)

        return model

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


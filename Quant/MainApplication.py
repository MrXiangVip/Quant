import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from MainWindow_Control import MainWindow
import pandas as pd

pd.set_option('display.width', 300)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./icons/stock.svg"))
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
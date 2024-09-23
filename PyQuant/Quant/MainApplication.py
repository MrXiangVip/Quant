


import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import main
from Quant.hotkey import HotKey
from main import *
from hotkey import *
import ctypes

if  __name__=='__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app =QApplication( sys.argv )
    app.setWindowIcon(QIcon("icons/apple-blue.svg"))
    myWin =MainWindow()

    myWin.show()
    sys.exit(app.exec_())
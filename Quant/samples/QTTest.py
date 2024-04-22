

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QToolTip, QDialog, QLabel, QLineEdit, \
    QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(400,320)
        self.status = self.statusBar()
        self.status.showMessage("this is status nofication")
        self.setWindowTitle("example")
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move( (screen.width()-size.width())/2, (screen.height()-size.height())/2)
        self.button = QPushButton("show dialog")
        self.button.clicked.connect( self.buttonOnClick)
        mainFrame = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        mainFrame.setLayout(layout)
        self.setCentralWidget( mainFrame )

    def buttonOnClick(self):
        print("button on click")
        dialog = WinDialog()
        dialog.setWindowTitle("dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec()
        print("show QDialog")


class WinForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif',10))
        self.setToolTip(" a notice")
        self.setGeometry(200, 300,400,400)
        self.setWindowTitle(" bobo")


class WinDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" QLable Ex")
        nameLab = QLabel("name", self)
        nameEd = QLineEdit( self)
        nameLab.setBuddy( nameEd)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget( nameLab, 0,0 )
        mainLayout.addWidget( nameEd, 0,1)

if __name__ == '__main__':
    app = QApplication( sys.argv)
    form = MainWindow()
    form.show()
    # win = WinForm()
    # win.show()
    # dialog = WinDialog()
    # dialog.show()
    sys.exit( app.exec_())
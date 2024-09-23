from PyQt5 import QtWidgets


class News_Ui_Form(object):
    def setupUI(self):
        print("setup ui")
        self.verticalLayout = QtWidgets.QVBoxLayout( )
        self.verticalLayout.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.setLayout(self.verticalLayout)

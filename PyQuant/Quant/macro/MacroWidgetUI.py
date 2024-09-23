
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Macro_UI_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(824, 700)
        self.browser = QWebEngineView()
        self.layout = QtWidgets.QVBoxLayout(Form)
        self.layout.addWidget(self.browser)
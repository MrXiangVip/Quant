from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout


class DetailDialog(QDialog):
    def __init__(self ):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Detail")
        self.resize(600, 800)
        button = QPushButton("close")
        button.clicked.connect(self.close)
        layout = QVBoxLayout()
        layout.addWidget( button)
        self.setLayout( layout)


from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTreeWidgetItem

from industry.IndustryWidgetModel import IndustryWidgetModel
from industry.IndustryWidgetView import Industry_Ui_Form
from settings import ths_member_columns
from settings import logger


class IndustryFormWidget(QWidget, Industry_Ui_Form):
    def __init__(self, root):
        super(IndustryFormWidget, self).__init__(root)
        self.root = root
        self.setupUi(self)
        # self.initWindow()

    def initWindow(self):
        self.updateWindow()

    def updateWindow(self):
        logger.debug("update window")
        # self.data = DataManager().getBrokerReport( date )
        # self.data = DataManager().getBrokerReportData( date )
        self.data = IndustryWidgetModel().get_ths_index()
        self.data = self.data.loc[self.data.exchange == 'A'].reset_index()  # .drop(columns='index')
        self.table_rows = self.data.shape[0]
        table_columns = self.data.shape[1]
        input_table_header = self.data.columns.values.tolist()
        # self.treeWidget.setColumnCount(table_columns)
        # self.treeWidget.setHeaderLabels(input_table_header)
        self.treeWidget.setColumnCount( len(ths_member_columns))
        self.treeWidget.setHeaderLabels( ths_member_columns )
        self.treeWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        # self.treeWidget.setSortingEnabled( True )
        # self.treeWidget.hideColumn(0)
        self.treeWidget.itemExpanded.connect(self.item_expanded)
        self.treeWidget.itemCollapsed.connect(self.item_collapsed)
        # self.treeWidget.setStyle(QStyleFactory.create('windows'))
        for row in range(self.table_rows):
            root = QTreeWidgetItem(self.treeWidget)
            for col in range(table_columns):
                logger.debug('row ', row, 'col ', col, self.data.loc[row][col])
                root.setText(col, str(self.data.loc[row][col]))

            for child_row in range(int(self.data.loc[row][3])):
                child = QTreeWidgetItem(root)
                child.setText(0, str(child_row))

    def item_expanded(self, tree_widget_item):
        logger.debug("item expanded ", tree_widget_item)
        ts_code = tree_widget_item.text(1)
        logger.debug(ts_code)
        # child_data = DataManager().get_ths_member(ts_code)
        child_data = IndustryWidgetModel().get_real_ths_member(ts_code)
        if child_data.empty or child_data.shape[0]==1:
            child_data = IndustryWidgetModel().get_ths_member(ts_code)
        logger.debug("child data \n", child_data)
        child_rows = child_data.shape[0]
        tree_widget_item.takeChildren()
        for child_row in range(child_rows):
            child = QTreeWidgetItem(tree_widget_item)
            for child_col in range(child_data.shape[1]):
                child.setText(child_col, str(child_data.loc[child_row][child_col]))

    def item_collapsed(self, item):
        logger.debug("item collapsed", item)
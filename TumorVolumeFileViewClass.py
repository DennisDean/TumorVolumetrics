# Code for displaying a tumor volume file within a table

# Set up a module-level logger
import logging
logger = logging.getLogger(__name__)

# Import
from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem

# Data
import pandas as pd

# GUI Interface
from TvFileView import Ui_MainWindow

# GUI Class
class TumorVolumeFileWindow(QMainWindow):
    # Initialize Tumor Volume File Window
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup and Draw Window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tumor Volume File")

        # test
        # self.test_table()

        # Store file name
        self.file_window = None
        self.tv_file_name = None
        self.tv_data_obj = None
        self.tv_data_df = None

    def test_table(self):
        table = self.ui.tableWidget_tv_file_table
        table.setRowCount(3)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["A", "B", "C"])
        for r in range(3):
            for c in range(3):
                table.setItem(r, c, QTableWidgetItem(f"{r},{c}"))

    # Create Window
    def open_file_window(self, tv_file_name, tv_data_obj):
        # Open window actions, create if it does not exist
        if self.file_window is None:
            self.file_window = TumorVolumeFileWindow(parent=self)
            self.file_window.show()
            self.file_window.raise_()
            self.file_window.activateWindow()

        # Store information
        self.tv_file_name = tv_file_name
        self.tv_data_obj = tv_data_obj
        self.tv_data_df = tv_data_obj.tmz_data_df

        # Populate Table
        self.load_dataframe_into_table(self.ui.tableWidget_tv_file_table, tv_data_obj.tmz_data_df)

        # Set status
        self.statusBar().showMessage(tv_file_name)
    def load_dataframe_into_table(self, table: QTableWidget, df: pd.DataFrame):
        # Set row and column count
        table.setRowCount(len(df.index))
        table.setColumnCount(len(df.columns))

        # Print
        print(QTableWidget)
        print(df)

        print("DF SHAPE:", df.shape)
        print("HEAD:\n", df.head(10))
        print("TABLE:", table)
        print(table.size())

        # Set headers
        table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())

        # Populate table
        print(len(df.index), len(df.columns))
        for row in range(len(df.index)):
            for col in range(len(df.columns)):
                value = str(df.iat[row, col])
                item = QTableWidgetItem(value)
                table.setItem(row, col, item)

        # Resize columns to fit content
        table.resizeColumnsToContents()

        table.setMinimumHeight(200)
        table.setMinimumWidth(300)




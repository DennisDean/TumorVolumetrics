# Code for displaying a tumor volume file within a table

# Set up a module-level logger
import logging
logger = logging.getLogger(__name__)

# Import
from PySide6.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem,
                              QAbstractItemView, QHeaderView, QMenu, QApplication)
from PySide6.QtCore import Qt

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

        # Force sorting off
        self.ui.tableWidget_tv_file_table.setSortingEnabled(False)

        # Store file name
        self.file_window = None
        self.tv_file_name = None
        self.tv_data_obj = None
        self.tv_data_df = None

    # Configure Table
    def configure_table_viewing(self, table: QTableWidget):
        """Configure table for better viewing experience"""

        # === SIZING ===
        # Resize columns to fit content
        table.resizeColumnsToContents()

        # Resize rows to fit content
        table.resizeRowsToContents()

        # Stretch last column to fill space
        table.horizontalHeader().setStretchLastSection(True)

        # Set column width mode (options: Interactive, Fixed, Stretch, ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Set specific column width
        table.setColumnWidth(0, 150)

        # === SELECTION ===
        # Set selection behavior (SelectRows, SelectColumns, SelectItems)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Set selection mode (SingleSelection, MultiSelection, ExtendedSelection, ContiguousSelection)
        table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        # === EDITING ===
        # Make table read-only
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # === APPEARANCE ===
        # Alternate row colors for readability
        table.setAlternatingRowColors(True)

        # Show/hide grid
        table.setShowGrid(True)

        # Enable sorting
        table.setSortingEnabled(False)

        # Set word wrap
        table.setWordWrap(False)

        # === HEADERS ===
        # Make headers bold/visible
        table.horizontalHeader().setVisible(True)
        table.verticalHeader().setVisible(True)

        # Set header font
        header_font = table.horizontalHeader().font()
        header_font.setBold(True)
        table.horizontalHeader().setFont(header_font)

        # === SCROLLING ===
        # Set scroll mode (ScrollPerPixel or ScrollPerItem)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # === CONTEXT MENU ===
        # Enable right-click context menu
        table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_context_menu)
    def show_context_menu(self, position):
        """Show right-click context menu"""
        menu = QMenu()

        copy_action = menu.addAction("Copy")
        export_action = menu.addAction("Export to CSV")
        menu.addSeparator()
        fit_columns_action = menu.addAction("Fit Columns to Content")

        action = menu.exec_(self.ui.tableWidget_tv_file_table.viewport().mapToGlobal(position))

        if action == copy_action:
            self.copy_selected_cells()
        elif action == export_action:
            self.export_to_csv()
        elif action == fit_columns_action:
            self.ui.tableWidget_tv_file_table.resizeColumnsToContents()
    def copy_selected_cells(self):
        """Copy selected cells to clipboard"""
        selection = self.ui.tableWidget_tv_file_table.selectedIndexes()
        if selection:
            rows = sorted(set(index.row() for index in selection))
            columns = sorted(set(index.column() for index in selection))

            text = ""
            for row in rows:
                row_text = []
                for col in columns:
                    item = self.ui.tableWidget_tv_file_table.item(row, col)
                    row_text.append(item.text() if item else "")
                text += "\t".join(row_text) + "\n"

            QApplication.clipboard().setText(text)
            self.statusBar().showMessage("Copied to clipboard", 2000)

    # === USEFUL GETTER METHODS ===
    def get_table_info(self, table: QTableWidget):
        """Get useful table information"""
        print(f"Rows: {table.rowCount()}")
        print(f"Columns: {table.columnCount()}")
        print(f"Selected rows: {len(set(index.row() for index in table.selectedIndexes()))}")
        print(f"Current row: {table.currentRow()}")
        print(f"Current column: {table.currentColumn()}")

        # Get current cell value
        current_item = table.currentItem()
        if current_item:
            print(f"Current cell value: {current_item.text()}")
    def scroll_to_top(self, table: QTableWidget):
        """Scroll to top of table"""
        table.scrollToTop()
    def scroll_to_bottom(self, table: QTableWidget):
        """Scroll to bottom of table"""
        table.scrollToBottom()
    def scroll_to_item(self, table: QTableWidget, row: int, col: int):
        """Scroll to specific cell"""
        item = table.item(row, col)
        if item:
            table.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtCenter)
    def clear_selection(self, table: QTableWidget):
        """Clear current selection"""
        table.clearSelection()
    def select_row(self, table: QTableWidget, row: int):
        """Select entire row"""
        table.selectRow(row)
    def select_column(self, table: QTableWidget, col: int):
        """Select entire column"""
        table.selectColumn(col)

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

        # Set headers
        table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())

        # Populate table
        for row in range(len(df.index)):
            for col in range(len(df.columns)):
                value = str(df.iat[row, col])
                item = QTableWidgetItem(value)
                table.setItem(row, col, item)

        # === APPLY VIEWING CONFIGURATIONS ===
        table.resizeColumnsToContents()
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.horizontalHeader().setStretchLastSection(True)

        # Optional: Set context menu
        table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_context_menu)
    def populate_data(self, tv_file_name, tv_data_obj):
        """Populate the window with data"""
        # Move forward only if filename is avaialbe

        # Get informtion
        self.tv_file_name = tv_file_name
        self.tv_data_obj = tv_data_obj
        self.tv_data_df = tv_data_obj.tmz_data_df

        # Populate Table
        self.load_dataframe_into_table(
            self.ui.tableWidget_tv_file_table,
            tv_data_obj.tmz_data_df
        )

        # Set status
        self.statusBar().showMessage(tv_file_name)

        # Set headers
        df = tv_data_obj.tmz_data_df
        table = self.ui.tableWidget_tv_file_table
        self.ui.tableWidget_tv_file_table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())

        # Populate table
        for row in range(len(df.index)):
            for col in range(len(df.columns)):
                value = str(df.iat[row, col])
                item = QTableWidgetItem(value)
                table.setItem(row, col, item)

        # Resize columns to fit content
        table.resizeColumnsToContents()






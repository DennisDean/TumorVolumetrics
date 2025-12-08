# Code for displaying a tumor experiment pllots

# Set up a module-level logger
import logging
logger = logging.getLogger(__name__)

# Import
from PySide6.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem,
                              QAbstractItemView, QHeaderView, QMenu, QApplication)
from PySide6.QtCore import Qt

# Data
import pandas as pd

# Tumor volume classes
from TumorVolumeClass import TumorVolumeDataClass

# GUI Interface
from TumorVolumeExperimentView import Ui_MainWindow

# GUI Class
class TumorVolumeExperimentWindow(QMainWindow):
    def __init__(self, tv_data_obj:TumorVolumeDataClass , parent=None):
        super().__init__(parent)

        # Setup and Draw Window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tumor Volume File")

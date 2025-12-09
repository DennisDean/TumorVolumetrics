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

# Utilities
def set_layout_visible(layout, visible: bool):
    """
    Recursively set visibility for all widgets in a layout and its nested layouts.

    Args:
        layout: QLayout object to process
        visible: Boolean indicating whether to show (True) or hide (False) widgets
    """
    for i in range(layout.count()):
        item = layout.itemAt(i)

        # Check if the item is a widget
        widget = item.widget()
        if widget:
            widget.setVisible(visible)

        # Check if the item is a nested layout
        nested_layout = item.layout()
        if nested_layout:
            # Recursively process the nested layout
            set_layout_visible(nested_layout, visible)

# GUI Class
class TumorVolumeExperimentWindow(QMainWindow):
    def __init__(self, tv_data_obj:TumorVolumeDataClass , parent=None):
        super().__init__(parent)

        # Setup and Draw Window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tumor Volume File")

        # Show plotting configuration layout
        self.ui.actionPlot_Configuration.triggered.connect(self.toggle_graph_configuration)
        set_layout_visible(self.ui.verticalLayout_visual_graph_settings, True)

    # Utilities
    def toggle_graph_configuration(self):
        toggled_boolean =  not self.ui.groupBox_plot_configurations.isVisible()
        configuration_layout = self.ui.verticalLayout_visual_graph_settings
        set_layout_visible(configuration_layout, toggled_boolean)



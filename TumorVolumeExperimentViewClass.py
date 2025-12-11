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
        self.ui.actionPlot_Configuration.triggered.connect(self.toggle_graph_configuration_group)
        set_layout_visible(self.ui.verticalLayout_visual_graph_settings, True)

        # Save data object
        self.tv_data_obj = tv_data_obj

        # Get Experiments
        self.experiments = tv_data_obj.unique_experiments
        self.ui.comboBox_configuration_experiments.addItems(self.experiments)

        # Set configurations
        self.initial_configuration = '4'
        self.plot_config_to_index = lambda x: int(x)-1
        self.num_of_plot_option_list = ['1','2','3','4']
        self.plot_graphicview_list = [self.ui.graphicsView_visual_top_left,   self.ui.graphicsView_visual_top_right,
                                      self.ui.graphicsView_visual_bottom_left, self.ui.graphicsView_visual_bottom_right]
        self.graphic_view_plot_dict = {'1':[True, False, False, False], '2':[True, True, False, False],
                                       '3':[True, True, True, False],    '4':[True, True, True, True]}
        self.ui.comboBox_configuration_num_of_plots.addItems(self.num_of_plot_option_list)
        self.ui.comboBox_configuration_num_of_plots.setCurrentIndex(self.plot_config_to_index(self.initial_configuration))
        self.ui.comboBox_configuration_num_of_plots.currentTextChanged.connect(self.toggle_plot_graphics_view)

        # Setup plotting
        self.plot_types: list|None = None
        self.plot_select_comboBox: list|None = None
        self.plotting_functions: list|None = None
        self.initialize_plotting()

    # Initialize
    def initialize_plotting(self):
        # Setup plotting
        self.plot_types = ["Avg_TV_Change_Bar", "TV_Control_Bar", "Objective_Response_Bar",
                           "AUC_with_Control_Bar", "Log2_Fold_Change_w_Error"]
        self.plot_select_comboBox = [self.ui.comboBox_configuration_plot_upper_left,
                                     self.ui.comboBox_configuration_plot_upper_right,
                                     self.ui.comboBox_configuration_plot_lower_left,
                                     self.ui.comboBox_configuration_plot_lower_right]
        self.plotting_functions = ["plot_average_tumor_volume_change_bar",
                                   "plot_tumor_control_ratio_bar",
                                   "proportion_in_objective_response_classification_bar",
                                   "plot_auc_with_controls_bar",
                                   "plot_log2fc_points"]
        for idx, cbox in enumerate(self.plot_select_comboBox):
            cbox.addItems(self.plot_types)
            cbox.setCurrentIndex(idx)

        # Draw plots
        self.draw_figure_group()



    # Utilities
    def toggle_graph_configuration_group(self):
        toggled_boolean =  not self.ui.groupBox_plot_configurations.isVisible()
        configuration_layout = self.ui.verticalLayout_visual_graph_settings
        set_layout_visible(configuration_layout, toggled_boolean)
    def toggle_plot_graphics_view(self, new_text):
        configuration_text = new_text
        graphic_view_boolean_settings = self.graphic_view_plot_dict[configuration_text]
        for (gv, gv_visible) in zip(self.plot_graphicview_list, graphic_view_boolean_settings):
            gv.setVisible(gv_visible)

    # Plot figure
    def draw_figure_group(self):
        # Get plot settings
        experiment_id = self.ui.comboBox_configuration_experiments.currentText()
        num_figures = int(self.ui.comboBox_configuration_num_of_plots.currentText())
        experiment_obj = self.tv_data_obj.tumor_vol_experiment_dict[experiment_id]
        for idx in range(num_figures):
            graph_id = self.plot_select_comboBox[idx]
            experiment_obj.plot_log2fc_points()




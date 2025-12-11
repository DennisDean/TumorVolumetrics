"""
Tumor Volumetrics Viewer

Overview:
A Python-native tumor volume data viewer designed to minimize the effort required to add new methods. The viewer
allows users to:

- load tumor volume data commonly stored in CSV files
- organize the data by experiment, study, and tumor volume curve
- generate common graphs and visualizations
- perform common analyses

Goal:
The goal of the viewer is to provide an open-source framework that supports GUI and interactive analysis. All data,
visualization, and analysis methods are available through TumorVolumeClass.py. Classes and methods in this file enable
command-line execution through the Python interface or interactive notebooks. The classes defined in this file include:

- TumorVolumeDataClass
- TumorVolumeExperimentClass
- TumorVolumeStudyClass
- TumorVolumeTimeSeriesClass

Each class includes data structures, analysis methods, and visualization methods. These methods are easily modified
and extended to support group-specific customizations or additional methods.

The interface provides the ability to save publication-quality figures and to standardize figure formatting during export
and through system-wide settings.

Motivation:
Working with the PDXNet community highlighted the need for tools that serve the full range of professionals working with
tumor volume data. Supporting both GUI and command-line access is intentional because experimentalists, computationalists,
and trainees often have strong preferences for how analyses are performed. The tool is also intended to serve as a starting
point for future analyses by providing a base of existing methods.

Author:
Dennis A. Dean II, PhD
Tumor Science

Completion Date: December 10, 2025

Acknowledgement:
The structure of the Python code benefited from the experience and contributions of the PDXNet community. Discussions during
the process of writing the following publications were highly influential in generating the code written for this application:

    Systematic Establishment of Robustness and Standards in Patient-Derived Xenograft
         Experiments and Analysis Cancer Res (2020) 80 (11): 2286–2297
    PDXNet portal: patient-derived Xenograft model, data, workflow and tool discovery
         NAR Cancer, Volume 4, Issue 2, June 2022
    Assessment of Patient-Derived Xenograft Growth and Antitumor Activity:
         The NCI PDXNet Consensus, Mol Cancer Ther (2024) 23 (7): 924–938

Copyright 2025 Dennis A. Dean II
This file is part of the SleepScienceViewer project.

This source code is licensed under the GNU Affero General Public License v3.0.
See the LICENSE file in the root directory of this source tree or visit
https://www.gnu.org/licenses/agpl-3.0.html for full terms.
"""

# To Do List
# Visualize
# ToDo: Create and launch experiment window
# ToDo: Create and launch study window
# ToDo: Create and launch curve viewer
# ToDo: Create and launch data viewer
# Main Window
# ToDo: Populate Experiment, Study, and Curves combo boxes
# ToDo: Populate tree with file contents
# ToDo: Load Experiment Window
# ToDo: Load study window
# ToDo: Load curves
# Data Format
# ToDo: Open an XML file format
#

# System Support
import os
import sys

from fontTools.ufoLib import deprecatedFontInfoAttributesVersion2

from logging_config import logger
__all__ = ['logger']

# PySide Support
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QTreeWidgetItem, QMessageBox
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtCore import Qt

# Import your Ui_MainWindow from the generated module
from TumorVolumetricsInterface import Ui_MainWindow

# Tumor Volume Classes
from TumorVolumeClass import TumorVolumeDataClass
from TumorVolumeFileViewClass import TumorVolumeFileWindow
from TumorVolumeExperimentViewClass import TumorVolumeExperimentWindow

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

# Application
class MainApp(QMainWindow):
    # Initialize
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Tumor Volumetrics")

        # Position window at upper left corner
        self.move(0, 0)
        self.setMaximumWidth(500)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        # Get the screen where the cursor currently is
        cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(cursor_pos)

        if screen:
            geo = screen.availableGeometry()
            # Position window at the top-left of that screen
            self.move(geo.topLeft())

        # Turn off show and navigate groups
        set_layout_visible(self.ui.verticalLayout_navigate, False)
        set_layout_visible(self.ui.verticalLayout_show, False)
        set_layout_visible(self.ui.horizontalLayout_spacer, False)

        # Resize window
        self.adjustSize()

        # Define variables
        self.tumor_volume_file_path:str|None = None
        self.tumor_volume_data_obj:TumorVolumeDataClass|None = None

        self.unique_contributors:list[str]|None = None
        self.unique_experiments:list[str]|None = None
        self.unique_studies:list[str]|None = None
        self.unique_arms:list[str]|None = None
        self.unique_time_series:list[str]|None = None

        # Load Buttons
        self.ui.pushButton_load_select_file.clicked.connect(self.pushbutton_load_csv_file)
        self.ui.pushButton_load_show_file.clicked.connect(self.pushbutton_show_csv_file)
        self.ui.pushButton_load_saveas.clicked.connect(self.save_xml_with_dialog)

        # Show Buttons
        self.ui.pushButton_show_contributor.clicked.connect(self.pushbutton_show_csv_file)
        self.ui.pushButton_show_disease.clicked.connect(self.pushbutton_show_csv_file)
        self.ui.pushButton_show_experiment.clicked.connect(self.pushbutton_show_experiment_viewer)
        self.ui.pushButton_show_study.clicked.connect(self.pushbutton_show_csv_file)
        self.ui.pushButton_show_arm.clicked.connect(self.pushbutton_show_csv_file)
        self.ui.pushButton_show_curves.clicked.connect(self.pushbutton_show_csv_file)

        # Store file Information
        self.tv_file_path:str|None = None
        self.tv_fn:str|None = None
        self.tumor_volume_file_window:TumorVolumeFileWindow|None = None
        self.tumor_volume_experiment_window:TumorVolumeExperimentViewClass|None = None

        # Button

    # Major Commands
    def pushbutton_load_csv_file(self):
        # Respond to user file request
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a Tumor Volume File",
            "",  # starting directory
            "All Files (*);;CSV Files (*.csv)"  # file filters
        )

        # Process file selection outputs
        if file_path:
            # Set status bar
            fn = os.path.basename(file_path)
            self.statusBar().showMessage(fn)
            logger.info(f"Selected file: {file_path}")

            # Store information
            self.tv_file_path = file_path
            self.tv_fn = fn
        else:
            logger.info(f"File selection canceled by user.")
            return

        # Set file name to gobal varaibles
        self.tumor_volume_file_path = file_path

        # Turn off show and navigate groups
        set_layout_visible(self.ui.verticalLayout_navigate, True)
        set_layout_visible(self.ui.verticalLayout_show, True)
        set_layout_visible(self.ui.horizontalLayout_spacer, True)
        self.adjustSize()

        # Load File
        self.tumor_volume_data_obj = TumorVolumeDataClass()
        self.tumor_volume_data_obj.load_tmz_csv(file_path)

        # Get unique entries from Tumor Volume Data Class
        self.unique_contributors = self.tumor_volume_data_obj.unique_contributors
        self.unique_diseases = self.tumor_volume_data_obj.unique_disease_types
        self.unique_experiments = self.tumor_volume_data_obj.unique_experiments
        self.unique_studies = self.tumor_volume_data_obj.unique_studies
        self.unique_arms = self.tumor_volume_data_obj.unique_arms
        self.unique_time_series = self.tumor_volume_data_obj.unique_pdx_ids

        # Clear Boxes
        c_boxes = [ self.ui.comboBox_show_contributor, self.ui.comboBox_show_disease,
                    self.ui.comboBox_show_experiment, self.ui.comboBox_show_study,
                    self.ui.comboBox_show_arms, self.ui.comboBox_show_curves]
        for cbox in c_boxes:
            cbox.clear()

        # Populate comboboxes
        self.ui.comboBox_show_contributor.clear()
        self.ui.comboBox_show_contributor.addItems(self.unique_contributors)
        self.ui.comboBox_show_disease.addItems(self.unique_diseases)
        self.ui.comboBox_show_experiment.addItems(self.unique_experiments)
        self.ui.comboBox_show_study.addItems(self.unique_studies)
        self.ui.comboBox_show_arms.addItems(self.unique_arms)
        self.ui.comboBox_show_curves.addItems(self.unique_time_series)

        # Set Tree
        self.populate_interface_tree()
    def save_xml_with_dialog(self, parent=None):
        """
        Opens a file-save dialog and writes XML content to the selected file.

        Parameters
        ----------
        parent : QWidget or None
            Parent widget for the dialog.
        xml_text : str
            The XML text to write to the file.
        """

        # Open save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save XML File",
            dir="",
            filter="XML Files (*.xml)"
        )

        # If user canceled
        if not file_path:
            return None

        # Ensure filename ends with .xml
        if not file_path.lower().endswith(".xml"):
            file_path += ".xml"


        df = self.tumor_volume_data_obj.tmz_data_df
        self.tumor_volume_data_obj.dataframe_to_xml(df, file_path)

        try:
            self.tumor_volume_data_obj.dataframe_to_xml(self.tumor_volume_data_obj.tmz_data_df.copy(), file_path)

        except Exception as e:
            QMessageBox.critical(parent, "Error", f"Could not save file:\n{e}")
            return None
    def populate_interface_tree(self):
        # Get ui interface tree
        ui_tree = self.ui.treeWidget_navigate_file

        # Set tree header level
        ui_tree.setHeaderHidden(True)

        # Populate tree widget to enable interactive views
        ui_tree = self.ui.treeWidget_navigate_file
        ui_tree.clear()
        ui_tree.addTopLevelItem(QTreeWidgetItem(['Contibutors']))
        ui_tree.addTopLevelItem(QTreeWidgetItem(['Disease']))
        ui_tree.addTopLevelItem(QTreeWidgetItem(['Experiments']))

    # Data viewers
    def pushbutton_show_csv_file(self):
        logger.info(f'Displaying the selected file: {self.tumor_volume_file_path}')

        if self.tumor_volume_file_window is None:
            self.tumor_volume_file_window= TumorVolumeFileWindow(parent=self)

        # Let the window populate itself
        self.tumor_volume_file_window.populate_data(self.tv_fn, self.tumor_volume_data_obj)
        self.tumor_volume_file_window.show()
        self.tumor_volume_file_window.raise_()
        self.tumor_volume_file_window.activateWindow()
    def pushbutton_show_experiment_viewer(self):
        logger.info(f'Displaying tumor volume experiment viewer: {self.tumor_volume_file_path}')

        if self.tumor_volume_experiment_window is None:
            self.tumor_volume_experiment_window = TumorVolumeExperimentWindow(self.tumor_volume_data_obj)

        # Let the window populate itself
        self.tumor_volume_experiment_window.show()
        self.tumor_volume_experiment_window.raise_()
        self.tumor_volume_experiment_window.activateWindow()

# Start Application
def main():
    # Starting Application
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()

    # Initialize logger
    logger.info('Starting TumorVolumetrics.')
if __name__ == "__main__":
    main()  # -*- coding: utf-8 -*-
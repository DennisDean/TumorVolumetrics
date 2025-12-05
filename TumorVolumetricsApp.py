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
# ToDo: Create and launch main window
# ToDo: Create and launch experiment window
# ToDo: Create and launch study window
# ToDo: Create and launch curve viewer
# ToDo: Create and launch data viewer
# Main Window
# ToDO: Select and load file buttong
# ToDo: Show and display file
# ToDo: Save csv as an XML file
# ToDo: Populate Experiment, Study, and Curves combo boxes
# ToDo: Populate tree with file contents
# ToDo: Load Experiment Window
# ToDo: Load study window
# ToDo: Load curves
# Data Format
# ToDo: Save as XML file format
#

# PySide Support
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtCore import Qt

# Import your Ui_MainWindow from the generated module
from TumorVolumetricsInterface import Ui_MainWindow

# Application
class MainApp(QMainWindow):
    # Initialize
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setWindowTitle("Tumor Volumetrics")
        self.ui.setupUi(self)

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


# Start Application
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()
if __name__ == "__main__":
    main()  # -*- coding: utf-8 -*-
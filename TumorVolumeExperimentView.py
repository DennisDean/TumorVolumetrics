# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TumorVolumeExperimentView.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(925, 619)
        self.actionPlot_Configuration = QAction(MainWindow)
        self.actionPlot_Configuration.setObjectName(u"actionPlot_Configuration")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_figure_grid = QHBoxLayout()
        self.horizontalLayout_figure_grid.setObjectName(u"horizontalLayout_figure_grid")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_visual_top_graphview = QHBoxLayout()
        self.horizontalLayout_visual_top_graphview.setObjectName(u"horizontalLayout_visual_top_graphview")
        self.graphicsView_visual_top_left = QGraphicsView(self.centralwidget)
        self.graphicsView_visual_top_left.setObjectName(u"graphicsView_visual_top_left")

        self.horizontalLayout_visual_top_graphview.addWidget(self.graphicsView_visual_top_left)

        self.graphicsView_visual_top_right = QGraphicsView(self.centralwidget)
        self.graphicsView_visual_top_right.setObjectName(u"graphicsView_visual_top_right")

        self.horizontalLayout_visual_top_graphview.addWidget(self.graphicsView_visual_top_right)


        self.verticalLayout_4.addLayout(self.horizontalLayout_visual_top_graphview)

        self.horizontalLayout_visual_bottom_graphview = QHBoxLayout()
        self.horizontalLayout_visual_bottom_graphview.setObjectName(u"horizontalLayout_visual_bottom_graphview")
        self.graphicsView_visual_bottom_left = QGraphicsView(self.centralwidget)
        self.graphicsView_visual_bottom_left.setObjectName(u"graphicsView_visual_bottom_left")

        self.horizontalLayout_visual_bottom_graphview.addWidget(self.graphicsView_visual_bottom_left)

        self.graphicsView_visual_bottom_right = QGraphicsView(self.centralwidget)
        self.graphicsView_visual_bottom_right.setObjectName(u"graphicsView_visual_bottom_right")

        self.horizontalLayout_visual_bottom_graphview.addWidget(self.graphicsView_visual_bottom_right)


        self.verticalLayout_4.addLayout(self.horizontalLayout_visual_bottom_graphview)


        self.horizontalLayout_figure_grid.addLayout(self.verticalLayout_4)

        self.verticalLayout_visual_graph_settings = QVBoxLayout()
        self.verticalLayout_visual_graph_settings.setObjectName(u"verticalLayout_visual_graph_settings")
        self.groupBox_plot_style_sheet = QGroupBox(self.centralwidget)
        self.groupBox_plot_style_sheet.setObjectName(u"groupBox_plot_style_sheet")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_plot_style_sheet.sizePolicy().hasHeightForWidth())
        self.groupBox_plot_style_sheet.setSizePolicy(sizePolicy)
        self.groupBox_plot_style_sheet.setCheckable(True)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_plot_style_sheet)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.groupBox_plot_style_sheet)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(0, 25))
        self.label.setMaximumSize(QSize(16777215, 25))
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label, 0, Qt.AlignHCenter)

        self.comboBox_plot_style_module = QComboBox(self.groupBox_plot_style_sheet)
        self.comboBox_plot_style_module.setObjectName(u"comboBox_plot_style_module")
        sizePolicy.setHeightForWidth(self.comboBox_plot_style_module.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_style_module.setSizePolicy(sizePolicy)
        self.comboBox_plot_style_module.setMinimumSize(QSize(170, 0))
        self.comboBox_plot_style_module.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_5.addWidget(self.comboBox_plot_style_module)

        self.verticalLayout_plot_scienceplot_options = QVBoxLayout()
        self.verticalLayout_plot_scienceplot_options.setObjectName(u"verticalLayout_plot_scienceplot_options")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(self.groupBox_plot_style_sheet)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(50, 0))
        self.label_3.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_7.addWidget(self.label_3)

        self.comboBox_plot_scienceplot_journal = QComboBox(self.groupBox_plot_style_sheet)
        self.comboBox_plot_scienceplot_journal.setObjectName(u"comboBox_plot_scienceplot_journal")

        self.horizontalLayout_7.addWidget(self.comboBox_plot_scienceplot_journal)


        self.verticalLayout_plot_scienceplot_options.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_12 = QLabel(self.groupBox_plot_style_sheet)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(50, 0))
        self.label_12.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_9.addWidget(self.label_12)

        self.comboBox_plot_scienceplot_color = QComboBox(self.groupBox_plot_style_sheet)
        self.comboBox_plot_scienceplot_color.setObjectName(u"comboBox_plot_scienceplot_color")

        self.horizontalLayout_9.addWidget(self.comboBox_plot_scienceplot_color)


        self.verticalLayout_plot_scienceplot_options.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_4 = QLabel(self.groupBox_plot_style_sheet)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(50, 0))
        self.label_4.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_8.addWidget(self.label_4)

        self.comboBox_plot_scienceplot_grid = QComboBox(self.groupBox_plot_style_sheet)
        self.comboBox_plot_scienceplot_grid.setObjectName(u"comboBox_plot_scienceplot_grid")
        sizePolicy.setHeightForWidth(self.comboBox_plot_scienceplot_grid.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_scienceplot_grid.setSizePolicy(sizePolicy)
        self.comboBox_plot_scienceplot_grid.setMinimumSize(QSize(110, 0))
        self.comboBox_plot_scienceplot_grid.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_8.addWidget(self.comboBox_plot_scienceplot_grid)


        self.verticalLayout_plot_scienceplot_options.addLayout(self.horizontalLayout_8)


        self.verticalLayout_5.addLayout(self.verticalLayout_plot_scienceplot_options)

        self.verticalLayout_matplotlib_options = QVBoxLayout()
        self.verticalLayout_matplotlib_options.setObjectName(u"verticalLayout_matplotlib_options")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_13 = QLabel(self.groupBox_plot_style_sheet)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(50, 0))
        self.label_13.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.label_13)

        self.comboBox_plot_matplotlib_style = QComboBox(self.groupBox_plot_style_sheet)
        self.comboBox_plot_matplotlib_style.setObjectName(u"comboBox_plot_matplotlib_style")

        self.horizontalLayout_6.addWidget(self.comboBox_plot_matplotlib_style)


        self.verticalLayout_matplotlib_options.addLayout(self.horizontalLayout_6)


        self.verticalLayout_5.addLayout(self.verticalLayout_matplotlib_options)


        self.verticalLayout_visual_graph_settings.addWidget(self.groupBox_plot_style_sheet)

        self.groupBox_plot_configurations = QGroupBox(self.centralwidget)
        self.groupBox_plot_configurations.setObjectName(u"groupBox_plot_configurations")
        sizePolicy.setHeightForWidth(self.groupBox_plot_configurations.sizePolicy().hasHeightForWidth())
        self.groupBox_plot_configurations.setSizePolicy(sizePolicy)
        self.groupBox_plot_configurations.setCheckable(True)
        self.groupBox_plot_configurations.setChecked(True)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_plot_configurations)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.groupBox_plot_configurations)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(90, 0))
        self.label_2.setMaximumSize(QSize(90, 16777215))

        self.verticalLayout_3.addWidget(self.label_2, 0, Qt.AlignHCenter)

        self.comboBox_configuration_experiments = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_experiments.setObjectName(u"comboBox_configuration_experiments")
        self.comboBox_configuration_experiments.setMinimumSize(QSize(170, 0))
        self.comboBox_configuration_experiments.setMaximumSize(QSize(170, 16777215))

        self.verticalLayout_3.addWidget(self.comboBox_configuration_experiments, 0, Qt.AlignHCenter)

        self.label_11 = QLabel(self.groupBox_plot_configurations)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 10))
        self.label_11.setMaximumSize(QSize(16777215, 10))

        self.verticalLayout_3.addWidget(self.label_11)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.label_5 = QLabel(self.groupBox_plot_configurations)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(75, 25))
        self.label_5.setMaximumSize(QSize(75, 25))

        self.horizontalLayout.addWidget(self.label_5, 0, Qt.AlignTop)

        self.comboBox_configuration_num_of_plots = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_num_of_plots.setObjectName(u"comboBox_configuration_num_of_plots")
        self.comboBox_configuration_num_of_plots.setMinimumSize(QSize(0, 25))
        self.comboBox_configuration_num_of_plots.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.comboBox_configuration_num_of_plots, 0, Qt.AlignTop)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.groupBox_plot_configurations)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(15, 25))
        self.label_6.setMaximumSize(QSize(15, 25))

        self.horizontalLayout_2.addWidget(self.label_6)

        self.comboBox_configuration_plot_upper_left = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_plot_upper_left.setObjectName(u"comboBox_configuration_plot_upper_left")
        self.comboBox_configuration_plot_upper_left.setMinimumSize(QSize(0, 25))
        self.comboBox_configuration_plot_upper_left.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_2.addWidget(self.comboBox_configuration_plot_upper_left)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(self.groupBox_plot_configurations)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)
        self.label_7.setMinimumSize(QSize(15, 25))
        self.label_7.setMaximumSize(QSize(15, 25))

        self.horizontalLayout_3.addWidget(self.label_7)

        self.comboBox_configuration_plot_upper_right = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_plot_upper_right.setObjectName(u"comboBox_configuration_plot_upper_right")

        self.horizontalLayout_3.addWidget(self.comboBox_configuration_plot_upper_right)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.groupBox_plot_configurations)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setMinimumSize(QSize(15, 25))
        self.label_8.setMaximumSize(QSize(15, 25))

        self.horizontalLayout_4.addWidget(self.label_8)

        self.comboBox_configuration_plot_lower_left = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_plot_lower_left.setObjectName(u"comboBox_configuration_plot_lower_left")

        self.horizontalLayout_4.addWidget(self.comboBox_configuration_plot_lower_left)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.groupBox_plot_configurations)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
        self.label_9.setMinimumSize(QSize(15, 25))
        self.label_9.setMaximumSize(QSize(15, 25))

        self.horizontalLayout_5.addWidget(self.label_9)

        self.comboBox_configuration_plot_lower_right = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_plot_lower_right.setObjectName(u"comboBox_configuration_plot_lower_right")

        self.horizontalLayout_5.addWidget(self.comboBox_configuration_plot_lower_right)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.verticalLayout_visual_graph_settings.addWidget(self.groupBox_plot_configurations)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_visual_graph_settings.addWidget(self.label_10)


        self.horizontalLayout_figure_grid.addLayout(self.verticalLayout_visual_graph_settings)


        self.verticalLayout_2.addLayout(self.horizontalLayout_figure_grid)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 925, 23))
        self.menuShow = QMenu(self.menubar)
        self.menuShow.setObjectName(u"menuShow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuShow.menuAction())
        self.menuShow.addAction(self.actionPlot_Configuration)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionPlot_Configuration.setText(QCoreApplication.translate("MainWindow", u"Plot Configuration", None))
        self.groupBox_plot_style_sheet.setTitle(QCoreApplication.translate("MainWindow", u"Plot Style Sheet", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Module", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Journal", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Grid", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Style", None))
        self.groupBox_plot_configurations.setTitle(QCoreApplication.translate("MainWindow", u"Plot Configuration", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Experiment", None))
        self.label_11.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"# of Plots:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"1. ", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"2.", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"3.", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"4.", None))
        self.label_10.setText("")
        self.menuShow.setTitle(QCoreApplication.translate("MainWindow", u"Show", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TumorVolumeStudyView.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGraphicsView,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(970, 1232)
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
        self.verticalLayout_plots = QVBoxLayout()
        self.verticalLayout_plots.setObjectName(u"verticalLayout_plots")
        self.horizontalLayout_visual_top_graphview = QHBoxLayout()
        self.horizontalLayout_visual_top_graphview.setObjectName(u"horizontalLayout_visual_top_graphview")
        self.graphicsView_visual_top_left = QGraphicsView(self.centralwidget)
        self.graphicsView_visual_top_left.setObjectName(u"graphicsView_visual_top_left")

        self.horizontalLayout_visual_top_graphview.addWidget(self.graphicsView_visual_top_left)

        self.graphicsView_visual_top_right = QGraphicsView(self.centralwidget)
        self.graphicsView_visual_top_right.setObjectName(u"graphicsView_visual_top_right")

        self.horizontalLayout_visual_top_graphview.addWidget(self.graphicsView_visual_top_right)


        self.verticalLayout_plots.addLayout(self.horizontalLayout_visual_top_graphview)

        self.horizontalLayout_visual_bottom_graphview = QHBoxLayout()
        self.horizontalLayout_visual_bottom_graphview.setObjectName(u"horizontalLayout_visual_bottom_graphview")
        self.graphicsView_visual_bottom_left = QGraphicsView(self.centralwidget)
        self.graphicsView_visual_bottom_left.setObjectName(u"graphicsView_visual_bottom_left")

        self.horizontalLayout_visual_bottom_graphview.addWidget(self.graphicsView_visual_bottom_left)

        self.graphicsView_visual_bottom_right = QGraphicsView(self.centralwidget)
        self.graphicsView_visual_bottom_right.setObjectName(u"graphicsView_visual_bottom_right")

        self.horizontalLayout_visual_bottom_graphview.addWidget(self.graphicsView_visual_bottom_right)


        self.verticalLayout_plots.addLayout(self.horizontalLayout_visual_bottom_graphview)


        self.horizontalLayout_figure_grid.addLayout(self.verticalLayout_plots)

        self.verticalLayout_visual_graph_settings = QVBoxLayout()
        self.verticalLayout_visual_graph_settings.setObjectName(u"verticalLayout_visual_graph_settings")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(250, 0))
        self.scrollArea.setMaximumSize(QSize(250, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 231, 2067))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy1)
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox_plot_configurations = QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_plot_configurations.setObjectName(u"groupBox_plot_configurations")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_plot_configurations.sizePolicy().hasHeightForWidth())
        self.groupBox_plot_configurations.setSizePolicy(sizePolicy2)
        self.groupBox_plot_configurations.setCheckable(True)
        self.groupBox_plot_configurations.setChecked(True)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_plot_configurations)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_plot_configuration = QVBoxLayout()
        self.verticalLayout_plot_configuration.setObjectName(u"verticalLayout_plot_configuration")
        self.label_2 = QLabel(self.groupBox_plot_configurations)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(90, 0))
        self.label_2.setMaximumSize(QSize(90, 16777215))

        self.verticalLayout_plot_configuration.addWidget(self.label_2)

        self.comboBox_configuration_study = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_study.setObjectName(u"comboBox_configuration_study")

        self.verticalLayout_plot_configuration.addWidget(self.comboBox_configuration_study)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.label_5 = QLabel(self.groupBox_plot_configurations)
        self.label_5.setObjectName(u"label_5")
        sizePolicy2.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy2)
        self.label_5.setMinimumSize(QSize(75, 25))
        self.label_5.setMaximumSize(QSize(75, 25))

        self.horizontalLayout.addWidget(self.label_5, 0, Qt.AlignTop)

        self.comboBox_configuration_num_of_plots = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_num_of_plots.setObjectName(u"comboBox_configuration_num_of_plots")
        self.comboBox_configuration_num_of_plots.setMinimumSize(QSize(0, 25))
        self.comboBox_configuration_num_of_plots.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.comboBox_configuration_num_of_plots, 0, Qt.AlignTop)


        self.verticalLayout_plot_configuration.addLayout(self.horizontalLayout)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_19 = QLabel(self.groupBox_plot_configurations)
        self.label_19.setObjectName(u"label_19")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy3)
        self.label_19.setMinimumSize(QSize(15, 25))
        self.label_19.setMaximumSize(QSize(15, 25))

        self.horizontalLayout_15.addWidget(self.label_19)

        self.comboBox_configuration_plot_upper_left_2 = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_plot_upper_left_2.setObjectName(u"comboBox_configuration_plot_upper_left_2")
        self.comboBox_configuration_plot_upper_left_2.setMinimumSize(QSize(0, 25))
        self.comboBox_configuration_plot_upper_left_2.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_15.addWidget(self.comboBox_configuration_plot_upper_left_2)


        self.verticalLayout_plot_configuration.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_20 = QLabel(self.groupBox_plot_configurations)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(15, 25))
        self.label_20.setMaximumSize(QSize(15, 25))

        self.horizontalLayout_16.addWidget(self.label_20)

        self.comboBox_configuration_plot_upper_right_2 = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_plot_upper_right_2.setObjectName(u"comboBox_configuration_plot_upper_right_2")
        self.comboBox_configuration_plot_upper_right_2.setMinimumSize(QSize(0, 25))
        self.comboBox_configuration_plot_upper_right_2.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_16.addWidget(self.comboBox_configuration_plot_upper_right_2)


        self.verticalLayout_plot_configuration.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_21 = QLabel(self.groupBox_plot_configurations)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMaximumSize(QSize(15, 25))

        self.horizontalLayout_17.addWidget(self.label_21)

        self.comboBox_configuration_plot_lower_left_2 = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_plot_lower_left_2.setObjectName(u"comboBox_configuration_plot_lower_left_2")
        self.comboBox_configuration_plot_lower_left_2.setMinimumSize(QSize(0, 25))
        self.comboBox_configuration_plot_lower_left_2.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_17.addWidget(self.comboBox_configuration_plot_lower_left_2)


        self.verticalLayout_plot_configuration.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_18 = QLabel(self.groupBox_plot_configurations)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(15, 25))
        self.label_18.setMaximumSize(QSize(15, 25))

        self.horizontalLayout_14.addWidget(self.label_18)

        self.comboBox_configuration_plot_lower_right_2 = QComboBox(self.groupBox_plot_configurations)
        self.comboBox_configuration_plot_lower_right_2.setObjectName(u"comboBox_configuration_plot_lower_right_2")
        self.comboBox_configuration_plot_lower_right_2.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_14.addWidget(self.comboBox_configuration_plot_lower_right_2)


        self.verticalLayout_plot_configuration.addLayout(self.horizontalLayout_14)


        self.verticalLayout_3.addLayout(self.verticalLayout_plot_configuration)


        self.verticalLayout_7.addWidget(self.groupBox_plot_configurations, 0, Qt.AlignTop)

        self.groupBox_plot_style_sheet = QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_plot_style_sheet.setObjectName(u"groupBox_plot_style_sheet")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.groupBox_plot_style_sheet.sizePolicy().hasHeightForWidth())
        self.groupBox_plot_style_sheet.setSizePolicy(sizePolicy4)
        self.groupBox_plot_style_sheet.setCheckable(True)
        self.groupBox_plot_style_sheet.setChecked(False)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_plot_style_sheet)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_plot_style_group = QVBoxLayout()
        self.verticalLayout_plot_style_group.setObjectName(u"verticalLayout_plot_style_group")
        self.verticalLayout_plot_style_group.setSizeConstraint(QLayout.SetMinimumSize)
        self.label = QLabel(self.groupBox_plot_style_sheet)
        self.label.setObjectName(u"label")
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)
        self.label.setMinimumSize(QSize(0, 25))
        self.label.setMaximumSize(QSize(16777215, 25))
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_plot_style_group.addWidget(self.label)

        self.comboBox_plot_style_module = QComboBox(self.groupBox_plot_style_sheet)
        self.comboBox_plot_style_module.setObjectName(u"comboBox_plot_style_module")
        sizePolicy2.setHeightForWidth(self.comboBox_plot_style_module.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_style_module.setSizePolicy(sizePolicy2)
        self.comboBox_plot_style_module.setMinimumSize(QSize(170, 25))
        self.comboBox_plot_style_module.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_plot_style_group.addWidget(self.comboBox_plot_style_module)

        self.verticalLayout_matplotlib_options = QVBoxLayout()
        self.verticalLayout_matplotlib_options.setObjectName(u"verticalLayout_matplotlib_options")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_13 = QLabel(self.groupBox_plot_style_sheet)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)
        self.label_13.setMinimumSize(QSize(50, 0))
        self.label_13.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.label_13)

        self.comboBox_plot_matplotlib_style = QComboBox(self.groupBox_plot_style_sheet)
        self.comboBox_plot_matplotlib_style.setObjectName(u"comboBox_plot_matplotlib_style")
        self.comboBox_plot_matplotlib_style.setMinimumSize(QSize(110, 25))
        self.comboBox_plot_matplotlib_style.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_6.addWidget(self.comboBox_plot_matplotlib_style)


        self.verticalLayout_matplotlib_options.addLayout(self.horizontalLayout_6)


        self.verticalLayout_plot_style_group.addLayout(self.verticalLayout_matplotlib_options)

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
        self.comboBox_plot_scienceplot_journal.setMinimumSize(QSize(110, 25))
        self.comboBox_plot_scienceplot_journal.setMaximumSize(QSize(16777215, 25))

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
        sizePolicy2.setHeightForWidth(self.comboBox_plot_scienceplot_color.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_scienceplot_color.setSizePolicy(sizePolicy2)
        self.comboBox_plot_scienceplot_color.setMinimumSize(QSize(110, 25))
        self.comboBox_plot_scienceplot_color.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_9.addWidget(self.comboBox_plot_scienceplot_color)


        self.verticalLayout_plot_scienceplot_options.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_4 = QLabel(self.groupBox_plot_style_sheet)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        self.label_4.setMinimumSize(QSize(50, 0))
        self.label_4.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_8.addWidget(self.label_4)

        self.comboBox_plot_scienceplot_grid = QComboBox(self.groupBox_plot_style_sheet)
        self.comboBox_plot_scienceplot_grid.setObjectName(u"comboBox_plot_scienceplot_grid")
        sizePolicy2.setHeightForWidth(self.comboBox_plot_scienceplot_grid.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_scienceplot_grid.setSizePolicy(sizePolicy2)
        self.comboBox_plot_scienceplot_grid.setMinimumSize(QSize(110, 25))
        self.comboBox_plot_scienceplot_grid.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_8.addWidget(self.comboBox_plot_scienceplot_grid)


        self.verticalLayout_plot_scienceplot_options.addLayout(self.horizontalLayout_8)


        self.verticalLayout_plot_style_group.addLayout(self.verticalLayout_plot_scienceplot_options)

        self.pushButton_plot_uodate_style = QPushButton(self.groupBox_plot_style_sheet)
        self.pushButton_plot_uodate_style.setObjectName(u"pushButton_plot_uodate_style")

        self.verticalLayout_plot_style_group.addWidget(self.pushButton_plot_uodate_style)


        self.verticalLayout_5.addLayout(self.verticalLayout_plot_style_group)


        self.verticalLayout_7.addWidget(self.groupBox_plot_style_sheet, 0, Qt.AlignTop)

        self.line = QFrame(self.scrollAreaWidgetContents_3)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.groupBox_auc_by_arm = QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_auc_by_arm.setObjectName(u"groupBox_auc_by_arm")
        self.groupBox_auc_by_arm.setCheckable(True)
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_auc_by_arm)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_38 = QLabel(self.groupBox_auc_by_arm)
        self.label_38.setObjectName(u"label_38")

        self.verticalLayout_10.addWidget(self.label_38)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_35 = QLabel(self.groupBox_auc_by_arm)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMinimumSize(QSize(70, 0))
        self.label_35.setMaximumSize(QSize(70, 16777215))
        self.label_35.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_27.addWidget(self.label_35)

        self.comboBox_auc_normalize = QComboBox(self.groupBox_auc_by_arm)
        self.comboBox_auc_normalize.setObjectName(u"comboBox_auc_normalize")

        self.horizontalLayout_27.addWidget(self.comboBox_auc_normalize)


        self.verticalLayout_10.addLayout(self.horizontalLayout_27)

        self.label_37 = QLabel(self.groupBox_auc_by_arm)
        self.label_37.setObjectName(u"label_37")

        self.verticalLayout_10.addWidget(self.label_37)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_34 = QLabel(self.groupBox_auc_by_arm)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(70, 0))
        self.label_34.setMaximumSize(QSize(70, 16777215))
        self.label_34.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_22.addWidget(self.label_34)

        self.comboBox_auc_show_labels = QComboBox(self.groupBox_auc_by_arm)
        self.comboBox_auc_show_labels.setObjectName(u"comboBox_auc_show_labels")

        self.horizontalLayout_22.addWidget(self.comboBox_auc_show_labels)


        self.verticalLayout_10.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_47 = QLabel(self.groupBox_auc_by_arm)
        self.label_47.setObjectName(u"label_47")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy5)
        self.label_47.setMinimumSize(QSize(70, 0))
        self.label_47.setMaximumSize(QSize(70, 16777215))
        self.label_47.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_33.addWidget(self.label_47)

        self.comboBox_auc_by_arm_label_rotation = QComboBox(self.groupBox_auc_by_arm)
        self.comboBox_auc_by_arm_label_rotation.setObjectName(u"comboBox_auc_by_arm_label_rotation")

        self.horizontalLayout_33.addWidget(self.comboBox_auc_by_arm_label_rotation)


        self.verticalLayout_10.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_36 = QLabel(self.groupBox_auc_by_arm)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(70, 0))
        self.label_36.setMaximumSize(QSize(70, 16777215))
        self.label_36.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_26.addWidget(self.label_36)

        self.comboBox_auc_shorten_labels = QComboBox(self.groupBox_auc_by_arm)
        self.comboBox_auc_shorten_labels.setObjectName(u"comboBox_auc_shorten_labels")

        self.horizontalLayout_26.addWidget(self.comboBox_auc_shorten_labels)


        self.verticalLayout_10.addLayout(self.horizontalLayout_26)


        self.verticalLayout_7.addWidget(self.groupBox_auc_by_arm)

        self.groupBox_event_free_survival = QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_event_free_survival.setObjectName(u"groupBox_event_free_survival")
        self.groupBox_event_free_survival.setCheckable(True)
        self.groupBox_event_free_survival.setChecked(True)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_event_free_survival)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_29 = QLabel(self.groupBox_event_free_survival)
        self.label_29.setObjectName(u"label_29")

        self.verticalLayout_9.addWidget(self.label_29)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_27 = QLabel(self.groupBox_event_free_survival)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(50, 0))
        self.label_27.setMaximumSize(QSize(50, 16777215))
        self.label_27.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_27)

        self.comboBox_event_free_delta = QComboBox(self.groupBox_event_free_survival)
        self.comboBox_event_free_delta.setObjectName(u"comboBox_event_free_delta")

        self.horizontalLayout_3.addWidget(self.comboBox_event_free_delta)


        self.verticalLayout_9.addLayout(self.horizontalLayout_3)

        self.label_33 = QLabel(self.groupBox_event_free_survival)
        self.label_33.setObjectName(u"label_33")

        self.verticalLayout_9.addWidget(self.label_33)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_28 = QLabel(self.groupBox_event_free_survival)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(50, 0))
        self.label_28.setMaximumSize(QSize(50, 16777215))
        self.label_28.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_20.addWidget(self.label_28)

        self.comboBox_event_free_cutoff = QComboBox(self.groupBox_event_free_survival)
        self.comboBox_event_free_cutoff.setObjectName(u"comboBox_event_free_cutoff")

        self.horizontalLayout_20.addWidget(self.comboBox_event_free_cutoff)


        self.verticalLayout_9.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_event_free_cutoff_day = QHBoxLayout()
        self.horizontalLayout_event_free_cutoff_day.setObjectName(u"horizontalLayout_event_free_cutoff_day")
        self.label_50 = QLabel(self.groupBox_event_free_survival)
        self.label_50.setObjectName(u"label_50")
        sizePolicy5.setHeightForWidth(self.label_50.sizePolicy().hasHeightForWidth())
        self.label_50.setSizePolicy(sizePolicy5)
        self.label_50.setMinimumSize(QSize(50, 0))
        self.label_50.setMaximumSize(QSize(50, 16777215))
        self.label_50.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_event_free_cutoff_day.addWidget(self.label_50)

        self.comboBox_event_free_cutoff_days = QComboBox(self.groupBox_event_free_survival)
        self.comboBox_event_free_cutoff_days.setObjectName(u"comboBox_event_free_cutoff_days")

        self.horizontalLayout_event_free_cutoff_day.addWidget(self.comboBox_event_free_cutoff_days)


        self.verticalLayout_9.addLayout(self.horizontalLayout_event_free_cutoff_day)

        self.label_30 = QLabel(self.groupBox_event_free_survival)
        self.label_30.setObjectName(u"label_30")

        self.verticalLayout_9.addWidget(self.label_30)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_31 = QLabel(self.groupBox_event_free_survival)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(50, 0))
        self.label_31.setMaximumSize(QSize(50, 16777215))
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_21.addWidget(self.label_31)

        self.comboBox_event_free_show_risk_plot = QComboBox(self.groupBox_event_free_survival)
        self.comboBox_event_free_show_risk_plot.setObjectName(u"comboBox_event_free_show_risk_plot")

        self.horizontalLayout_21.addWidget(self.comboBox_event_free_show_risk_plot)


        self.verticalLayout_9.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_32 = QLabel(self.groupBox_event_free_survival)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(50, 0))
        self.label_32.setMaximumSize(QSize(50, 16777215))
        self.label_32.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_25.addWidget(self.label_32)

        self.comboBox_event_free_show_risk_table = QComboBox(self.groupBox_event_free_survival)
        self.comboBox_event_free_show_risk_table.setObjectName(u"comboBox_event_free_show_risk_table")

        self.horizontalLayout_25.addWidget(self.comboBox_event_free_show_risk_table)


        self.verticalLayout_9.addLayout(self.horizontalLayout_25)


        self.verticalLayout_8.addLayout(self.verticalLayout_9)


        self.verticalLayout_7.addWidget(self.groupBox_event_free_survival)

        self.groupBox_objective_response = QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_objective_response.setObjectName(u"groupBox_objective_response")
        sizePolicy2.setHeightForWidth(self.groupBox_objective_response.sizePolicy().hasHeightForWidth())
        self.groupBox_objective_response.setSizePolicy(sizePolicy2)
        self.groupBox_objective_response.setCheckable(True)
        self.groupBox_objective_response.setChecked(True)
        self.verticalLayout_groupbox_objective_response_2 = QVBoxLayout(self.groupBox_objective_response)
        self.verticalLayout_groupbox_objective_response_2.setObjectName(u"verticalLayout_groupbox_objective_response_2")
        self.label_46 = QLabel(self.groupBox_objective_response)
        self.label_46.setObjectName(u"label_46")

        self.verticalLayout_groupbox_objective_response_2.addWidget(self.label_46)

        self.verticalLayout_groupbox_objective_response = QVBoxLayout()
        self.verticalLayout_groupbox_objective_response.setObjectName(u"verticalLayout_groupbox_objective_response")
        self.verticalLayout_groupbox_objective_response.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_45 = QLabel(self.groupBox_objective_response)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setMinimumSize(QSize(70, 0))
        self.label_45.setMaximumSize(QSize(70, 16777215))
        self.label_45.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_32.addWidget(self.label_45)

        self.comboBox_obj_res_show_labels = QComboBox(self.groupBox_objective_response)
        self.comboBox_obj_res_show_labels.setObjectName(u"comboBox_obj_res_show_labels")

        self.horizontalLayout_32.addWidget(self.comboBox_obj_res_show_labels)


        self.verticalLayout_groupbox_objective_response.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.label_48 = QLabel(self.groupBox_objective_response)
        self.label_48.setObjectName(u"label_48")
        sizePolicy5.setHeightForWidth(self.label_48.sizePolicy().hasHeightForWidth())
        self.label_48.setSizePolicy(sizePolicy5)
        self.label_48.setMaximumSize(QSize(70, 16777215))
        self.label_48.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_34.addWidget(self.label_48)

        self.comboBox_objective_response_label_rotation = QComboBox(self.groupBox_objective_response)
        self.comboBox_objective_response_label_rotation.setObjectName(u"comboBox_objective_response_label_rotation")

        self.horizontalLayout_34.addWidget(self.comboBox_objective_response_label_rotation)


        self.verticalLayout_groupbox_objective_response.addLayout(self.horizontalLayout_34)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_44 = QLabel(self.groupBox_objective_response)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(70, 0))
        self.label_44.setMaximumSize(QSize(70, 16777215))
        self.label_44.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_31.addWidget(self.label_44)

        self.comboBox_obj_res_shorten_labels = QComboBox(self.groupBox_objective_response)
        self.comboBox_obj_res_shorten_labels.setObjectName(u"comboBox_obj_res_shorten_labels")

        self.horizontalLayout_31.addWidget(self.comboBox_obj_res_shorten_labels)


        self.verticalLayout_groupbox_objective_response.addLayout(self.horizontalLayout_31)

        self.label_17 = QLabel(self.groupBox_objective_response)
        self.label_17.setObjectName(u"label_17")
        sizePolicy3.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy3)
        self.label_17.setMinimumSize(QSize(0, 25))
        self.label_17.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_groupbox_objective_response.addWidget(self.label_17)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_14 = QLabel(self.groupBox_objective_response)
        self.label_14.setObjectName(u"label_14")
        sizePolicy3.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy3)
        self.label_14.setMinimumSize(QSize(25, 25))
        self.label_14.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_13.addWidget(self.label_14)

        self.comboBox_objective_plot_pd = QComboBox(self.groupBox_objective_response)
        self.comboBox_objective_plot_pd.setObjectName(u"comboBox_objective_plot_pd")
        self.comboBox_objective_plot_pd.setMinimumSize(QSize(0, 25))
        self.comboBox_objective_plot_pd.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_13.addWidget(self.comboBox_objective_plot_pd)


        self.verticalLayout_groupbox_objective_response.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_15 = QLabel(self.groupBox_objective_response)
        self.label_15.setObjectName(u"label_15")
        sizePolicy3.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy3)
        self.label_15.setMinimumSize(QSize(25, 25))
        self.label_15.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_12.addWidget(self.label_15)

        self.comboBox_objective_plot_sd = QComboBox(self.groupBox_objective_response)
        self.comboBox_objective_plot_sd.setObjectName(u"comboBox_objective_plot_sd")
        self.comboBox_objective_plot_sd.setMinimumSize(QSize(0, 25))
        self.comboBox_objective_plot_sd.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_12.addWidget(self.comboBox_objective_plot_sd)


        self.verticalLayout_groupbox_objective_response.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_11 = QLabel(self.groupBox_objective_response)
        self.label_11.setObjectName(u"label_11")
        sizePolicy3.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy3)
        self.label_11.setMinimumSize(QSize(25, 25))
        self.label_11.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_10.addWidget(self.label_11)

        self.comboBox_objective_plot_pr = QComboBox(self.groupBox_objective_response)
        self.comboBox_objective_plot_pr.setObjectName(u"comboBox_objective_plot_pr")
        self.comboBox_objective_plot_pr.setMinimumSize(QSize(0, 25))
        self.comboBox_objective_plot_pr.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_10.addWidget(self.comboBox_objective_plot_pr)


        self.verticalLayout_groupbox_objective_response.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_16 = QLabel(self.groupBox_objective_response)
        self.label_16.setObjectName(u"label_16")
        sizePolicy3.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy3)
        self.label_16.setMinimumSize(QSize(25, 25))
        self.label_16.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_11.addWidget(self.label_16)

        self.comboBox_objective_plot_cr = QComboBox(self.groupBox_objective_response)
        self.comboBox_objective_plot_cr.setObjectName(u"comboBox_objective_plot_cr")
        self.comboBox_objective_plot_cr.setMinimumSize(QSize(0, 25))
        self.comboBox_objective_plot_cr.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_11.addWidget(self.comboBox_objective_plot_cr)


        self.verticalLayout_groupbox_objective_response.addLayout(self.horizontalLayout_11)

        self.pushButton_objective_response_update = QPushButton(self.groupBox_objective_response)
        self.pushButton_objective_response_update.setObjectName(u"pushButton_objective_response_update")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pushButton_objective_response_update.sizePolicy().hasHeightForWidth())
        self.pushButton_objective_response_update.setSizePolicy(sizePolicy6)
        self.pushButton_objective_response_update.setMinimumSize(QSize(0, 25))
        self.pushButton_objective_response_update.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_groupbox_objective_response.addWidget(self.pushButton_objective_response_update)


        self.verticalLayout_groupbox_objective_response_2.addLayout(self.verticalLayout_groupbox_objective_response)


        self.verticalLayout_7.addWidget(self.groupBox_objective_response)

        self.groupBox_percent_tv_change = QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_percent_tv_change.setObjectName(u"groupBox_percent_tv_change")
        self.groupBox_percent_tv_change.setCheckable(True)
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_percent_tv_change)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_39 = QLabel(self.groupBox_percent_tv_change)
        self.label_39.setObjectName(u"label_39")

        self.verticalLayout_11.addWidget(self.label_39)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_41 = QLabel(self.groupBox_percent_tv_change)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(70, 0))
        self.label_41.setMaximumSize(QSize(70, 16777215))
        self.label_41.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_29.addWidget(self.label_41)

        self.comboBox_tv_change_normalize = QComboBox(self.groupBox_percent_tv_change)
        self.comboBox_tv_change_normalize.setObjectName(u"comboBox_tv_change_normalize")

        self.horizontalLayout_29.addWidget(self.comboBox_tv_change_normalize)


        self.verticalLayout_11.addLayout(self.horizontalLayout_29)

        self.label_43 = QLabel(self.groupBox_percent_tv_change)
        self.label_43.setObjectName(u"label_43")

        self.verticalLayout_11.addWidget(self.label_43)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_42 = QLabel(self.groupBox_percent_tv_change)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(70, 0))
        self.label_42.setMaximumSize(QSize(70, 16777215))
        self.label_42.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_30.addWidget(self.label_42)

        self.comboBox_tv_change_show_labels = QComboBox(self.groupBox_percent_tv_change)
        self.comboBox_tv_change_show_labels.setObjectName(u"comboBox_tv_change_show_labels")

        self.horizontalLayout_30.addWidget(self.comboBox_tv_change_show_labels)


        self.verticalLayout_11.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.label_49 = QLabel(self.groupBox_percent_tv_change)
        self.label_49.setObjectName(u"label_49")
        sizePolicy5.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy5)
        self.label_49.setMinimumSize(QSize(70, 0))
        self.label_49.setMaximumSize(QSize(70, 16777215))
        self.label_49.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_35.addWidget(self.label_49)

        self.comboBox_tc_change_label_rotation = QComboBox(self.groupBox_percent_tv_change)
        self.comboBox_tc_change_label_rotation.setObjectName(u"comboBox_tc_change_label_rotation")

        self.horizontalLayout_35.addWidget(self.comboBox_tc_change_label_rotation)


        self.verticalLayout_11.addLayout(self.horizontalLayout_35)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_40 = QLabel(self.groupBox_percent_tv_change)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(70, 0))
        self.label_40.setMaximumSize(QSize(70, 16777215))
        self.label_40.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_28.addWidget(self.label_40)

        self.comboBox_tv_change_shorten_labels = QComboBox(self.groupBox_percent_tv_change)
        self.comboBox_tv_change_shorten_labels.setObjectName(u"comboBox_tv_change_shorten_labels")

        self.horizontalLayout_28.addWidget(self.comboBox_tv_change_shorten_labels)


        self.verticalLayout_11.addLayout(self.horizontalLayout_28)


        self.verticalLayout_7.addWidget(self.groupBox_percent_tv_change)

        self.groupBox_configuration_spider = QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_configuration_spider.setObjectName(u"groupBox_configuration_spider")
        sizePolicy2.setHeightForWidth(self.groupBox_configuration_spider.sizePolicy().hasHeightForWidth())
        self.groupBox_configuration_spider.setSizePolicy(sizePolicy2)
        self.groupBox_configuration_spider.setCheckable(True)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_configuration_spider)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_6 = QLabel(self.groupBox_configuration_spider)
        self.label_6.setObjectName(u"label_6")
        sizePolicy2.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy2)
        self.label_6.setMinimumSize(QSize(0, 25))
        self.label_6.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.label_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox_config_data_transform = QComboBox(self.groupBox_configuration_spider)
        self.comboBox_config_data_transform.setObjectName(u"comboBox_config_data_transform")
        self.comboBox_config_data_transform.setMinimumSize(QSize(0, 25))
        self.comboBox_config_data_transform.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_2.addWidget(self.comboBox_config_data_transform)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.label_8 = QLabel(self.groupBox_configuration_spider)
        self.label_8.setObjectName(u"label_8")
        sizePolicy2.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy2)
        self.label_8.setMinimumSize(QSize(0, 20))
        self.label_8.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_6.addWidget(self.label_8)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_22 = QLabel(self.groupBox_configuration_spider)
        self.label_22.setObjectName(u"label_22")
        sizePolicy2.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy2)
        self.label_22.setMinimumSize(QSize(75, 25))
        self.label_22.setMaximumSize(QSize(75, 25))
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.label_22)

        self.comboBox_spider_time_series = QComboBox(self.groupBox_configuration_spider)
        self.comboBox_spider_time_series.setObjectName(u"comboBox_spider_time_series")
        self.comboBox_spider_time_series.setMinimumSize(QSize(0, 25))
        self.comboBox_spider_time_series.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_18.addWidget(self.comboBox_spider_time_series)


        self.verticalLayout_6.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.groupBox_configuration_spider)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)
        self.label_9.setMinimumSize(QSize(75, 25))
        self.label_9.setMaximumSize(QSize(75, 25))
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_9)

        self.comboBox_spider_aggregate = QComboBox(self.groupBox_configuration_spider)
        self.comboBox_spider_aggregate.setObjectName(u"comboBox_spider_aggregate")
        self.comboBox_spider_aggregate.setMinimumSize(QSize(0, 25))
        self.comboBox_spider_aggregate.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_5.addWidget(self.comboBox_spider_aggregate)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.groupBox_configuration_spider)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)
        self.label_7.setMinimumSize(QSize(75, 25))
        self.label_7.setMaximumSize(QSize(75, 25))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.comboBox_spider_weight = QComboBox(self.groupBox_configuration_spider)
        self.comboBox_spider_weight.setObjectName(u"comboBox_spider_weight")
        self.comboBox_spider_weight.setMinimumSize(QSize(0, 25))
        self.comboBox_spider_weight.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_4.addWidget(self.comboBox_spider_weight)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.label_23 = QLabel(self.groupBox_configuration_spider)
        self.label_23.setObjectName(u"label_23")
        sizePolicy2.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy2)
        self.label_23.setMinimumSize(QSize(0, 20))
        self.label_23.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_6.addWidget(self.label_23)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_24 = QLabel(self.groupBox_configuration_spider)
        self.label_24.setObjectName(u"label_24")
        sizePolicy2.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy2)
        self.label_24.setMinimumSize(QSize(75, 25))
        self.label_24.setMaximumSize(QSize(75, 25))
        self.label_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_19.addWidget(self.label_24)

        self.comboBox_spider_marker = QComboBox(self.groupBox_configuration_spider)
        self.comboBox_spider_marker.setObjectName(u"comboBox_spider_marker")
        self.comboBox_spider_marker.setMinimumSize(QSize(0, 25))
        self.comboBox_spider_marker.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_19.addWidget(self.comboBox_spider_marker)


        self.verticalLayout_6.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_26 = QLabel(self.groupBox_configuration_spider)
        self.label_26.setObjectName(u"label_26")
        sizePolicy2.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy2)
        self.label_26.setMinimumSize(QSize(75, 25))
        self.label_26.setMaximumSize(QSize(75, 25))
        self.label_26.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_24.addWidget(self.label_26)

        self.comboBox_spider_sem = QComboBox(self.groupBox_configuration_spider)
        self.comboBox_spider_sem.setObjectName(u"comboBox_spider_sem")
        self.comboBox_spider_sem.setMinimumSize(QSize(0, 25))
        self.comboBox_spider_sem.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_24.addWidget(self.comboBox_spider_sem)


        self.verticalLayout_6.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_25 = QLabel(self.groupBox_configuration_spider)
        self.label_25.setObjectName(u"label_25")
        sizePolicy3.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy3)
        self.label_25.setMinimumSize(QSize(75, 25))
        self.label_25.setMaximumSize(QSize(75, 25))
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_23.addWidget(self.label_25)

        self.comboBox_spider_err_bars = QComboBox(self.groupBox_configuration_spider)
        self.comboBox_spider_err_bars.setObjectName(u"comboBox_spider_err_bars")

        self.horizontalLayout_23.addWidget(self.comboBox_spider_err_bars)


        self.verticalLayout_6.addLayout(self.horizontalLayout_23)


        self.verticalLayout_4.addLayout(self.verticalLayout_6)


        self.verticalLayout_7.addWidget(self.groupBox_configuration_spider)

        self.label_10 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_10.setObjectName(u"label_10")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy7)
        self.label_10.setMinimumSize(QSize(75, 0))
        self.label_10.setMaximumSize(QSize(75, 16777215))

        self.verticalLayout_7.addWidget(self.label_10)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_visual_graph_settings.addWidget(self.scrollArea, 0, Qt.AlignRight)


        self.horizontalLayout_figure_grid.addLayout(self.verticalLayout_visual_graph_settings)


        self.verticalLayout_2.addLayout(self.horizontalLayout_figure_grid)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 970, 23))
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
        self.groupBox_plot_configurations.setTitle(QCoreApplication.translate("MainWindow", u"Plot Configuration", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Study", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"# of Plots:", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"1.", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"2.", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"3.", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"4.", None))
        self.groupBox_plot_style_sheet.setTitle(QCoreApplication.translate("MainWindow", u"Plot Style Sheet", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Module", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Style", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Journal", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Grid", None))
        self.pushButton_plot_uodate_style.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.groupBox_auc_by_arm.setTitle(QCoreApplication.translate("MainWindow", u"AUC by ARM", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"AUC", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Normal.", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Labels", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Shorten", None))
        self.groupBox_event_free_survival.setTitle(QCoreApplication.translate("MainWindow", u"Event-Free Survivial", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Delta", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Cutoff", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Day", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Show Risk", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Table", None))
        self.groupBox_objective_response.setTitle(QCoreApplication.translate("MainWindow", u"Objective Response Plot", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Labels", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Shorten", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Set Obj. Response Color", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"PD", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"SD", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"PR", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"CR", None))
        self.pushButton_objective_response_update.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.groupBox_percent_tv_change.setTitle(QCoreApplication.translate("MainWindow", u"Percent TV Change", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Data", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Normal.", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Labels", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Shorten", None))
        self.groupBox_configuration_spider.setTitle(QCoreApplication.translate("MainWindow", u"Spider Plot", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Data Transform", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Show:", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Time Series", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Aggregate", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Weight", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Aggregate:", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Marker", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"SEM", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Err. Bars", None))
        self.label_10.setText("")
        self.menuShow.setTitle(QCoreApplication.translate("MainWindow", u"Show", None))
    # retranslateUi


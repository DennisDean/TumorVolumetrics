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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(925, 619)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_control = QHBoxLayout()
        self.horizontalLayout_control.setObjectName(u"horizontalLayout_control")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(90, 0))
        self.label_2.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_control.addWidget(self.label_2)

        self.comboBox_control_experiments = QComboBox(self.centralwidget)
        self.comboBox_control_experiments.setObjectName(u"comboBox_control_experiments")
        self.comboBox_control_experiments.setMinimumSize(QSize(150, 0))
        self.comboBox_control_experiments.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_control.addWidget(self.comboBox_control_experiments)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_control.addWidget(self.label_3)

        self.pushButton_control_avg_tv = QPushButton(self.centralwidget)
        self.pushButton_control_avg_tv.setObjectName(u"pushButton_control_avg_tv")
        self.pushButton_control_avg_tv.setMinimumSize(QSize(90, 0))
        self.pushButton_control_avg_tv.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_control.addWidget(self.pushButton_control_avg_tv)

        self.pushButton_control_tc_ratio = QPushButton(self.centralwidget)
        self.pushButton_control_tc_ratio.setObjectName(u"pushButton_control_tc_ratio")
        self.pushButton_control_tc_ratio.setMinimumSize(QSize(90, 0))
        self.pushButton_control_tc_ratio.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_control.addWidget(self.pushButton_control_tc_ratio)

        self.pushButton_control_auc = QPushButton(self.centralwidget)
        self.pushButton_control_auc.setObjectName(u"pushButton_control_auc")
        self.pushButton_control_auc.setMinimumSize(QSize(90, 0))
        self.pushButton_control_auc.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_control.addWidget(self.pushButton_control_auc)

        self.pushButton_control_log_2_change = QPushButton(self.centralwidget)
        self.pushButton_control_log_2_change.setObjectName(u"pushButton_control_log_2_change")
        self.pushButton_control_log_2_change.setMinimumSize(QSize(90, 0))
        self.pushButton_control_log_2_change.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_control.addWidget(self.pushButton_control_log_2_change)

        self.pushButton_control_objective_response_classification = QPushButton(self.centralwidget)
        self.pushButton_control_objective_response_classification.setObjectName(u"pushButton_control_objective_response_classification")
        self.pushButton_control_objective_response_classification.setMinimumSize(QSize(90, 0))
        self.pushButton_control_objective_response_classification.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_control.addWidget(self.pushButton_control_objective_response_classification)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_control.addWidget(self.label_4)

        self.pushButton_control_graph_export_settings = QPushButton(self.centralwidget)
        self.pushButton_control_graph_export_settings.setObjectName(u"pushButton_control_graph_export_settings")
        self.pushButton_control_graph_export_settings.setMinimumSize(QSize(25, 25))
        self.pushButton_control_graph_export_settings.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_control.addWidget(self.pushButton_control_graph_export_settings)


        self.verticalLayout_2.addLayout(self.horizontalLayout_control)

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
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(75, 25))
        self.label_5.setMaximumSize(QSize(75, 25))

        self.horizontalLayout.addWidget(self.label_5, 0, Qt.AlignTop)

        self.comboBox_2 = QComboBox(self.groupBox)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout.addWidget(self.comboBox_2, 0, Qt.AlignTop)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.comboBox_5 = QComboBox(self.groupBox)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.verticalLayout_3.addWidget(self.comboBox_5)

        self.comboBox_4 = QComboBox(self.groupBox)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.verticalLayout_3.addWidget(self.comboBox_4)

        self.comboBox_3 = QComboBox(self.groupBox)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.verticalLayout_3.addWidget(self.comboBox_3)

        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_3.addWidget(self.comboBox)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)


        self.verticalLayout_visual_graph_settings.addWidget(self.groupBox)


        self.horizontalLayout_figure_grid.addLayout(self.verticalLayout_visual_graph_settings)


        self.verticalLayout_2.addLayout(self.horizontalLayout_figure_grid)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 925, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Experiment", None))
        self.label_3.setText("")
        self.pushButton_control_avg_tv.setText(QCoreApplication.translate("MainWindow", u"Avg TV \u0394", None))
        self.pushButton_control_tc_ratio.setText(QCoreApplication.translate("MainWindow", u"T/C Ratio", None))
        self.pushButton_control_auc.setText(QCoreApplication.translate("MainWindow", u"AUC", None))
        self.pushButton_control_log_2_change.setText(QCoreApplication.translate("MainWindow", u"log2 \u0394", None))
        self.pushButton_control_objective_response_classification.setText(QCoreApplication.translate("MainWindow", u"ORC", None))
        self.label_4.setText("")
        self.pushButton_control_graph_export_settings.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Plot Configuration", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"# of Plots:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi


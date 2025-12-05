# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TumorVolumetricsInterface.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(334, 646)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExperiment = QAction(MainWindow)
        self.actionExperiment.setObjectName(u"actionExperiment")
        self.actionStudy = QAction(MainWindow)
        self.actionStudy.setObjectName(u"actionStudy")
        self.actionCurves = QAction(MainWindow)
        self.actionCurves.setObjectName(u"actionCurves")
        self.actionShow = QAction(MainWindow)
        self.actionShow.setObjectName(u"actionShow")
        self.actionTumor_Volume_CSV = QAction(MainWindow)
        self.actionTumor_Volume_CSV.setObjectName(u"actionTumor_Volume_CSV")
        self.actionTumor_Volume_Extended = QAction(MainWindow)
        self.actionTumor_Volume_Extended.setObjectName(u"actionTumor_Volume_Extended")
        self.actionTumor_Volume_XML = QAction(MainWindow)
        self.actionTumor_Volume_XML.setObjectName(u"actionTumor_Volume_XML")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(300, 0))
        self.centralwidget.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_load_file_path = QLineEdit(self.groupBox)
        self.lineEdit_load_file_path.setObjectName(u"lineEdit_load_file_path")
        self.lineEdit_load_file_path.setMinimumSize(QSize(0, 25))
        self.lineEdit_load_file_path.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_2.addWidget(self.lineEdit_load_file_path)

        self.pushButton_load_select_file = QPushButton(self.groupBox)
        self.pushButton_load_select_file.setObjectName(u"pushButton_load_select_file")
        self.pushButton_load_select_file.setMinimumSize(QSize(25, 25))
        self.pushButton_load_select_file.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_2.addWidget(self.pushButton_load_select_file)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(75, 25))
        self.pushButton.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_load_saveas = QPushButton(self.groupBox)
        self.pushButton_load_saveas.setObjectName(u"pushButton_load_saveas")
        self.pushButton_load_saveas.setMinimumSize(QSize(75, 25))
        self.pushButton_load_saveas.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_3.addWidget(self.pushButton_load_saveas)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.groupBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(85, 25))
        self.label_2.setMaximumSize(QSize(85, 25))

        self.horizontalLayout_4.addWidget(self.label_2)

        self.comboBox_show_experiment = QComboBox(self.groupBox_3)
        self.comboBox_show_experiment.setObjectName(u"comboBox_show_experiment")
        self.comboBox_show_experiment.setMinimumSize(QSize(0, 25))
        self.comboBox_show_experiment.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_4.addWidget(self.comboBox_show_experiment)

        self.pushButton_show_experiment = QPushButton(self.groupBox_3)
        self.pushButton_show_experiment.setObjectName(u"pushButton_show_experiment")
        self.pushButton_show_experiment.setMinimumSize(QSize(25, 25))
        self.pushButton_show_experiment.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_4.addWidget(self.pushButton_show_experiment)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(85, 25))
        self.label_3.setMaximumSize(QSize(85, 25))

        self.horizontalLayout_5.addWidget(self.label_3)

        self.comboBox_show_study = QComboBox(self.groupBox_3)
        self.comboBox_show_study.setObjectName(u"comboBox_show_study")
        self.comboBox_show_study.setMinimumSize(QSize(0, 25))
        self.comboBox_show_study.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_5.addWidget(self.comboBox_show_study)

        self.pushButton_show_study = QPushButton(self.groupBox_3)
        self.pushButton_show_study.setObjectName(u"pushButton_show_study")
        self.pushButton_show_study.setMinimumSize(QSize(25, 25))
        self.pushButton_show_study.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_5.addWidget(self.pushButton_show_study)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(85, 25))
        self.label_4.setMaximumSize(QSize(85, 25))

        self.horizontalLayout_6.addWidget(self.label_4)

        self.comboBox_show_curves = QComboBox(self.groupBox_3)
        self.comboBox_show_curves.setObjectName(u"comboBox_show_curves")
        self.comboBox_show_curves.setMinimumSize(QSize(0, 25))
        self.comboBox_show_curves.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_6.addWidget(self.comboBox_show_curves)

        self.pushButton_show_curves = QPushButton(self.groupBox_3)
        self.pushButton_show_curves.setObjectName(u"pushButton_show_curves")
        self.pushButton_show_curves.setMinimumSize(QSize(25, 25))
        self.pushButton_show_curves.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_6.addWidget(self.pushButton_show_curves)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.treeWidget_navigate_file = QTreeWidget(self.groupBox_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_navigate_file.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_navigate_file.setObjectName(u"treeWidget_navigate_file")

        self.verticalLayout_4.addWidget(self.treeWidget_navigate_file)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 334, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionShow)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionExperiment)
        self.menuView.addAction(self.actionStudy)
        self.menuView.addAction(self.actionCurves)
        self.menuHelp.addAction(self.actionTumor_Volume_CSV)
        self.menuHelp.addAction(self.actionTumor_Volume_Extended)
        self.menuHelp.addAction(self.actionTumor_Volume_XML)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionExperiment.setText(QCoreApplication.translate("MainWindow", u"View Experiment", None))
        self.actionStudy.setText(QCoreApplication.translate("MainWindow", u"View Study", None))
        self.actionCurves.setText(QCoreApplication.translate("MainWindow", u"View Curves", None))
        self.actionShow.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.actionTumor_Volume_CSV.setText(QCoreApplication.translate("MainWindow", u"Tumor Volume CSV", None))
        self.actionTumor_Volume_Extended.setText(QCoreApplication.translate("MainWindow", u"Tumor Volume Extended", None))
        self.actionTumor_Volume_XML.setText(QCoreApplication.translate("MainWindow", u"Tumor Volume XML", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Load Tumor Volume File", None))
        self.pushButton_load_select_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.pushButton_load_saveas.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Experiment", None))
        self.pushButton_show_experiment.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Study", None))
        self.pushButton_show_study.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Curves", None))
        self.pushButton_show_curves.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Navigate", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi


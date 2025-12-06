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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(364, 575)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 75))
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(300, 0))
        self.centralwidget.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.groupBox_load = QGroupBox(self.centralwidget)
        self.groupBox_load.setObjectName(u"groupBox_load")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_load.sizePolicy().hasHeightForWidth())
        self.groupBox_load.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_load)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.groupBox_load)
        self.label.setObjectName(u"label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.label)

        self.pushButton_load_select_file = QPushButton(self.groupBox_load)
        self.pushButton_load_select_file.setObjectName(u"pushButton_load_select_file")
        self.pushButton_load_select_file.setMinimumSize(QSize(75, 25))
        self.pushButton_load_select_file.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_3.addWidget(self.pushButton_load_select_file, 0, Qt.AlignLeft)

        self.label_9 = QLabel(self.groupBox_load)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label_9)

        self.pushButton = QPushButton(self.groupBox_load)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(75, 25))
        self.pushButton.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_load_saveas = QPushButton(self.groupBox_load)
        self.pushButton_load_saveas.setObjectName(u"pushButton_load_saveas")
        self.pushButton_load_saveas.setMinimumSize(QSize(75, 25))
        self.pushButton_load_saveas.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_3.addWidget(self.pushButton_load_saveas)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.groupBox_load, 0, Qt.AlignTop)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_show = QVBoxLayout()
        self.verticalLayout_show.setObjectName(u"verticalLayout_show")
        self.groupBox_show = QGroupBox(self.centralwidget)
        self.groupBox_show.setObjectName(u"groupBox_show")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_show)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.groupBox_show)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(85, 25))
        self.label_5.setMaximumSize(QSize(85, 25))

        self.horizontalLayout.addWidget(self.label_5)

        self.comboBox_show_contributor = QComboBox(self.groupBox_show)
        self.comboBox_show_contributor.setObjectName(u"comboBox_show_contributor")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBox_show_contributor.sizePolicy().hasHeightForWidth())
        self.comboBox_show_contributor.setSizePolicy(sizePolicy4)
        self.comboBox_show_contributor.setMinimumSize(QSize(0, 25))
        self.comboBox_show_contributor.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.comboBox_show_contributor)

        self.pushButton_show_contributor = QPushButton(self.groupBox_show)
        self.pushButton_show_contributor.setObjectName(u"pushButton_show_contributor")
        self.pushButton_show_contributor.setMinimumSize(QSize(25, 25))
        self.pushButton_show_contributor.setMaximumSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButton_show_contributor)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_8 = QLabel(self.groupBox_show)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(85, 25))
        self.label_8.setMaximumSize(QSize(85, 25))

        self.horizontalLayout_9.addWidget(self.label_8)

        self.comboBox_show_disease = QComboBox(self.groupBox_show)
        self.comboBox_show_disease.setObjectName(u"comboBox_show_disease")
        self.comboBox_show_disease.setMinimumSize(QSize(0, 25))
        self.comboBox_show_disease.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_9.addWidget(self.comboBox_show_disease)

        self.pushButton_show_disease = QPushButton(self.groupBox_show)
        self.pushButton_show_disease.setObjectName(u"pushButton_show_disease")
        self.pushButton_show_disease.setMinimumSize(QSize(25, 25))
        self.pushButton_show_disease.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_9.addWidget(self.pushButton_show_disease)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.groupBox_show)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(85, 25))
        self.label_2.setMaximumSize(QSize(85, 25))

        self.horizontalLayout_4.addWidget(self.label_2)

        self.comboBox_show_experiment = QComboBox(self.groupBox_show)
        self.comboBox_show_experiment.setObjectName(u"comboBox_show_experiment")
        self.comboBox_show_experiment.setMinimumSize(QSize(0, 25))
        self.comboBox_show_experiment.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_4.addWidget(self.comboBox_show_experiment)

        self.pushButton_show_experiment = QPushButton(self.groupBox_show)
        self.pushButton_show_experiment.setObjectName(u"pushButton_show_experiment")
        self.pushButton_show_experiment.setMinimumSize(QSize(25, 25))
        self.pushButton_show_experiment.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_4.addWidget(self.pushButton_show_experiment)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.groupBox_show)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(85, 25))
        self.label_3.setMaximumSize(QSize(85, 25))

        self.horizontalLayout_5.addWidget(self.label_3)

        self.comboBox_show_study = QComboBox(self.groupBox_show)
        self.comboBox_show_study.setObjectName(u"comboBox_show_study")
        self.comboBox_show_study.setMinimumSize(QSize(0, 25))
        self.comboBox_show_study.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_5.addWidget(self.comboBox_show_study)

        self.pushButton_show_study = QPushButton(self.groupBox_show)
        self.pushButton_show_study.setObjectName(u"pushButton_show_study")
        self.pushButton_show_study.setMinimumSize(QSize(25, 25))
        self.pushButton_show_study.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_5.addWidget(self.pushButton_show_study)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetFixedSize)
        self.label_7 = QLabel(self.groupBox_show)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(85, 25))
        self.label_7.setMaximumSize(QSize(85, 25))

        self.horizontalLayout_8.addWidget(self.label_7)

        self.comboBox_show_arms = QComboBox(self.groupBox_show)
        self.comboBox_show_arms.setObjectName(u"comboBox_show_arms")
        self.comboBox_show_arms.setMinimumSize(QSize(0, 25))
        self.comboBox_show_arms.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_8.addWidget(self.comboBox_show_arms)

        self.pushButton_show_arm = QPushButton(self.groupBox_show)
        self.pushButton_show_arm.setObjectName(u"pushButton_show_arm")
        self.pushButton_show_arm.setMinimumSize(QSize(25, 25))
        self.pushButton_show_arm.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_8.addWidget(self.pushButton_show_arm)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.groupBox_show)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(85, 25))
        self.label_4.setMaximumSize(QSize(85, 25))

        self.horizontalLayout_6.addWidget(self.label_4)

        self.comboBox_show_curves = QComboBox(self.groupBox_show)
        self.comboBox_show_curves.setObjectName(u"comboBox_show_curves")
        self.comboBox_show_curves.setMinimumSize(QSize(0, 25))
        self.comboBox_show_curves.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_6.addWidget(self.comboBox_show_curves)

        self.pushButton_show_curves = QPushButton(self.groupBox_show)
        self.pushButton_show_curves.setObjectName(u"pushButton_show_curves")
        self.pushButton_show_curves.setMinimumSize(QSize(25, 25))
        self.pushButton_show_curves.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_6.addWidget(self.pushButton_show_curves)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.groupBox_show)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 25))
        self.label_6.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_7.addWidget(self.label_6)

        self.checkBox = QCheckBox(self.groupBox_show)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMinimumSize(QSize(95, 25))
        self.checkBox.setMaximumSize(QSize(95, 25))
        self.checkBox.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_7.addWidget(self.checkBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)


        self.verticalLayout_show.addWidget(self.groupBox_show)


        self.verticalLayout_2.addLayout(self.verticalLayout_show)

        self.verticalLayout_navigate = QVBoxLayout()
        self.verticalLayout_navigate.setObjectName(u"verticalLayout_navigate")
        self.groupBox_navigate = QGroupBox(self.centralwidget)
        self.groupBox_navigate.setObjectName(u"groupBox_navigate")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_navigate)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.treeWidget_navigate_file = QTreeWidget(self.groupBox_navigate)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_navigate_file.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_navigate_file.setObjectName(u"treeWidget_navigate_file")

        self.verticalLayout_4.addWidget(self.treeWidget_navigate_file)


        self.verticalLayout_navigate.addWidget(self.groupBox_navigate)


        self.verticalLayout_2.addLayout(self.verticalLayout_navigate)

        self.horizontalLayout_spacer = QHBoxLayout()
        self.horizontalLayout_spacer.setObjectName(u"horizontalLayout_spacer")
        self.label_bottom_seperator = QLabel(self.centralwidget)
        self.label_bottom_seperator.setObjectName(u"label_bottom_seperator")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_bottom_seperator.sizePolicy().hasHeightForWidth())
        self.label_bottom_seperator.setSizePolicy(sizePolicy5)
        self.label_bottom_seperator.setMinimumSize(QSize(100, 0))
        self.label_bottom_seperator.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_spacer.addWidget(self.label_bottom_seperator)


        self.verticalLayout_2.addLayout(self.horizontalLayout_spacer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 364, 23))
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
        self.groupBox_load.setTitle(QCoreApplication.translate("MainWindow", u"Load Tumor Volume File", None))
        self.label.setText("")
        self.pushButton_load_select_file.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.label_9.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.pushButton_load_saveas.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.groupBox_show.setTitle(QCoreApplication.translate("MainWindow", u"Show", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Contributor", None))
        self.pushButton_show_contributor.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Disease", None))
        self.pushButton_show_disease.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Experiment", None))
        self.pushButton_show_experiment.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Study", None))
        self.pushButton_show_study.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Arms", None))
        self.pushButton_show_arm.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TV Curves", None))
        self.pushButton_show_curves.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_6.setText("")
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Show All", None))
        self.groupBox_navigate.setTitle(QCoreApplication.translate("MainWindow", u"Navigate", None))
        self.label_bottom_seperator.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cp_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QProgressBar, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.WindowModal)
        MainWindow.resize(760, 566)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_9 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_8.addWidget(self.label_12)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_8.addWidget(self.comboBox_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.verticalLayout_2.setStretch(0, 9)

        self.horizontalLayout_9.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(110, 0))
        self.label.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(20, 0))

        self.horizontalLayout_2.addWidget(self.label_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(110, 0))
        self.label_2.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(20, 0))

        self.horizontalLayout_3.addWidget(self.label_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton = QRadioButton(self.centralwidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.horizontalLayout_4.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_4.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.centralwidget)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_4.addWidget(self.radioButton_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_5.addWidget(self.label_7)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_6.addWidget(self.label_5)

        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_6.addWidget(self.lineEdit_3)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_6.addWidget(self.label_9)

        self.lineEdit_4 = QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_6.addWidget(self.lineEdit_4)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_6.addWidget(self.label_8)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_6.addWidget(self.label_10)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(300, 16777214))

        self.horizontalLayout_6.addWidget(self.comboBox)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_6.addWidget(self.label_11)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget.rowCount() < 8):
            self.tableWidget.setRowCount(8)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(0, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(1, 1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(2, 1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(3, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(4, 1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(5, 1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(6, 1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(7, 1, __qtablewidgetitem17)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(0, 270))
        self.tableWidget.setMaximumSize(QSize(320, 16777215))

        self.verticalLayout_3.addWidget(self.tableWidget)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.pushBack = QPushButton(self.centralwidget)
        self.pushBack.setObjectName(u"pushBack")

        self.verticalLayout_4.addWidget(self.pushBack)

        self.progress_2 = QProgressBar(self.centralwidget)
        self.progress_2.setObjectName(u"progress_2")
        self.progress_2.setMaximumSize(QSize(16777215, 2))
        self.progress_2.setValue(0)
        self.progress_2.setTextVisible(False)
        self.progress_2.setInvertedAppearance(False)

        self.verticalLayout_4.addWidget(self.progress_2)


        self.horizontalLayout_7.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)

        self.verticalLayout.addWidget(self.pushButton)

        self.progress = QProgressBar(self.centralwidget)
        self.progress.setObjectName(u"progress")
        self.progress.setMaximumSize(QSize(16777215, 2))
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setInvertedAppearance(False)

        self.verticalLayout.addWidget(self.progress)


        self.horizontalLayout_7.addLayout(self.verticalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, -1, 0, -1)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.pushExport = QPushButton(self.centralwidget)
        self.pushExport.setObjectName(u"pushExport")

        self.verticalLayout_5.addWidget(self.pushExport)

        self.progress_3 = QProgressBar(self.centralwidget)
        self.progress_3.setObjectName(u"progress_3")
        self.progress_3.setMaximumSize(QSize(16777215, 2))
        self.progress_3.setValue(0)
        self.progress_3.setTextVisible(False)
        self.progress_3.setInvertedAppearance(False)

        self.verticalLayout_5.addWidget(self.progress_3)


        self.horizontalLayout_7.addLayout(self.verticalLayout_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)

        self.pushCloseAll = QPushButton(self.centralwidget)
        self.pushCloseAll.setObjectName(u"pushCloseAll")

        self.horizontalLayout_10.addWidget(self.pushCloseAll)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_9.addLayout(self.verticalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 760, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"debyetools - [termodynamic properties]", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"                                                                           property to plot:", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(5, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(6, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(7, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(8, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(9, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.comboBox_2.setItemText(10, QCoreApplication.translate("MainWindow", u"New Item", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"Temperature range:", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"0.1 1000.1 100", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"K", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Pressure:", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"0 30 10", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"GPa", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"Slater", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Dugdale-MacDonald", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"mean-free-volume", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"FactSage parameters:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"From:", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"298.15", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"K", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"to:", None))
        self.lineEdit_4.setText(QCoreApplication.translate("MainWindow", u"1000.1", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"K", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"P:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"GPa", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Values", None));
        ___qtablewidgetitem1 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"G+TS (T=298.15)", None));
        ___qtablewidgetitem2 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"S (T=298.15)", None));
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"C0", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"C1", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"C2", None));
        ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"C3", None));
        ___qtablewidgetitem7 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"C4", None));
        ___qtablewidgetitem8 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"C5", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem9 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"J/mol-at", None));
        ___qtablewidgetitem10 = self.tableWidget.item(1, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"J/K/mol-at", None));
        ___qtablewidgetitem11 = self.tableWidget.item(2, 1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"T^(0)", None));
        ___qtablewidgetitem12 = self.tableWidget.item(3, 1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"T^(1)", None));
        ___qtablewidgetitem13 = self.tableWidget.item(4, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"T^(-2)", None));
        ___qtablewidgetitem14 = self.tableWidget.item(5, 1)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"T^(2)", None));
        ___qtablewidgetitem15 = self.tableWidget.item(6, 1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"T^(-0.5)", None));
        ___qtablewidgetitem16 = self.tableWidget.item(7, 1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"T^(-3)", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.pushBack.setText(QCoreApplication.translate("MainWindow", u"<back", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"re-calculate", None))
        self.pushExport.setText(QCoreApplication.translate("MainWindow", u"export parameters", None))
        self.pushCloseAll.setText(QCoreApplication.translate("MainWindow", u"close all...", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_small.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

from debyetools.tpropsgui.custom_widgets import ClickableLineEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.WindowModal)
        MainWindow.resize(476, 466)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_11 = ClickableLineEdit(self.centralwidget)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setEnabled(True)
        self.lineEdit_11.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_11)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.label_25 = QLabel(self.centralwidget)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout.addWidget(self.label_25)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_24 = QLabel(self.centralwidget)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout.addWidget(self.label_24)


        self.verticalLayout_8.addLayout(self.horizontalLayout)

        self.frame_6 = QFrame(self.centralwidget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_6)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.label_7 = QLabel(self.frame_6)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.lineEdit_2 = QLineEdit(self.frame_6)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_4.addWidget(self.lineEdit_2)

        self.comboBox = QComboBox(self.frame_6)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_4.addWidget(self.comboBox)

        self.moreinfo = QLabel(self.frame_6)
        self.moreinfo.setObjectName(u"moreinfo")
        font = QFont()
        font.setPointSize(10)
        self.moreinfo.setFont(font)

        self.horizontalLayout_4.addWidget(self.moreinfo)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushFitEOS = QPushButton(self.frame_6)
        self.pushFitEOS.setObjectName(u"pushFitEOS")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushFitEOS.sizePolicy().hasHeightForWidth())
        self.pushFitEOS.setSizePolicy(sizePolicy)
        self.pushFitEOS.setMinimumSize(QSize(0, 25))

        self.verticalLayout_2.addWidget(self.pushFitEOS)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_8.addWidget(self.frame_6)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame)
        self.verticalLayout_12.setSpacing(2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 2, 0)
        self.label_16 = QLabel(self.frame)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 22))
        self.label_16.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_7.addWidget(self.label_16)

        self.lineEdit_3 = QLineEdit(self.frame)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(0, 22))
        self.lineEdit_3.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_7.addWidget(self.lineEdit_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.pushNu = QPushButton(self.frame)
        self.pushNu.setObjectName(u"pushNu")

        self.horizontalLayout_7.addWidget(self.pushNu)


        self.verticalLayout_12.addLayout(self.horizontalLayout_7)


        self.verticalLayout_8.addWidget(self.frame)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_8.setSpacing(2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.checkBox = QCheckBox(self.frame_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.horizontalLayout_8.addWidget(self.checkBox)

        self.lineEdit_el = QLineEdit(self.frame_2)
        self.lineEdit_el.setObjectName(u"lineEdit_el")

        self.horizontalLayout_8.addWidget(self.lineEdit_el)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.pushDoscar = QPushButton(self.frame_2)
        self.pushDoscar.setObjectName(u"pushDoscar")

        self.horizontalLayout_8.addWidget(self.pushDoscar)


        self.verticalLayout_8.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_9.setSpacing(2)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.checkBox_2 = QCheckBox(self.frame_3)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setMinimumSize(QSize(0, 22))
        self.checkBox_2.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_14.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.frame_3)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setMinimumSize(QSize(0, 22))
        self.checkBox_3.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_14.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.frame_3)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setMinimumSize(QSize(0, 22))
        self.checkBox_4.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_14.addWidget(self.checkBox_4)


        self.horizontalLayout_9.addLayout(self.verticalLayout_14)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.lineEdit_def = QLineEdit(self.frame_3)
        self.lineEdit_def.setObjectName(u"lineEdit_def")
        self.lineEdit_def.setEnabled(False)
        self.lineEdit_def.setMinimumSize(QSize(0, 22))
        self.lineEdit_def.setMaximumSize(QSize(16777215, 22))
        self.lineEdit_def.setFrame(True)

        self.verticalLayout_15.addWidget(self.lineEdit_def)

        self.lineEdit_anh = QLineEdit(self.frame_3)
        self.lineEdit_anh.setObjectName(u"lineEdit_anh")
        self.lineEdit_anh.setEnabled(False)
        self.lineEdit_anh.setMinimumSize(QSize(0, 22))
        self.lineEdit_anh.setMaximumSize(QSize(16777215, 22))
        self.lineEdit_anh.setFrame(True)

        self.verticalLayout_15.addWidget(self.lineEdit_anh)

        self.lineEdit_xs = QLineEdit(self.frame_3)
        self.lineEdit_xs.setObjectName(u"lineEdit_xs")
        self.lineEdit_xs.setEnabled(False)
        self.lineEdit_xs.setMinimumSize(QSize(0, 22))
        self.lineEdit_xs.setMaximumSize(QSize(16777215, 22))
        self.lineEdit_xs.setFrame(True)

        self.verticalLayout_15.addWidget(self.lineEdit_xs)


        self.horizontalLayout_9.addLayout(self.verticalLayout_15)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)


        self.verticalLayout_8.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_5 = QCheckBox(self.frame_4)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setMinimumSize(QSize(0, 22))
        self.checkBox_5.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_2.addWidget(self.checkBox_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.lineEdit_xspol = QLineEdit(self.frame_4)
        self.lineEdit_xspol.setObjectName(u"lineEdit_xspol")
        self.lineEdit_xspol.setEnabled(False)
        self.lineEdit_xspol.setMinimumSize(QSize(0, 22))
        self.lineEdit_xspol.setMaximumSize(QSize(16777215, 22))
        self.lineEdit_xspol.setFrame(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_xspol)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_8.addWidget(self.frame_4)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)

        self.verticalLayout_TP = QVBoxLayout()
        self.verticalLayout_TP.setSpacing(0)
        self.verticalLayout_TP.setObjectName(u"verticalLayout_TP")
        self.verticalLayout_TP.setContentsMargins(0, -1, -1, -1)
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_TP.addItem(self.verticalSpacer_9)

        self.horizontalLayout_T = QHBoxLayout()
        self.horizontalLayout_T.setSpacing(0)
        self.horizontalLayout_T.setObjectName(u"horizontalLayout_T")
        self.horizontalLayout_T.setContentsMargins(0, -1, -1, -1)
        self.label_T = QLabel(self.centralwidget)
        self.label_T.setObjectName(u"label_T")

        self.horizontalLayout_T.addWidget(self.label_T)

        self.lineEdit_T = QLineEdit(self.centralwidget)
        self.lineEdit_T.setObjectName(u"lineEdit_T")

        self.horizontalLayout_T.addWidget(self.lineEdit_T)

        self.label_T_2 = QLabel(self.centralwidget)
        self.label_T_2.setObjectName(u"label_T_2")
        self.label_T_2.setMinimumSize(QSize(20, 0))
        self.label_T_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_T.addWidget(self.label_T_2)


        self.verticalLayout_TP.addLayout(self.horizontalLayout_T)

        self.horizontalLayout_P = QHBoxLayout()
        self.horizontalLayout_P.setSpacing(0)
        self.horizontalLayout_P.setObjectName(u"horizontalLayout_P")
        self.horizontalLayout_P.setContentsMargins(0, -1, -1, -1)
        self.label_P = QLabel(self.centralwidget)
        self.label_P.setObjectName(u"label_P")

        self.horizontalLayout_P.addWidget(self.label_P)

        self.lineEdit_P = QLineEdit(self.centralwidget)
        self.lineEdit_P.setObjectName(u"lineEdit_P")

        self.horizontalLayout_P.addWidget(self.lineEdit_P)

        self.label_P_2 = QLabel(self.centralwidget)
        self.label_P_2.setObjectName(u"label_P_2")
        self.label_P_2.setMinimumSize(QSize(20, 0))
        self.label_P_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_P.addWidget(self.label_P_2)


        self.verticalLayout_TP.addLayout(self.horizontalLayout_P)


        self.horizontalLayout_10.addLayout(self.verticalLayout_TP)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setSpacing(2)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_8)

        self.pushgoback = QPushButton(self.centralwidget)
        self.pushgoback.setObjectName(u"pushgoback")
        self.pushgoback.setEnabled(True)

        self.verticalLayout_17.addWidget(self.pushgoback)

        self.progress_3 = QProgressBar(self.centralwidget)
        self.progress_3.setObjectName(u"progress_3")
        self.progress_3.setMaximumSize(QSize(16777215, 2))
        self.progress_3.setValue(0)
        self.progress_3.setTextVisible(False)
        self.progress_3.setInvertedAppearance(False)

        self.verticalLayout_17.addWidget(self.progress_3)


        self.horizontalLayout_10.addLayout(self.verticalLayout_17)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(2)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_7)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setEnabled(True)

        self.verticalLayout_16.addWidget(self.pushButton_5)

        self.progress = QProgressBar(self.centralwidget)
        self.progress.setObjectName(u"progress")
        self.progress.setMaximumSize(QSize(16777215, 2))
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setInvertedAppearance(False)

        self.verticalLayout_16.addWidget(self.progress)


        self.horizontalLayout_10.addLayout(self.verticalLayout_16)


        self.verticalLayout_8.addLayout(self.horizontalLayout_10)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 476, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"debyetools - [input parameters]", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"formula:", None))
        self.lineEdit_11.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"mass:", None))
        self.lineEdit.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"kg/mol-at", None))
        self.label_25.setText("")
        self.label_24.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"EOS params:", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"-3e5, 1e-5, 7e10, 4", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Birch-Murnaghan", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Rose-Vinet", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Mie-Gruneisen", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"TB-SMA", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Murnaghan", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"Poirier-Tarantola", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"Morse potential", None))

        self.moreinfo.setText(QCoreApplication.translate("MainWindow", u"\u24d8", None))
        self.pushFitEOS.setText(QCoreApplication.translate("MainWindow", u"fit parameters", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Poisson's ratio:", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"0.25", None))
        self.pushNu.setText(QCoreApplication.translate("MainWindow", u"calculate Poisson's ratio", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"electronic contribution:", None))
        self.lineEdit_el.setText(QCoreApplication.translate("MainWindow", u"0, 0, 0, 0", None))
        self.pushDoscar.setText(QCoreApplication.translate("MainWindow", u"calculate parameters", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"mono-vacancies:", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"intrinsic anh.:", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"explicit anh.:", None))
        self.lineEdit_def.setText(QCoreApplication.translate("MainWindow", u"100, 1, 1000, 0.1", None))
        self.lineEdit_anh.setText(QCoreApplication.translate("MainWindow", u"0, 1", None))
        self.lineEdit_xs.setText(QCoreApplication.translate("MainWindow", u"0, 0, 0", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"excess polynomial", None))
        self.lineEdit_xspol.setText(QCoreApplication.translate("MainWindow", u"0,0,0,0", None))
        self.label_T.setText(QCoreApplication.translate("MainWindow", u"T:", None))
        self.lineEdit_T.setText(QCoreApplication.translate("MainWindow", u"0.1 1000 50", None))
        self.label_T_2.setText(QCoreApplication.translate("MainWindow", u"K", None))
        self.label_P.setText(QCoreApplication.translate("MainWindow", u"P:", None))
        self.lineEdit_P.setText(QCoreApplication.translate("MainWindow", u"0 30 10", None))
        self.label_P_2.setText(QCoreApplication.translate("MainWindow", u"GPa", None))
        self.pushgoback.setText(QCoreApplication.translate("MainWindow", u"< go back", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"run >", None))
    # retranslateUi


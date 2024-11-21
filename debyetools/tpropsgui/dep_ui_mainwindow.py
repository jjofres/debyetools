# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

from debyetools.tpropsgui.custom_widgets import ClickableLineEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(519, 674)
        self.actionE_V = QAction(MainWindow)
        self.actionE_V.setObjectName(u"actionE_V")
        self.actionasasas = QAction(MainWindow)
        self.actionasasas.setObjectName(u"actionasasas")
        self.actionEV = QAction(MainWindow)
        self.actionEV.setObjectName(u"actionEV")
        self.actionSUMMARY = QAction(MainWindow)
        self.actionSUMMARY.setObjectName(u"actionSUMMARY")
        self.actionOUTCAR = QAction(MainWindow)
        self.actionOUTCAR.setObjectName(u"actionOUTCAR")
        self.actionDOSCAR = QAction(MainWindow)
        self.actionDOSCAR.setObjectName(u"actionDOSCAR")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_17 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit_11 = ClickableLineEdit(self.centralwidget)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
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

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_24 = QLabel(self.centralwidget)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout.addWidget(self.label_24)


        self.verticalLayout_17.addLayout(self.horizontalLayout)

        self.frame_6 = QFrame(self.centralwidget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Box)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_6)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label_2 = QLabel(self.frame_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.EvVText = QPlainTextEdit(self.frame_6)
        self.EvVText.setObjectName(u"EvVText")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EvVText.sizePolicy().hasHeightForWidth())
        self.EvVText.setSizePolicy(sizePolicy)
        self.EvVText.setMinimumSize(QSize(0, 100))

        self.horizontalLayout_2.addWidget(self.EvVText)

        self.frame_5 = QFrame(self.frame_6)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Plain)
        self.radioButton = QRadioButton(self.frame_5)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setEnabled(True)
        self.radioButton.setGeometry(QRect(10, 20, 151, 22))
        self.radioButton.setChecked(True)
        self.radioButton_3 = QRadioButton(self.frame_5)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setEnabled(True)
        self.radioButton_3.setGeometry(QRect(10, 40, 151, 22))
        self.radioButton_3.setChecked(False)
        self.label_6 = QLabel(self.frame_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 0, 31, 16))

        self.horizontalLayout_2.addWidget(self.frame_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.label_5 = QLabel(self.frame_6)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.lineEdit_2 = QLineEdit(self.frame_6)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_4.addWidget(self.lineEdit_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.frame_6)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMinimumSize(QSize(0, 25))

        self.verticalLayout_2.addWidget(self.pushButton)

        self.progress_2 = QProgressBar(self.frame_6)
        self.progress_2.setObjectName(u"progress_2")
        self.progress_2.setMaximumSize(QSize(16777215, 2))
        self.progress_2.setValue(0)
        self.progress_2.setTextVisible(False)
        self.progress_2.setInvertedAppearance(False)

        self.verticalLayout_2.addWidget(self.progress_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.comboBox = QComboBox(self.frame_6)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_4.addWidget(self.comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_17.addWidget(self.frame_6)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.elastic_constants = QTextEdit(self.frame)
        self.elastic_constants.setObjectName(u"elastic_constants")
        self.elastic_constants.setMinimumSize(QSize(120, 0))

        self.verticalLayout_3.addWidget(self.elastic_constants)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setSpacing(2)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 22))
        self.label_9.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_13.addWidget(self.label_9)

        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 22))
        self.label_10.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_13.addWidget(self.label_10)

        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 22))
        self.label_11.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_13.addWidget(self.label_11)

        self.label_15 = QLabel(self.frame)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 22))
        self.label_15.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_13.addWidget(self.label_15)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer)


        self.horizontalLayout_5.addLayout(self.verticalLayout_13)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_5 = QLineEdit(self.frame)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(0, 22))
        self.lineEdit_5.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_5.addWidget(self.lineEdit_5)

        self.lineEdit_4 = QLineEdit(self.frame)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(0, 22))
        self.lineEdit_4.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_5.addWidget(self.lineEdit_4)

        self.lineEdit_6 = QLineEdit(self.frame)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMinimumSize(QSize(0, 22))
        self.lineEdit_6.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_5.addWidget(self.lineEdit_6)

        self.lineEdit_10 = QLineEdit(self.frame)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setMinimumSize(QSize(0, 22))
        self.lineEdit_10.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_5.addWidget(self.lineEdit_10)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.frame)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(0, 22))
        self.label_20.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_11.addWidget(self.label_20)

        self.label_23 = QLabel(self.frame)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(0, 22))
        self.label_23.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_11.addWidget(self.label_23)

        self.label_22 = QLabel(self.frame)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(0, 22))
        self.label_22.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_11.addWidget(self.label_22)

        self.label_21 = QLabel(self.frame)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(0, 22))
        self.label_21.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_11.addWidget(self.label_21)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_3)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.frame)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 22))
        self.label_12.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_7.addWidget(self.label_12)

        self.label_13 = QLabel(self.frame)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 22))
        self.label_13.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_7.addWidget(self.label_13)

        self.label_14 = QLabel(self.frame)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 22))
        self.label_14.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_7.addWidget(self.label_14)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 22))
        self.label_8.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_7.addWidget(self.label_8)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_9 = QLineEdit(self.frame)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setMinimumSize(QSize(0, 22))
        self.lineEdit_9.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_10.addWidget(self.lineEdit_9)

        self.lineEdit_8 = QLineEdit(self.frame)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setMinimumSize(QSize(0, 22))
        self.lineEdit_8.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_10.addWidget(self.lineEdit_8)

        self.lineEdit_7 = QLineEdit(self.frame)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setMinimumSize(QSize(0, 22))
        self.lineEdit_7.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_10.addWidget(self.lineEdit_7)

        self.lineEdit_3 = QLineEdit(self.frame)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(0, 22))
        self.lineEdit_3.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_10.addWidget(self.lineEdit_3)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_5)


        self.horizontalLayout_5.addLayout(self.verticalLayout_10)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_16 = QLabel(self.frame)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 22))
        self.label_16.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_6.addWidget(self.label_16)

        self.label_17 = QLabel(self.frame)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(0, 22))
        self.label_17.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_6.addWidget(self.label_17)

        self.label_18 = QLabel(self.frame)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(0, 22))
        self.label_18.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_6.addWidget(self.label_18)

        self.label_19 = QLabel(self.frame)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(0, 22))
        self.label_19.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_6.addWidget(self.label_19)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_6)


        self.horizontalLayout_5.addLayout(self.verticalLayout_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 2, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_7.addWidget(self.pushButton_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_6.addLayout(self.verticalLayout_4)


        self.verticalLayout_12.addLayout(self.horizontalLayout_6)


        self.verticalLayout_17.addWidget(self.frame)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.checkBox = QCheckBox(self.frame_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.horizontalLayout_8.addWidget(self.checkBox)

        self.lineEdit_el = QLineEdit(self.frame_2)
        self.lineEdit_el.setObjectName(u"lineEdit_el")

        self.horizontalLayout_8.addWidget(self.lineEdit_el)

        self.pushButton_3 = QPushButton(self.frame_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_8.addWidget(self.pushButton_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.verticalLayout_17.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_3)
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

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)


        self.verticalLayout_17.addWidget(self.frame_3)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)

        self.verticalLayout_TP = QVBoxLayout()
        self.verticalLayout_TP.setSpacing(0)
        self.verticalLayout_TP.setObjectName(u"verticalLayout_TP")
        self.verticalLayout_TP.setContentsMargins(0, -1, -1, -1)
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


        self.verticalLayout_TP.addLayout(self.horizontalLayout_P)


        self.horizontalLayout_10.addLayout(self.verticalLayout_TP)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

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


        self.verticalLayout_17.addLayout(self.horizontalLayout_10)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 519, 21))
        self.menuplot = QMenu(self.menubar)
        self.menuplot.setObjectName(u"menuplot")
        self.menuload_data = QMenu(self.menubar)
        self.menuload_data.setObjectName(u"menuload_data")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuplot.menuAction())
        self.menubar.addAction(self.menuload_data.menuAction())
        self.menuplot.addAction(self.actionEV)
        self.menuload_data.addAction(self.actionSUMMARY)
        self.menuload_data.addAction(self.actionOUTCAR)
        self.menuload_data.addAction(self.actionDOSCAR)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"debyetools GUI", None))
        self.actionE_V.setText(QCoreApplication.translate("MainWindow", u"Exxx", None))
        self.actionasasas.setText(QCoreApplication.translate("MainWindow", u"asasas", None))
        self.actionEV.setText(QCoreApplication.translate("MainWindow", u"E(V)", None))
        self.actionSUMMARY.setText(QCoreApplication.translate("MainWindow", u"Energy curve (SUMMARY)", None))
        self.actionOUTCAR.setText(QCoreApplication.translate("MainWindow", u"Elastic constants (OUTCAR)", None))
        self.actionDOSCAR.setText(QCoreApplication.translate("MainWindow", u"eDOS (DOSCAR.i)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"formula:", None))
        self.lineEdit_11.setText(QCoreApplication.translate("MainWindow", u"Al4", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"mass:", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"0.02698", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"kg/mol-at", None))
        self.label_25.setText("")
        self.label_24.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"E(V):", None))
        self.EvVText.setPlainText(QCoreApplication.translate("MainWindow", u"#V	E\n"
"1.201468E+01	-3.210751E+00\n"
"1.241964E+01	-3.326448E+00\n"
"1.283359E+01	-3.424838E+00\n"
"1.325664E+01	-3.507320E+00\n"
"1.368889E+01	-3.575208E+00\n"
"1.413044E+01	-3.629742E+00\n"
"1.458137E+01	-3.672073E+00\n"
"1.504180E+01	-3.703298E+00\n"
"1.551183E+01	-3.724441E+00\n"
"1.599154E+01	-3.736464E+00\n"
"1.648104E+01	-3.740270E+00\n"
"1.698044E+01	-3.736691E+00\n"
"1.748982E+01	-3.726524E+00\n"
"1.800928E+01	-3.710495E+00\n"
"1.853893E+01	-3.689294E+00\n"
"1.907887E+01	-3.663562E+00\n"
"1.962919E+01	-3.633908E+00\n"
"2.018999E+01	-3.600914E+00\n"
"2.076137E+01	-3.565133E+00\n"
"2.134343E+01	-3.527076E+00\n"
"2.193627E+01	-3.487192E+00", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"eV and A^3 (per at)", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u" J and m^3 (per mol-at)", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"units:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"EOS params:", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"-3e5, 1e-5, 7e10, 4", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"fit", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Birch-Murnaghan", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Rose-Vinet", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Mie-Gruneisen", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"TB-SMA", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Murnaghan", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"Poirier-Tarantola", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"EAM int. potential", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"Morse int. potential", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Stiffness Tensor (GPa):", None))
        self.elastic_constants.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">97  69  69  0   0   0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">69  97  69  0   0   0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">69  69  97  0   0   0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-r"
                        "ight:0px; -qt-block-indent:0; text-indent:0px;\">0   0   0   45  0   0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0   0   0   0   45  0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0   0   0   0   0   45</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"B (Voigt):", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"B (Reuss):", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"B (Voigt-Reuss-Hill): ", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Universal anisotrpy:", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"79", None))
        self.lineEdit_4.setText(QCoreApplication.translate("MainWindow", u"78", None))
        self.lineEdit_6.setText(QCoreApplication.translate("MainWindow", u"78", None))
        self.lineEdit_10.setText(QCoreApplication.translate("MainWindow", u"1.8", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"GPa   ", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"GPa   ", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"GPa   ", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"GPa   ", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"S (Voigt):", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"S (Reuss):", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"S (Voigt-Reuss-Hill): ", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Poisson's ratio:", None))
        self.lineEdit_9.setText(QCoreApplication.translate("MainWindow", u"24", None))
        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u"33", None))
        self.lineEdit_7.setText(QCoreApplication.translate("MainWindow", u"28", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"0.34", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"GPa", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"GPa", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"GPa", None))
        self.label_19.setText("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"re-calculate Poisson's ratio", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"electronic contribution:", None))
        self.lineEdit_el.setText(QCoreApplication.translate("MainWindow", u"0, 0, 0, 0", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"calculate", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"mono-vacancies:", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"explicit anh.:", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"excess:", None))
        self.lineEdit_def.setText(QCoreApplication.translate("MainWindow", u"100, 1, 1000, 0.1", None))
        self.lineEdit_anh.setText(QCoreApplication.translate("MainWindow", u"0, 1", None))
        self.lineEdit_xs.setText(QCoreApplication.translate("MainWindow", u"0, 0, 0", None))
        self.label_T.setText(QCoreApplication.translate("MainWindow", u"T: ", None))
        self.lineEdit_T.setText(QCoreApplication.translate("MainWindow", u"0.1 1000 50", None))
        self.label_P.setText(QCoreApplication.translate("MainWindow", u"P: ", None))
        self.lineEdit_P.setText(QCoreApplication.translate("MainWindow", u"0 30 10", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"calculate", None))
        self.menuplot.setTitle(QCoreApplication.translate("MainWindow", u"plot", None))
        self.menuload_data.setTitle(QCoreApplication.translate("MainWindow", u"load data", None))
    # retranslateUi


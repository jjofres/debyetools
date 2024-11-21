# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_calculateNu.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModality.WindowModal)
        Form.resize(636, 190)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.elastic_constants = QTextEdit(Form)
        self.elastic_constants.setObjectName(u"elastic_constants")
        self.elastic_constants.setMinimumSize(QSize(200, 0))

        self.verticalLayout_3.addWidget(self.elastic_constants)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setSpacing(2)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 22))
        self.label_9.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_13.addWidget(self.label_9)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 22))
        self.label_10.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_13.addWidget(self.label_10)

        self.label_11 = QLabel(Form)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 22))
        self.label_11.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_13.addWidget(self.label_11)

        self.label_15 = QLabel(Form)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 22))
        self.label_15.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_13.addWidget(self.label_15)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer)


        self.horizontalLayout_5.addLayout(self.verticalLayout_13)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_5 = QLineEdit(Form)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(0, 22))
        self.lineEdit_5.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_5.addWidget(self.lineEdit_5)

        self.lineEdit_4 = QLineEdit(Form)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(0, 22))
        self.lineEdit_4.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_5.addWidget(self.lineEdit_4)

        self.lineEdit_6 = QLineEdit(Form)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMinimumSize(QSize(0, 22))
        self.lineEdit_6.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_5.addWidget(self.lineEdit_6)

        self.lineEdit_10 = QLineEdit(Form)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setMinimumSize(QSize(0, 22))
        self.lineEdit_10.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_5.addWidget(self.lineEdit_10)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(Form)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(0, 22))
        self.label_20.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_11.addWidget(self.label_20)

        self.label_23 = QLabel(Form)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(0, 22))
        self.label_23.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_11.addWidget(self.label_23)

        self.label_22 = QLabel(Form)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(0, 22))
        self.label_22.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_11.addWidget(self.label_22)

        self.label_21 = QLabel(Form)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(0, 22))
        self.label_21.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_11.addWidget(self.label_21)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_3)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(Form)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 22))
        self.label_12.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_7.addWidget(self.label_12)

        self.label_13 = QLabel(Form)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 22))
        self.label_13.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_7.addWidget(self.label_13)

        self.label_14 = QLabel(Form)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 22))
        self.label_14.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_7.addWidget(self.label_14)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 22))
        self.label_8.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_7.addWidget(self.label_8)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_9 = QLineEdit(Form)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setMinimumSize(QSize(0, 22))
        self.lineEdit_9.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_10.addWidget(self.lineEdit_9)

        self.lineEdit_8 = QLineEdit(Form)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setMinimumSize(QSize(0, 22))
        self.lineEdit_8.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_10.addWidget(self.lineEdit_8)

        self.lineEdit_7 = QLineEdit(Form)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setMinimumSize(QSize(0, 22))
        self.lineEdit_7.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_10.addWidget(self.lineEdit_7)

        self.lineEdit_3 = QLineEdit(Form)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(0, 22))
        self.lineEdit_3.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_10.addWidget(self.lineEdit_3)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_5)


        self.horizontalLayout_5.addLayout(self.verticalLayout_10)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_16 = QLabel(Form)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 22))
        self.label_16.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_6.addWidget(self.label_16)

        self.label_17 = QLabel(Form)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(0, 22))
        self.label_17.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_6.addWidget(self.label_17)

        self.label_18 = QLabel(Form)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(0, 22))
        self.label_18.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_6.addWidget(self.label_18)

        self.label_19 = QLabel(Form)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(0, 22))
        self.label_19.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_6.addWidget(self.label_19)

        self.pushMore = QPushButton(Form)
        self.pushMore.setObjectName(u"pushMore")

        self.verticalLayout_6.addWidget(self.pushMore)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_6)


        self.horizontalLayout_5.addLayout(self.verticalLayout_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 2, 0)
        self.pushLoadElastic = QPushButton(Form)
        self.pushLoadElastic.setObjectName(u"pushLoadElastic")

        self.horizontalLayout_7.addWidget(self.pushLoadElastic)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_7.addWidget(self.pushButton_2)

        self.pushSave = QPushButton(Form)
        self.pushSave.setObjectName(u"pushSave")

        self.horizontalLayout_7.addWidget(self.pushSave)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_6.addLayout(self.verticalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"debyetools - [elastic properties]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Stiffness Tensor (GPa):", None))
        self.elastic_constants.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Form", u"Average properties:", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"B (Voigt):", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"B (Reuss):", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"B (Voigt-Reuss-Hill):", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Universal anisotrpy:", None))
        self.lineEdit_5.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_10.setText("")
        self.label_20.setText(QCoreApplication.translate("Form", u"GPa", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"GPa", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"GPa", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"GPa", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"S (Voigt):", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"S (Reuss):", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"S (Voigt-Reuss-Hill):", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Poisson's ratio:", None))
        self.lineEdit_9.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_3.setText("")
        self.label_16.setText(QCoreApplication.translate("Form", u"GPa", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"GPa", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"GPa", None))
        self.label_19.setText("")
        self.pushMore.setText(QCoreApplication.translate("Form", u"More...", None))
        self.pushLoadElastic.setText(QCoreApplication.translate("Form", u"Load tensor...", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Calculate", None))
        self.pushSave.setText(QCoreApplication.translate("Form", u"Save and Close", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialogSUMMARY.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 183)
        self.summarypath = QLineEdit(Dialog)
        self.summarypath.setObjectName(u"summarypath")
        self.summarypath.setGeometry(QRect(110, 30, 271, 24))
        self.ok = QPushButton(Dialog)
        self.ok.setObjectName(u"ok")
        self.ok.setGeometry(QRect(300, 150, 80, 24))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 130, 241, 71))
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.browsesummary = QPushButton(Dialog)
        self.browsesummary.setObjectName(u"browsesummary")
        self.browsesummary.setGeometry(QRect(20, 30, 80, 24))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 111, 16))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 60, 111, 16))
        self.browseposcar = QPushButton(Dialog)
        self.browseposcar.setObjectName(u"browseposcar")
        self.browseposcar.setGeometry(QRect(20, 80, 80, 24))
        self.poscarpath = QLineEdit(Dialog)
        self.poscarpath.setObjectName(u"poscarpath")
        self.poscarpath.setGeometry(QRect(110, 80, 271, 24))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Enter path for Eneergy curve and crystal structure...", None))
        self.summarypath.setText(QCoreApplication.translate("Dialog", u"./SUMMARY", None))
        self.ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Note: along with the SUMMARY file is important to include a POSCAR file to calculate the volumes.", None))
        self.browsesummary.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"SUMMARY:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"POSCAR:", None))
        self.browseposcar.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.poscarpath.setText(QCoreApplication.translate("Dialog", u"./POSCAR", None))
    # retranslateUi


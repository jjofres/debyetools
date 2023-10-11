# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialogOUTCAR.ui'
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
        Dialog.resize(400, 99)
        self.ok = QPushButton(Dialog)
        self.ok.setObjectName(u"ok")
        self.ok.setGeometry(QRect(300, 70, 80, 24))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 111, 16))
        self.browseoutcar = QPushButton(Dialog)
        self.browseoutcar.setObjectName(u"browseoutcar")
        self.browseoutcar.setGeometry(QRect(20, 30, 80, 24))
        self.outcarpath = QLineEdit(Dialog)
        self.outcarpath.setObjectName(u"outcarpath")
        self.outcarpath.setGeometry(QRect(110, 30, 271, 24))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Enter path for Elastic constants...", None))
        self.ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"OUTCAR:", None))
        self.browseoutcar.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.outcarpath.setText(QCoreApplication.translate("Dialog", u"./OUTCAR", None))
    # retranslateUi


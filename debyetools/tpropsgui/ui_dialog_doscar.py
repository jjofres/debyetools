# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_DOSCAR.ui'
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
        Dialog.resize(400, 115)
        self.browse = QPushButton(Dialog)
        self.browse.setObjectName(u"browse")
        self.browse.setGeometry(QRect(20, 10, 80, 24))
        self.filepath = QLineEdit(Dialog)
        self.filepath.setObjectName(u"filepath")
        self.filepath.setGeometry(QRect(110, 10, 271, 24))
        self.ok = QPushButton(Dialog)
        self.ok.setObjectName(u"ok")
        self.ok.setGeometry(QRect(300, 40, 80, 24))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 40, 241, 71))
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2.setWordWrap(True)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Select folder where the \"DOSCAR.i\" files are...", None))
        self.browse.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.filepath.setText(QCoreApplication.translate("Dialog", u".", None))
        self.ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Note: DOSCAR files must be placed in the same folder and named \"DOSCAR.i\", where \"i\" is an integer from 1 to the number of points in the E(V) data. ", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_plots_elastic.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(600, 820)
        Dialog.setMinimumSize(QSize(600, 820))
        Dialog.setMaximumSize(QSize(600, 820))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.label_5)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.label)

        self.hLplots1 = QHBoxLayout()
        self.hLplots1.setObjectName(u"hLplots1")

        self.verticalLayout.addLayout(self.hLplots1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.label_2)

        self.hLplots2 = QHBoxLayout()
        self.hLplots2.setObjectName(u"hLplots2")

        self.verticalLayout.addLayout(self.hLplots2)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.label_3)

        self.hLplots3 = QHBoxLayout()
        self.hLplots3.setObjectName(u"hLplots3")

        self.verticalLayout.addLayout(self.hLplots3)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.label_4)

        self.hLplots4 = QHBoxLayout()
        self.hLplots4.setObjectName(u"hLplots4")

        self.verticalLayout.addLayout(self.hLplots4)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Variations of the elastic moduli:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Young's modulus", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Linear compresibiliy", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Shear modulus", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Poisson's ratio", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_loadEOS.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(400, 194)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.summarypath = QLineEdit(Dialog)
        self.summarypath.setObjectName(u"summarypath")

        self.horizontalLayout.addWidget(self.summarypath)

        self.browsesummary = QPushButton(Dialog)
        self.browsesummary.setObjectName(u"browsesummary")

        self.horizontalLayout.addWidget(self.browsesummary)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 30))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2.setWordWrap(True)

        self.horizontalLayout_6.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.poscarpath = QLineEdit(Dialog)
        self.poscarpath.setObjectName(u"poscarpath")

        self.horizontalLayout_2.addWidget(self.poscarpath)

        self.browseposcar = QPushButton(Dialog)
        self.browseposcar.setObjectName(u"browseposcar")

        self.horizontalLayout_2.addWidget(self.browseposcar)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.ok = QPushButton(Dialog)
        self.ok.setObjectName(u"ok")

        self.horizontalLayout_3.addWidget(self.ok)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"debyetools - [load energies and structure...]", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"SUMMARY:", None))
        self.summarypath.setText(QCoreApplication.translate("Dialog", u"./SUMMARY", None))
        self.browsesummary.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Note: along with the SUMMARY file is important to include a POSCAR file to calculate the volumes.", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"POSCAR:", None))
        self.poscarpath.setText(QCoreApplication.translate("Dialog", u"./POSCAR", None))
        self.browseposcar.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi


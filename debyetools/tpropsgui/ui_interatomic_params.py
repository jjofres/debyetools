# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interatomic_params.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(796, 395)
        self.horizontalLayoutWidget = QWidget(Form)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(280, 10, 241, 241))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 290, 49, 21))
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 320, 161, 21))
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(140, 290, 91, 24))
        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(140, 320, 91, 24))
        self.plainTextEdit = QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setGeometry(QRect(530, 10, 261, 241))
        palette = QPalette()
        self.plainTextEdit.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Cascadia Mono"])
        font.setPointSize(8)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setFrameShape(QFrame.Box)
        self.plainTextEdit.setTabChangesFocus(False)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setCenterOnScroll(False)
        self.OKbutton = QPushButton(Form)
        self.OKbutton.setObjectName(u"OKbutton")
        self.OKbutton.setGeometry(QRect(680, 340, 80, 24))
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(590, 340, 71, 24))
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 31, 16))
        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget.rowCount() < 3):
            self.tableWidget.setRowCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setItem(1, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setItem(1, 2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setItem(2, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setItem(2, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setItem(2, 2, __qtablewidgetitem14)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 30, 171, 81))
        self.tableWidget.setFrameShape(QFrame.Box)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget.verticalHeader().setDefaultSectionSize(25)
        self.tableWidget_2 = QTableWidget(Form)
        if (self.tableWidget_2.columnCount() < 4):
            self.tableWidget_2.setColumnCount(4)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        if (self.tableWidget_2.rowCount() < 10):
            self.tableWidget_2.setRowCount(10)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(5, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(6, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(7, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(8, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(9, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget_2.setItem(0, 0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableWidget_2.setItem(0, 1, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableWidget_2.setItem(0, 2, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableWidget_2.setItem(0, 3, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableWidget_2.setItem(1, 0, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableWidget_2.setItem(1, 1, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableWidget_2.setItem(1, 2, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableWidget_2.setItem(1, 3, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableWidget_2.setItem(2, 0, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableWidget_2.setItem(2, 1, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableWidget_2.setItem(2, 2, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tableWidget_2.setItem(2, 3, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableWidget_2.setItem(3, 0, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tableWidget_2.setItem(3, 1, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableWidget_2.setItem(3, 2, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tableWidget_2.setItem(3, 3, __qtablewidgetitem44)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setGeometry(QRect(10, 130, 231, 131))
        self.tableWidget_2.setFrameShape(QFrame.Box)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(40)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(25)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 110, 31, 16))
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 350, 161, 21))
        self.lineEdit_3 = QLineEdit(Form)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(140, 350, 91, 24))
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(240, 290, 49, 21))
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(240, 350, 71, 21))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"input interatomic potential parameters...", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"cutoff:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"# of nearest neighbors:", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"5", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Form", u"3", None))
        self.OKbutton.setText(QCoreApplication.translate("Form", u"Close", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.label.setText(QCoreApplication.translate("Form", u"cell:", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"New Column", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"New Column", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"New Column", None));
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"x", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"y", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"z", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem6 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"4.04", None));
        ___qtablewidgetitem7 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem8 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem9 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem10 = self.tableWidget.item(1, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"4.04", None));
        ___qtablewidgetitem11 = self.tableWidget.item(1, 2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem12 = self.tableWidget.item(2, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem13 = self.tableWidget.item(2, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem14 = self.tableWidget.item(2, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Form", u"4.04", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        ___qtablewidgetitem15 = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Form", u"x", None));
        ___qtablewidgetitem16 = self.tableWidget_2.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Form", u"y", None));
        ___qtablewidgetitem17 = self.tableWidget_2.horizontalHeaderItem(2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Form", u"z", None));
        ___qtablewidgetitem18 = self.tableWidget_2.horizontalHeaderItem(3)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Form", u"type", None));
        ___qtablewidgetitem19 = self.tableWidget_2.verticalHeaderItem(0)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Form", u"atom 1", None));
        ___qtablewidgetitem20 = self.tableWidget_2.verticalHeaderItem(1)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Form", u"atom 2", None));
        ___qtablewidgetitem21 = self.tableWidget_2.verticalHeaderItem(2)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("Form", u"atom 3", None));
        ___qtablewidgetitem22 = self.tableWidget_2.verticalHeaderItem(3)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("Form", u"atom 4", None));
        ___qtablewidgetitem23 = self.tableWidget_2.verticalHeaderItem(4)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("Form", u"atom 5", None));
        ___qtablewidgetitem24 = self.tableWidget_2.verticalHeaderItem(5)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("Form", u"atom 6", None));
        ___qtablewidgetitem25 = self.tableWidget_2.verticalHeaderItem(6)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("Form", u"atom 7", None));
        ___qtablewidgetitem26 = self.tableWidget_2.verticalHeaderItem(7)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("Form", u"atom 8", None));
        ___qtablewidgetitem27 = self.tableWidget_2.verticalHeaderItem(8)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("Form", u"atom 9", None));
        ___qtablewidgetitem28 = self.tableWidget_2.verticalHeaderItem(9)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("Form", u"atom 10", None));

        __sortingEnabled1 = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        ___qtablewidgetitem29 = self.tableWidget_2.item(0, 0)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem30 = self.tableWidget_2.item(0, 1)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem31 = self.tableWidget_2.item(0, 2)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem32 = self.tableWidget_2.item(0, 3)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("Form", u"Al", None));
        ___qtablewidgetitem33 = self.tableWidget_2.item(1, 0)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem34 = self.tableWidget_2.item(1, 1)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem35 = self.tableWidget_2.item(1, 2)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem36 = self.tableWidget_2.item(1, 3)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("Form", u"Al", None));
        ___qtablewidgetitem37 = self.tableWidget_2.item(2, 0)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem38 = self.tableWidget_2.item(2, 1)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem39 = self.tableWidget_2.item(2, 2)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem40 = self.tableWidget_2.item(2, 3)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("Form", u"Al", None));
        ___qtablewidgetitem41 = self.tableWidget_2.item(3, 0)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem42 = self.tableWidget_2.item(3, 1)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem43 = self.tableWidget_2.item(3, 2)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem44 = self.tableWidget_2.item(3, 3)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("Form", u"Al", None));
        self.tableWidget_2.setSortingEnabled(__sortingEnabled1)

        self.label_2.setText(QCoreApplication.translate("Form", u"basis:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"parameters initial guess:", None))
        self.lineEdit_3.setText("")
        self.label_6.setText(QCoreApplication.translate("Form", u"[A]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"(D, alpha, r0)", None))
    # retranslateUi


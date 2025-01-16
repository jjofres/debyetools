# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_crystal.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModality.WindowModal)
        Form.resize(779, 422)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tableCell = QTableWidget(Form)
        if (self.tableCell.columnCount() < 3):
            self.tableCell.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableCell.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableCell.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableCell.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableCell.rowCount() < 3):
            self.tableCell.setRowCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableCell.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableCell.setVerticalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableCell.setVerticalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableCell.setItem(0, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableCell.setItem(0, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableCell.setItem(0, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableCell.setItem(1, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableCell.setItem(1, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableCell.setItem(1, 2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableCell.setItem(2, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableCell.setItem(2, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableCell.setItem(2, 2, __qtablewidgetitem14)
        self.tableCell.setObjectName(u"tableCell")
        self.tableCell.setMinimumSize(QSize(165, 100))
        self.tableCell.setMaximumSize(QSize(165, 100))
        self.tableCell.setFrameShape(QFrame.Shape.Box)
        self.tableCell.horizontalHeader().setVisible(False)
        self.tableCell.horizontalHeader().setDefaultSectionSize(50)
        self.tableCell.verticalHeader().setDefaultSectionSize(25)

        self.verticalLayout.addWidget(self.tableCell)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.tableBasis = QTableWidget(Form)
        if (self.tableBasis.columnCount() < 4):
            self.tableBasis.setColumnCount(4)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableBasis.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableBasis.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableBasis.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableBasis.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        if (self.tableBasis.rowCount() < 10):
            self.tableBasis.setRowCount(10)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(0, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(1, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(2, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(3, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(4, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(5, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(6, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(7, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(8, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableBasis.setVerticalHeaderItem(9, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableBasis.setItem(0, 0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableBasis.setItem(0, 1, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableBasis.setItem(0, 2, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableBasis.setItem(0, 3, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableBasis.setItem(1, 0, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableBasis.setItem(1, 1, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableBasis.setItem(1, 2, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableBasis.setItem(1, 3, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableBasis.setItem(2, 0, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableBasis.setItem(2, 1, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableBasis.setItem(2, 2, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tableBasis.setItem(2, 3, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableBasis.setItem(3, 0, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tableBasis.setItem(3, 1, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableBasis.setItem(3, 2, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tableBasis.setItem(3, 3, __qtablewidgetitem44)
        self.tableBasis.setObjectName(u"tableBasis")
        self.tableBasis.setMaximumSize(QSize(250, 200))
        self.tableBasis.setFrameShape(QFrame.Shape.Box)
        self.tableBasis.horizontalHeader().setDefaultSectionSize(40)
        self.tableBasis.verticalHeader().setDefaultSectionSize(25)

        self.verticalLayout.addWidget(self.tableBasis)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 5, -1, 5)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.lineEditCutoff = QLineEdit(Form)
        self.lineEditCutoff.setObjectName(u"lineEditCutoff")
        self.lineEditCutoff.setMaximumSize(QSize(70, 16777215))

        self.verticalLayout_3.addWidget(self.lineEditCutoff)

        self.lineEditNnn = QLineEdit(Form)
        self.lineEditNnn.setObjectName(u"lineEditNnn")
        self.lineEditNnn.setMaximumSize(QSize(70, 16777215))

        self.verticalLayout_3.addWidget(self.lineEditNnn)

        self.lineEditInitialGuess = QLineEdit(Form)
        self.lineEditInitialGuess.setObjectName(u"lineEditInitialGuess")
        self.lineEditInitialGuess.setMaximumSize(QSize(70, 16777215))

        self.verticalLayout_3.addWidget(self.lineEditInitialGuess)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_4.addWidget(self.label_7)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_4.addWidget(self.label_6)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_4.addWidget(self.label_8)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_xxxx = QHBoxLayout()
        self.horizontalLayout_xxxx.setObjectName(u"horizontalLayout_xxxx")
        self.horizontalLayout_xxxx.setContentsMargins(10, 10, 10, -1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout_xxxx)

        self.plainPairAnalysis = QPlainTextEdit(Form)
        self.plainPairAnalysis.setObjectName(u"plainPairAnalysis")
        self.plainPairAnalysis.setEnabled(True)
        self.plainPairAnalysis.setMinimumSize(QSize(150, 150))
        self.plainPairAnalysis.setMaximumSize(QSize(175, 400))
        palette = QPalette()
        self.plainPairAnalysis.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Cascadia Mono"])
        font.setPointSize(8)
        self.plainPairAnalysis.setFont(font)
        self.plainPairAnalysis.setFrameShape(QFrame.Shape.Box)
        self.plainPairAnalysis.setTabChangesFocus(False)
        self.plainPairAnalysis.setReadOnly(True)
        self.plainPairAnalysis.setBackgroundVisible(False)
        self.plainPairAnalysis.setCenterOnScroll(False)

        self.horizontalLayout_2.addWidget(self.plainPairAnalysis)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setEnabled(False)

        self.verticalLayout_5.addWidget(self.label_10)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.pushBack = QPushButton(Form)
        self.pushBack.setObjectName(u"pushBack")

        self.horizontalLayout_4.addWidget(self.pushBack)

        self.pushUpdate = QPushButton(Form)
        self.pushUpdate.setObjectName(u"pushUpdate")

        self.horizontalLayout_4.addWidget(self.pushUpdate)

        self.pushNext = QPushButton(Form)
        self.pushNext.setObjectName(u"pushNext")

        self.horizontalLayout_4.addWidget(self.pushNext)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.horizontalLayout.addLayout(self.verticalLayout_5)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"debyetools - [crystal structure]", None))
        self.label.setText(QCoreApplication.translate("Form", u"cell:", None))
        ___qtablewidgetitem = self.tableCell.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"New Column", None));
        ___qtablewidgetitem1 = self.tableCell.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"New Column", None));
        ___qtablewidgetitem2 = self.tableCell.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"New Column", None));
        ___qtablewidgetitem3 = self.tableCell.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"x", None));
        ___qtablewidgetitem4 = self.tableCell.verticalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"y", None));
        ___qtablewidgetitem5 = self.tableCell.verticalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"z", None));

        __sortingEnabled = self.tableCell.isSortingEnabled()
        self.tableCell.setSortingEnabled(False)
        ___qtablewidgetitem6 = self.tableCell.item(0, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"4.04", None));
        ___qtablewidgetitem7 = self.tableCell.item(0, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem8 = self.tableCell.item(0, 2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem9 = self.tableCell.item(1, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem10 = self.tableCell.item(1, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"4.04", None));
        ___qtablewidgetitem11 = self.tableCell.item(1, 2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem12 = self.tableCell.item(2, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem13 = self.tableCell.item(2, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Form", u"0.0", None));
        ___qtablewidgetitem14 = self.tableCell.item(2, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Form", u"4.04", None));
        self.tableCell.setSortingEnabled(__sortingEnabled)

        self.label_2.setText(QCoreApplication.translate("Form", u"basis:", None))
        ___qtablewidgetitem15 = self.tableBasis.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Form", u"x", None));
        ___qtablewidgetitem16 = self.tableBasis.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Form", u"y", None));
        ___qtablewidgetitem17 = self.tableBasis.horizontalHeaderItem(2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Form", u"z", None));
        ___qtablewidgetitem18 = self.tableBasis.horizontalHeaderItem(3)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Form", u"type", None));
        ___qtablewidgetitem19 = self.tableBasis.verticalHeaderItem(0)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Form", u"atom 1", None));
        ___qtablewidgetitem20 = self.tableBasis.verticalHeaderItem(1)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Form", u"atom 2", None));
        ___qtablewidgetitem21 = self.tableBasis.verticalHeaderItem(2)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("Form", u"atom 3", None));
        ___qtablewidgetitem22 = self.tableBasis.verticalHeaderItem(3)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("Form", u"atom 4", None));
        ___qtablewidgetitem23 = self.tableBasis.verticalHeaderItem(4)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("Form", u"atom 5", None));
        ___qtablewidgetitem24 = self.tableBasis.verticalHeaderItem(5)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("Form", u"atom 6", None));
        ___qtablewidgetitem25 = self.tableBasis.verticalHeaderItem(6)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("Form", u"atom 7", None));
        ___qtablewidgetitem26 = self.tableBasis.verticalHeaderItem(7)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("Form", u"atom 8", None));
        ___qtablewidgetitem27 = self.tableBasis.verticalHeaderItem(8)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("Form", u"atom 9", None));
        ___qtablewidgetitem28 = self.tableBasis.verticalHeaderItem(9)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("Form", u"atom 10", None));

        __sortingEnabled1 = self.tableBasis.isSortingEnabled()
        self.tableBasis.setSortingEnabled(False)
        ___qtablewidgetitem29 = self.tableBasis.item(0, 0)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem30 = self.tableBasis.item(0, 1)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem31 = self.tableBasis.item(0, 2)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem32 = self.tableBasis.item(1, 0)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem33 = self.tableBasis.item(1, 1)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem34 = self.tableBasis.item(1, 2)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem35 = self.tableBasis.item(2, 0)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem36 = self.tableBasis.item(2, 1)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem37 = self.tableBasis.item(2, 2)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem38 = self.tableBasis.item(3, 0)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("Form", u"0", None));
        ___qtablewidgetitem39 = self.tableBasis.item(3, 1)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("Form", u"0.5", None));
        ___qtablewidgetitem40 = self.tableBasis.item(3, 2)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("Form", u"0.5", None));
        self.tableBasis.setSortingEnabled(__sortingEnabled1)

        self.label_3.setText(QCoreApplication.translate("Form", u"cutoff:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"# of nearest neighbors:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"parameters initial guess:", None))
        self.lineEditCutoff.setText("")
        self.lineEditNnn.setText("")
        self.lineEditInitialGuess.setText("")
        self.label_7.setText(QCoreApplication.translate("Form", u"[A]", None))
        self.label_6.setText("")
        self.label_8.setText("")
        self.label_10.setText("")
        self.pushBack.setText(QCoreApplication.translate("Form", u"Back", None))
        self.pushUpdate.setText(QCoreApplication.translate("Form", u"Update", None))
        self.pushNext.setText(QCoreApplication.translate("Form", u"Next", None))
    # retranslateUi


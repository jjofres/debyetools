# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_periodictable.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

from debyetools.tpropsgui.custom_widgets import CountingButton

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(470, 299)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushB88 = CountingButton(Dialog)
        self.pushB88.setObjectName(u"pushB88")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushB88.sizePolicy().hasHeightForWidth())
        self.pushB88.setSizePolicy(sizePolicy)
        self.pushB88.setMinimumSize(QSize(25, 25))
        self.pushB88.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB88, 9, 3, 1, 1)

        self.pushB66 = CountingButton(Dialog)
        self.pushB66.setObjectName(u"pushB66")
        sizePolicy.setHeightForWidth(self.pushB66.sizePolicy().hasHeightForWidth())
        self.pushB66.setSizePolicy(sizePolicy)
        self.pushB66.setMinimumSize(QSize(25, 25))
        self.pushB66.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB66, 8, 13, 1, 1)

        self.pushB85 = CountingButton(Dialog)
        self.pushB85.setObjectName(u"pushB85")
        sizePolicy.setHeightForWidth(self.pushB85.sizePolicy().hasHeightForWidth())
        self.pushB85.setSizePolicy(sizePolicy)
        self.pushB85.setMinimumSize(QSize(25, 25))
        self.pushB85.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB85, 5, 18, 1, 1)

        self.pushB75 = CountingButton(Dialog)
        self.pushB75.setObjectName(u"pushB75")
        sizePolicy.setHeightForWidth(self.pushB75.sizePolicy().hasHeightForWidth())
        self.pushB75.setSizePolicy(sizePolicy)
        self.pushB75.setMinimumSize(QSize(25, 25))
        self.pushB75.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB75, 5, 8, 1, 1)

        self.pushB101 = CountingButton(Dialog)
        self.pushB101.setObjectName(u"pushB101")
        sizePolicy.setHeightForWidth(self.pushB101.sizePolicy().hasHeightForWidth())
        self.pushB101.setSizePolicy(sizePolicy)
        self.pushB101.setMinimumSize(QSize(25, 25))
        self.pushB101.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB101, 9, 16, 1, 1)

        self.pushB110 = CountingButton(Dialog)
        self.pushB110.setObjectName(u"pushB110")
        sizePolicy.setHeightForWidth(self.pushB110.sizePolicy().hasHeightForWidth())
        self.pushB110.setSizePolicy(sizePolicy)
        self.pushB110.setMinimumSize(QSize(25, 25))
        self.pushB110.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB110, 6, 11, 1, 1)

        self.pushB82 = CountingButton(Dialog)
        self.pushB82.setObjectName(u"pushB82")
        sizePolicy.setHeightForWidth(self.pushB82.sizePolicy().hasHeightForWidth())
        self.pushB82.setSizePolicy(sizePolicy)
        self.pushB82.setMinimumSize(QSize(25, 25))
        self.pushB82.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB82, 5, 15, 1, 1)

        self.pushB70 = CountingButton(Dialog)
        self.pushB70.setObjectName(u"pushB70")
        sizePolicy.setHeightForWidth(self.pushB70.sizePolicy().hasHeightForWidth())
        self.pushB70.setSizePolicy(sizePolicy)
        self.pushB70.setMinimumSize(QSize(25, 25))
        self.pushB70.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB70, 8, 17, 1, 1)

        self.pushB116 = CountingButton(Dialog)
        self.pushB116.setObjectName(u"pushB116")
        sizePolicy.setHeightForWidth(self.pushB116.sizePolicy().hasHeightForWidth())
        self.pushB116.setSizePolicy(sizePolicy)
        self.pushB116.setMinimumSize(QSize(25, 25))
        self.pushB116.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB116, 6, 17, 1, 1)

        self.pushB72 = CountingButton(Dialog)
        self.pushB72.setObjectName(u"pushB72")
        sizePolicy.setHeightForWidth(self.pushB72.sizePolicy().hasHeightForWidth())
        self.pushB72.setSizePolicy(sizePolicy)
        self.pushB72.setMinimumSize(QSize(25, 25))
        self.pushB72.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB72, 5, 5, 1, 1)

        self.pushB114 = CountingButton(Dialog)
        self.pushB114.setObjectName(u"pushB114")
        sizePolicy.setHeightForWidth(self.pushB114.sizePolicy().hasHeightForWidth())
        self.pushB114.setSizePolicy(sizePolicy)
        self.pushB114.setMinimumSize(QSize(25, 25))
        self.pushB114.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB114, 6, 15, 1, 1)

        self.pushB22 = CountingButton(Dialog)
        self.pushB22.setObjectName(u"pushB22")
        sizePolicy.setHeightForWidth(self.pushB22.sizePolicy().hasHeightForWidth())
        self.pushB22.setSizePolicy(sizePolicy)
        self.pushB22.setMinimumSize(QSize(25, 25))
        self.pushB22.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB22, 3, 5, 1, 1)

        self.pushB103 = CountingButton(Dialog)
        self.pushB103.setObjectName(u"pushB103")
        sizePolicy.setHeightForWidth(self.pushB103.sizePolicy().hasHeightForWidth())
        self.pushB103.setSizePolicy(sizePolicy)
        self.pushB103.setMinimumSize(QSize(25, 25))
        self.pushB103.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB103, 6, 4, 1, 1)

        self.pushB35 = CountingButton(Dialog)
        self.pushB35.setObjectName(u"pushB35")
        sizePolicy.setHeightForWidth(self.pushB35.sizePolicy().hasHeightForWidth())
        self.pushB35.setSizePolicy(sizePolicy)
        self.pushB35.setMinimumSize(QSize(25, 25))
        self.pushB35.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB35, 3, 18, 1, 1)

        self.pushB12 = CountingButton(Dialog)
        self.pushB12.setObjectName(u"pushB12")
        sizePolicy.setHeightForWidth(self.pushB12.sizePolicy().hasHeightForWidth())
        self.pushB12.setSizePolicy(sizePolicy)
        self.pushB12.setMinimumSize(QSize(25, 25))
        self.pushB12.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB12, 2, 13, 1, 1)

        self.pushB18 = CountingButton(Dialog)
        self.pushB18.setObjectName(u"pushB18")
        sizePolicy.setHeightForWidth(self.pushB18.sizePolicy().hasHeightForWidth())
        self.pushB18.setSizePolicy(sizePolicy)
        self.pushB18.setMinimumSize(QSize(25, 25))
        self.pushB18.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB18, 3, 1, 1, 1)

        self.pushB60 = CountingButton(Dialog)
        self.pushB60.setObjectName(u"pushB60")
        sizePolicy.setHeightForWidth(self.pushB60.sizePolicy().hasHeightForWidth())
        self.pushB60.setSizePolicy(sizePolicy)
        self.pushB60.setMinimumSize(QSize(25, 25))
        self.pushB60.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB60, 8, 7, 1, 1)

        self.pushB98 = CountingButton(Dialog)
        self.pushB98.setObjectName(u"pushB98")
        sizePolicy.setHeightForWidth(self.pushB98.sizePolicy().hasHeightForWidth())
        self.pushB98.setSizePolicy(sizePolicy)
        self.pushB98.setMinimumSize(QSize(25, 25))
        self.pushB98.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB98, 9, 13, 1, 1)

        self.pushB100 = CountingButton(Dialog)
        self.pushB100.setObjectName(u"pushB100")
        sizePolicy.setHeightForWidth(self.pushB100.sizePolicy().hasHeightForWidth())
        self.pushB100.setSizePolicy(sizePolicy)
        self.pushB100.setMinimumSize(QSize(25, 25))
        self.pushB100.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB100, 9, 15, 1, 1)

        self.pushB54 = CountingButton(Dialog)
        self.pushB54.setObjectName(u"pushB54")
        sizePolicy.setHeightForWidth(self.pushB54.sizePolicy().hasHeightForWidth())
        self.pushB54.setSizePolicy(sizePolicy)
        self.pushB54.setMinimumSize(QSize(25, 25))
        self.pushB54.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB54, 5, 1, 1, 1)

        self.pushB79 = CountingButton(Dialog)
        self.pushB79.setObjectName(u"pushB79")
        sizePolicy.setHeightForWidth(self.pushB79.sizePolicy().hasHeightForWidth())
        self.pushB79.setSizePolicy(sizePolicy)
        self.pushB79.setMinimumSize(QSize(25, 25))
        self.pushB79.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB79, 5, 12, 1, 1)

        self.pushB11 = CountingButton(Dialog)
        self.pushB11.setObjectName(u"pushB11")
        sizePolicy.setHeightForWidth(self.pushB11.sizePolicy().hasHeightForWidth())
        self.pushB11.setSizePolicy(sizePolicy)
        self.pushB11.setMinimumSize(QSize(25, 25))
        self.pushB11.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB11, 2, 2, 1, 1)

        self.pushB63 = CountingButton(Dialog)
        self.pushB63.setObjectName(u"pushB63")
        sizePolicy.setHeightForWidth(self.pushB63.sizePolicy().hasHeightForWidth())
        self.pushB63.setSizePolicy(sizePolicy)
        self.pushB63.setMinimumSize(QSize(25, 25))
        self.pushB63.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB63, 8, 10, 1, 1)

        self.pushB91 = CountingButton(Dialog)
        self.pushB91.setObjectName(u"pushB91")
        sizePolicy.setHeightForWidth(self.pushB91.sizePolicy().hasHeightForWidth())
        self.pushB91.setSizePolicy(sizePolicy)
        self.pushB91.setMinimumSize(QSize(25, 25))
        self.pushB91.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB91, 9, 6, 1, 1)

        self.pushB42 = CountingButton(Dialog)
        self.pushB42.setObjectName(u"pushB42")
        sizePolicy.setHeightForWidth(self.pushB42.sizePolicy().hasHeightForWidth())
        self.pushB42.setSizePolicy(sizePolicy)
        self.pushB42.setMinimumSize(QSize(25, 25))
        self.pushB42.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB42, 4, 7, 1, 1)

        self.pushB62 = CountingButton(Dialog)
        self.pushB62.setObjectName(u"pushB62")
        sizePolicy.setHeightForWidth(self.pushB62.sizePolicy().hasHeightForWidth())
        self.pushB62.setSizePolicy(sizePolicy)
        self.pushB62.setMinimumSize(QSize(25, 25))
        self.pushB62.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB62, 8, 9, 1, 1)

        self.pushB64 = CountingButton(Dialog)
        self.pushB64.setObjectName(u"pushB64")
        sizePolicy.setHeightForWidth(self.pushB64.sizePolicy().hasHeightForWidth())
        self.pushB64.setSizePolicy(sizePolicy)
        self.pushB64.setMinimumSize(QSize(25, 25))
        self.pushB64.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB64, 8, 11, 1, 1)

        self.pushB0 = CountingButton(Dialog)
        self.pushB0.setObjectName(u"pushB0")
        sizePolicy.setHeightForWidth(self.pushB0.sizePolicy().hasHeightForWidth())
        self.pushB0.setSizePolicy(sizePolicy)
        self.pushB0.setMinimumSize(QSize(25, 25))
        self.pushB0.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB0, 0, 1, 1, 1)

        self.pushB69 = CountingButton(Dialog)
        self.pushB69.setObjectName(u"pushB69")
        sizePolicy.setHeightForWidth(self.pushB69.sizePolicy().hasHeightForWidth())
        self.pushB69.setSizePolicy(sizePolicy)
        self.pushB69.setMinimumSize(QSize(25, 25))
        self.pushB69.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB69, 8, 16, 1, 1)

        self.pushB50 = CountingButton(Dialog)
        self.pushB50.setObjectName(u"pushB50")
        sizePolicy.setHeightForWidth(self.pushB50.sizePolicy().hasHeightForWidth())
        self.pushB50.setSizePolicy(sizePolicy)
        self.pushB50.setMinimumSize(QSize(25, 25))
        self.pushB50.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB50, 4, 15, 1, 1)

        self.pushB29 = CountingButton(Dialog)
        self.pushB29.setObjectName(u"pushB29")
        sizePolicy.setHeightForWidth(self.pushB29.sizePolicy().hasHeightForWidth())
        self.pushB29.setSizePolicy(sizePolicy)
        self.pushB29.setMinimumSize(QSize(25, 25))
        self.pushB29.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB29, 3, 12, 1, 1)

        self.pushB96 = CountingButton(Dialog)
        self.pushB96.setObjectName(u"pushB96")
        sizePolicy.setHeightForWidth(self.pushB96.sizePolicy().hasHeightForWidth())
        self.pushB96.setSizePolicy(sizePolicy)
        self.pushB96.setMinimumSize(QSize(25, 25))
        self.pushB96.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB96, 9, 11, 1, 1)

        self.pushB38 = CountingButton(Dialog)
        self.pushB38.setObjectName(u"pushB38")
        sizePolicy.setHeightForWidth(self.pushB38.sizePolicy().hasHeightForWidth())
        self.pushB38.setSizePolicy(sizePolicy)
        self.pushB38.setMinimumSize(QSize(25, 25))
        self.pushB38.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB38, 4, 3, 1, 1)

        self.pushB43 = CountingButton(Dialog)
        self.pushB43.setObjectName(u"pushB43")
        sizePolicy.setHeightForWidth(self.pushB43.sizePolicy().hasHeightForWidth())
        self.pushB43.setSizePolicy(sizePolicy)
        self.pushB43.setMinimumSize(QSize(25, 25))
        self.pushB43.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB43, 4, 8, 1, 1)

        self.pushB59 = CountingButton(Dialog)
        self.pushB59.setObjectName(u"pushB59")
        sizePolicy.setHeightForWidth(self.pushB59.sizePolicy().hasHeightForWidth())
        self.pushB59.setSizePolicy(sizePolicy)
        self.pushB59.setMinimumSize(QSize(25, 25))
        self.pushB59.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB59, 8, 6, 1, 1)

        self.pushB76 = CountingButton(Dialog)
        self.pushB76.setObjectName(u"pushB76")
        sizePolicy.setHeightForWidth(self.pushB76.sizePolicy().hasHeightForWidth())
        self.pushB76.setSizePolicy(sizePolicy)
        self.pushB76.setMinimumSize(QSize(25, 25))
        self.pushB76.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB76, 5, 9, 1, 1)

        self.pushB20 = CountingButton(Dialog)
        self.pushB20.setObjectName(u"pushB20")
        sizePolicy.setHeightForWidth(self.pushB20.sizePolicy().hasHeightForWidth())
        self.pushB20.setSizePolicy(sizePolicy)
        self.pushB20.setMinimumSize(QSize(25, 25))
        self.pushB20.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB20, 3, 3, 1, 1)

        self.pushB40 = CountingButton(Dialog)
        self.pushB40.setObjectName(u"pushB40")
        sizePolicy.setHeightForWidth(self.pushB40.sizePolicy().hasHeightForWidth())
        self.pushB40.setSizePolicy(sizePolicy)
        self.pushB40.setMinimumSize(QSize(25, 25))
        self.pushB40.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB40, 4, 5, 1, 1)

        self.pushB65 = CountingButton(Dialog)
        self.pushB65.setObjectName(u"pushB65")
        sizePolicy.setHeightForWidth(self.pushB65.sizePolicy().hasHeightForWidth())
        self.pushB65.setSizePolicy(sizePolicy)
        self.pushB65.setMinimumSize(QSize(25, 25))
        self.pushB65.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB65, 8, 12, 1, 1)

        self.pushB89 = CountingButton(Dialog)
        self.pushB89.setObjectName(u"pushB89")
        sizePolicy.setHeightForWidth(self.pushB89.sizePolicy().hasHeightForWidth())
        self.pushB89.setSizePolicy(sizePolicy)
        self.pushB89.setMinimumSize(QSize(25, 25))
        self.pushB89.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB89, 9, 4, 1, 1)

        self.pushB81 = CountingButton(Dialog)
        self.pushB81.setObjectName(u"pushB81")
        sizePolicy.setHeightForWidth(self.pushB81.sizePolicy().hasHeightForWidth())
        self.pushB81.setSizePolicy(sizePolicy)
        self.pushB81.setMinimumSize(QSize(25, 25))
        self.pushB81.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB81, 5, 14, 1, 1)

        self.pushB52 = CountingButton(Dialog)
        self.pushB52.setObjectName(u"pushB52")
        sizePolicy.setHeightForWidth(self.pushB52.sizePolicy().hasHeightForWidth())
        self.pushB52.setSizePolicy(sizePolicy)
        self.pushB52.setMinimumSize(QSize(25, 25))
        self.pushB52.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB52, 4, 17, 1, 1)

        self.pushB32 = CountingButton(Dialog)
        self.pushB32.setObjectName(u"pushB32")
        sizePolicy.setHeightForWidth(self.pushB32.sizePolicy().hasHeightForWidth())
        self.pushB32.setSizePolicy(sizePolicy)
        self.pushB32.setMinimumSize(QSize(25, 25))
        self.pushB32.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB32, 3, 15, 1, 1)

        self.pushB8 = CountingButton(Dialog)
        self.pushB8.setObjectName(u"pushB8")
        sizePolicy.setHeightForWidth(self.pushB8.sizePolicy().hasHeightForWidth())
        self.pushB8.setSizePolicy(sizePolicy)
        self.pushB8.setMinimumSize(QSize(25, 25))
        self.pushB8.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB8, 1, 17, 1, 1)

        self.pushB117 = CountingButton(Dialog)
        self.pushB117.setObjectName(u"pushB117")
        sizePolicy.setHeightForWidth(self.pushB117.sizePolicy().hasHeightForWidth())
        self.pushB117.setSizePolicy(sizePolicy)
        self.pushB117.setMinimumSize(QSize(25, 25))
        self.pushB117.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB117, 6, 18, 1, 1)

        self.pushB84 = CountingButton(Dialog)
        self.pushB84.setObjectName(u"pushB84")
        sizePolicy.setHeightForWidth(self.pushB84.sizePolicy().hasHeightForWidth())
        self.pushB84.setSizePolicy(sizePolicy)
        self.pushB84.setMinimumSize(QSize(25, 25))
        self.pushB84.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB84, 5, 17, 1, 1)

        self.pushB21 = CountingButton(Dialog)
        self.pushB21.setObjectName(u"pushB21")
        sizePolicy.setHeightForWidth(self.pushB21.sizePolicy().hasHeightForWidth())
        self.pushB21.setSizePolicy(sizePolicy)
        self.pushB21.setMinimumSize(QSize(25, 25))
        self.pushB21.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB21, 3, 4, 1, 1)

        self.pushB9 = CountingButton(Dialog)
        self.pushB9.setObjectName(u"pushB9")
        sizePolicy.setHeightForWidth(self.pushB9.sizePolicy().hasHeightForWidth())
        self.pushB9.setSizePolicy(sizePolicy)
        self.pushB9.setMinimumSize(QSize(25, 25))
        self.pushB9.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB9, 1, 18, 1, 1)

        self.pushB14 = CountingButton(Dialog)
        self.pushB14.setObjectName(u"pushB14")
        sizePolicy.setHeightForWidth(self.pushB14.sizePolicy().hasHeightForWidth())
        self.pushB14.setSizePolicy(sizePolicy)
        self.pushB14.setMinimumSize(QSize(25, 25))
        self.pushB14.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB14, 2, 15, 1, 1)

        self.pushB26 = CountingButton(Dialog)
        self.pushB26.setObjectName(u"pushB26")
        sizePolicy.setHeightForWidth(self.pushB26.sizePolicy().hasHeightForWidth())
        self.pushB26.setSizePolicy(sizePolicy)
        self.pushB26.setMinimumSize(QSize(25, 25))
        self.pushB26.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB26, 3, 9, 1, 1)

        self.pushB33 = CountingButton(Dialog)
        self.pushB33.setObjectName(u"pushB33")
        sizePolicy.setHeightForWidth(self.pushB33.sizePolicy().hasHeightForWidth())
        self.pushB33.setSizePolicy(sizePolicy)
        self.pushB33.setMinimumSize(QSize(25, 25))
        self.pushB33.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB33, 3, 16, 1, 1)

        self.pushB31 = CountingButton(Dialog)
        self.pushB31.setObjectName(u"pushB31")
        sizePolicy.setHeightForWidth(self.pushB31.sizePolicy().hasHeightForWidth())
        self.pushB31.setSizePolicy(sizePolicy)
        self.pushB31.setMinimumSize(QSize(25, 25))
        self.pushB31.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB31, 3, 14, 1, 1)

        self.pushB17 = CountingButton(Dialog)
        self.pushB17.setObjectName(u"pushB17")
        sizePolicy.setHeightForWidth(self.pushB17.sizePolicy().hasHeightForWidth())
        self.pushB17.setSizePolicy(sizePolicy)
        self.pushB17.setMinimumSize(QSize(25, 25))
        self.pushB17.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB17, 2, 18, 1, 1)

        self.pushB109 = CountingButton(Dialog)
        self.pushB109.setObjectName(u"pushB109")
        sizePolicy.setHeightForWidth(self.pushB109.sizePolicy().hasHeightForWidth())
        self.pushB109.setSizePolicy(sizePolicy)
        self.pushB109.setMinimumSize(QSize(25, 25))
        self.pushB109.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB109, 6, 10, 1, 1)

        self.pushB108 = CountingButton(Dialog)
        self.pushB108.setObjectName(u"pushB108")
        sizePolicy.setHeightForWidth(self.pushB108.sizePolicy().hasHeightForWidth())
        self.pushB108.setSizePolicy(sizePolicy)
        self.pushB108.setMinimumSize(QSize(25, 25))
        self.pushB108.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB108, 6, 9, 1, 1)

        self.pushB3 = CountingButton(Dialog)
        self.pushB3.setObjectName(u"pushB3")
        sizePolicy.setHeightForWidth(self.pushB3.sizePolicy().hasHeightForWidth())
        self.pushB3.setSizePolicy(sizePolicy)
        self.pushB3.setMinimumSize(QSize(25, 25))
        self.pushB3.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB3, 1, 2, 1, 1)

        self.pushB78 = CountingButton(Dialog)
        self.pushB78.setObjectName(u"pushB78")
        sizePolicy.setHeightForWidth(self.pushB78.sizePolicy().hasHeightForWidth())
        self.pushB78.setSizePolicy(sizePolicy)
        self.pushB78.setMinimumSize(QSize(25, 25))
        self.pushB78.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB78, 5, 11, 1, 1)

        self.pushB105 = CountingButton(Dialog)
        self.pushB105.setObjectName(u"pushB105")
        sizePolicy.setHeightForWidth(self.pushB105.sizePolicy().hasHeightForWidth())
        self.pushB105.setSizePolicy(sizePolicy)
        self.pushB105.setMinimumSize(QSize(25, 25))
        self.pushB105.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB105, 6, 6, 1, 1)

        self.pushB34 = CountingButton(Dialog)
        self.pushB34.setObjectName(u"pushB34")
        sizePolicy.setHeightForWidth(self.pushB34.sizePolicy().hasHeightForWidth())
        self.pushB34.setSizePolicy(sizePolicy)
        self.pushB34.setMinimumSize(QSize(25, 25))
        self.pushB34.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB34, 3, 17, 1, 1)

        self.pushB87 = CountingButton(Dialog)
        self.pushB87.setObjectName(u"pushB87")
        sizePolicy.setHeightForWidth(self.pushB87.sizePolicy().hasHeightForWidth())
        self.pushB87.setSizePolicy(sizePolicy)
        self.pushB87.setMinimumSize(QSize(25, 25))
        self.pushB87.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB87, 6, 2, 1, 1)

        self.pushB23 = CountingButton(Dialog)
        self.pushB23.setObjectName(u"pushB23")
        sizePolicy.setHeightForWidth(self.pushB23.sizePolicy().hasHeightForWidth())
        self.pushB23.setSizePolicy(sizePolicy)
        self.pushB23.setMinimumSize(QSize(25, 25))
        self.pushB23.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB23, 3, 6, 1, 1)

        self.pushB4 = CountingButton(Dialog)
        self.pushB4.setObjectName(u"pushB4")
        sizePolicy.setHeightForWidth(self.pushB4.sizePolicy().hasHeightForWidth())
        self.pushB4.setSizePolicy(sizePolicy)
        self.pushB4.setMinimumSize(QSize(25, 25))
        self.pushB4.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB4, 1, 13, 1, 1)

        self.pushB83 = CountingButton(Dialog)
        self.pushB83.setObjectName(u"pushB83")
        sizePolicy.setHeightForWidth(self.pushB83.sizePolicy().hasHeightForWidth())
        self.pushB83.setSizePolicy(sizePolicy)
        self.pushB83.setMinimumSize(QSize(25, 25))
        self.pushB83.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB83, 5, 16, 1, 1)

        self.pushB115 = CountingButton(Dialog)
        self.pushB115.setObjectName(u"pushB115")
        sizePolicy.setHeightForWidth(self.pushB115.sizePolicy().hasHeightForWidth())
        self.pushB115.setSizePolicy(sizePolicy)
        self.pushB115.setMinimumSize(QSize(25, 25))
        self.pushB115.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB115, 6, 16, 1, 1)

        self.pushB44 = CountingButton(Dialog)
        self.pushB44.setObjectName(u"pushB44")
        sizePolicy.setHeightForWidth(self.pushB44.sizePolicy().hasHeightForWidth())
        self.pushB44.setSizePolicy(sizePolicy)
        self.pushB44.setMinimumSize(QSize(25, 25))
        self.pushB44.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB44, 4, 9, 1, 1)

        self.pushB27 = CountingButton(Dialog)
        self.pushB27.setObjectName(u"pushB27")
        sizePolicy.setHeightForWidth(self.pushB27.sizePolicy().hasHeightForWidth())
        self.pushB27.setSizePolicy(sizePolicy)
        self.pushB27.setMinimumSize(QSize(25, 25))
        self.pushB27.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB27, 3, 10, 1, 1)

        self.pushB92 = CountingButton(Dialog)
        self.pushB92.setObjectName(u"pushB92")
        sizePolicy.setHeightForWidth(self.pushB92.sizePolicy().hasHeightForWidth())
        self.pushB92.setSizePolicy(sizePolicy)
        self.pushB92.setMinimumSize(QSize(25, 25))
        self.pushB92.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB92, 9, 7, 1, 1)

        self.pushB61 = CountingButton(Dialog)
        self.pushB61.setObjectName(u"pushB61")
        sizePolicy.setHeightForWidth(self.pushB61.sizePolicy().hasHeightForWidth())
        self.pushB61.setSizePolicy(sizePolicy)
        self.pushB61.setMinimumSize(QSize(25, 25))
        self.pushB61.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB61, 8, 8, 1, 1)

        self.pushB41 = CountingButton(Dialog)
        self.pushB41.setObjectName(u"pushB41")
        sizePolicy.setHeightForWidth(self.pushB41.sizePolicy().hasHeightForWidth())
        self.pushB41.setSizePolicy(sizePolicy)
        self.pushB41.setMinimumSize(QSize(25, 25))
        self.pushB41.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB41, 4, 6, 1, 1)

        self.pushB57 = CountingButton(Dialog)
        self.pushB57.setObjectName(u"pushB57")
        sizePolicy.setHeightForWidth(self.pushB57.sizePolicy().hasHeightForWidth())
        self.pushB57.setSizePolicy(sizePolicy)
        self.pushB57.setMinimumSize(QSize(25, 25))
        self.pushB57.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB57, 8, 4, 1, 1)

        self.pushB95 = CountingButton(Dialog)
        self.pushB95.setObjectName(u"pushB95")
        sizePolicy.setHeightForWidth(self.pushB95.sizePolicy().hasHeightForWidth())
        self.pushB95.setSizePolicy(sizePolicy)
        self.pushB95.setMinimumSize(QSize(25, 25))
        self.pushB95.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB95, 9, 10, 1, 1)

        self.pushB97 = CountingButton(Dialog)
        self.pushB97.setObjectName(u"pushB97")
        sizePolicy.setHeightForWidth(self.pushB97.sizePolicy().hasHeightForWidth())
        self.pushB97.setSizePolicy(sizePolicy)
        self.pushB97.setMinimumSize(QSize(25, 25))
        self.pushB97.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB97, 9, 12, 1, 1)

        self.pushB99 = CountingButton(Dialog)
        self.pushB99.setObjectName(u"pushB99")
        sizePolicy.setHeightForWidth(self.pushB99.sizePolicy().hasHeightForWidth())
        self.pushB99.setSizePolicy(sizePolicy)
        self.pushB99.setMinimumSize(QSize(25, 25))
        self.pushB99.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB99, 9, 14, 1, 1)

        self.pushB47 = CountingButton(Dialog)
        self.pushB47.setObjectName(u"pushB47")
        sizePolicy.setHeightForWidth(self.pushB47.sizePolicy().hasHeightForWidth())
        self.pushB47.setSizePolicy(sizePolicy)
        self.pushB47.setMinimumSize(QSize(25, 25))
        self.pushB47.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB47, 4, 12, 1, 1)

        self.pushB106 = CountingButton(Dialog)
        self.pushB106.setObjectName(u"pushB106")
        sizePolicy.setHeightForWidth(self.pushB106.sizePolicy().hasHeightForWidth())
        self.pushB106.setSizePolicy(sizePolicy)
        self.pushB106.setMinimumSize(QSize(25, 25))
        self.pushB106.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB106, 6, 7, 1, 1)

        self.pushB71 = CountingButton(Dialog)
        self.pushB71.setObjectName(u"pushB71")
        sizePolicy.setHeightForWidth(self.pushB71.sizePolicy().hasHeightForWidth())
        self.pushB71.setSizePolicy(sizePolicy)
        self.pushB71.setMinimumSize(QSize(25, 25))
        self.pushB71.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB71, 5, 4, 1, 1)

        self.pushB58 = CountingButton(Dialog)
        self.pushB58.setObjectName(u"pushB58")
        sizePolicy.setHeightForWidth(self.pushB58.sizePolicy().hasHeightForWidth())
        self.pushB58.setSizePolicy(sizePolicy)
        self.pushB58.setMinimumSize(QSize(25, 25))
        self.pushB58.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB58, 8, 5, 1, 1)

        self.pushB104 = CountingButton(Dialog)
        self.pushB104.setObjectName(u"pushB104")
        sizePolicy.setHeightForWidth(self.pushB104.sizePolicy().hasHeightForWidth())
        self.pushB104.setSizePolicy(sizePolicy)
        self.pushB104.setMinimumSize(QSize(25, 25))
        self.pushB104.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB104, 6, 5, 1, 1)

        self.pushB68 = CountingButton(Dialog)
        self.pushB68.setObjectName(u"pushB68")
        sizePolicy.setHeightForWidth(self.pushB68.sizePolicy().hasHeightForWidth())
        self.pushB68.setSizePolicy(sizePolicy)
        self.pushB68.setMinimumSize(QSize(25, 25))
        self.pushB68.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB68, 8, 15, 1, 1)

        self.pushB15 = CountingButton(Dialog)
        self.pushB15.setObjectName(u"pushB15")
        sizePolicy.setHeightForWidth(self.pushB15.sizePolicy().hasHeightForWidth())
        self.pushB15.setSizePolicy(sizePolicy)
        self.pushB15.setMinimumSize(QSize(25, 25))
        self.pushB15.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB15, 2, 16, 1, 1)

        self.pushB90 = CountingButton(Dialog)
        self.pushB90.setObjectName(u"pushB90")
        sizePolicy.setHeightForWidth(self.pushB90.sizePolicy().hasHeightForWidth())
        self.pushB90.setSizePolicy(sizePolicy)
        self.pushB90.setMinimumSize(QSize(25, 25))
        self.pushB90.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB90, 9, 5, 1, 1)

        self.pushB112 = CountingButton(Dialog)
        self.pushB112.setObjectName(u"pushB112")
        sizePolicy.setHeightForWidth(self.pushB112.sizePolicy().hasHeightForWidth())
        self.pushB112.setSizePolicy(sizePolicy)
        self.pushB112.setMinimumSize(QSize(25, 25))
        self.pushB112.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB112, 6, 13, 1, 1)

        self.pushB94 = CountingButton(Dialog)
        self.pushB94.setObjectName(u"pushB94")
        sizePolicy.setHeightForWidth(self.pushB94.sizePolicy().hasHeightForWidth())
        self.pushB94.setSizePolicy(sizePolicy)
        self.pushB94.setMinimumSize(QSize(25, 25))
        self.pushB94.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB94, 9, 9, 1, 1)

        self.pushB77 = CountingButton(Dialog)
        self.pushB77.setObjectName(u"pushB77")
        sizePolicy.setHeightForWidth(self.pushB77.sizePolicy().hasHeightForWidth())
        self.pushB77.setSizePolicy(sizePolicy)
        self.pushB77.setMinimumSize(QSize(25, 25))
        self.pushB77.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB77, 5, 10, 1, 1)

        self.pushB49 = CountingButton(Dialog)
        self.pushB49.setObjectName(u"pushB49")
        sizePolicy.setHeightForWidth(self.pushB49.sizePolicy().hasHeightForWidth())
        self.pushB49.setSizePolicy(sizePolicy)
        self.pushB49.setMinimumSize(QSize(25, 25))
        self.pushB49.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB49, 4, 14, 1, 1)

        self.pushB45 = CountingButton(Dialog)
        self.pushB45.setObjectName(u"pushB45")
        sizePolicy.setHeightForWidth(self.pushB45.sizePolicy().hasHeightForWidth())
        self.pushB45.setSizePolicy(sizePolicy)
        self.pushB45.setMinimumSize(QSize(25, 25))
        self.pushB45.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB45, 4, 10, 1, 1)

        self.pushB7 = CountingButton(Dialog)
        self.pushB7.setObjectName(u"pushB7")
        sizePolicy.setHeightForWidth(self.pushB7.sizePolicy().hasHeightForWidth())
        self.pushB7.setSizePolicy(sizePolicy)
        self.pushB7.setMinimumSize(QSize(25, 25))
        self.pushB7.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB7, 1, 16, 1, 1)

        self.pushB86 = CountingButton(Dialog)
        self.pushB86.setObjectName(u"pushB86")
        sizePolicy.setHeightForWidth(self.pushB86.sizePolicy().hasHeightForWidth())
        self.pushB86.setSizePolicy(sizePolicy)
        self.pushB86.setMinimumSize(QSize(25, 25))
        self.pushB86.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB86, 6, 1, 1, 1)

        self.pushB46 = CountingButton(Dialog)
        self.pushB46.setObjectName(u"pushB46")
        sizePolicy.setHeightForWidth(self.pushB46.sizePolicy().hasHeightForWidth())
        self.pushB46.setSizePolicy(sizePolicy)
        self.pushB46.setMinimumSize(QSize(25, 25))
        self.pushB46.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB46, 4, 11, 1, 1)

        self.pushB36 = CountingButton(Dialog)
        self.pushB36.setObjectName(u"pushB36")
        sizePolicy.setHeightForWidth(self.pushB36.sizePolicy().hasHeightForWidth())
        self.pushB36.setSizePolicy(sizePolicy)
        self.pushB36.setMinimumSize(QSize(25, 25))
        self.pushB36.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB36, 4, 1, 1, 1)

        self.pushB67 = CountingButton(Dialog)
        self.pushB67.setObjectName(u"pushB67")
        sizePolicy.setHeightForWidth(self.pushB67.sizePolicy().hasHeightForWidth())
        self.pushB67.setSizePolicy(sizePolicy)
        self.pushB67.setMinimumSize(QSize(25, 25))
        self.pushB67.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB67, 8, 14, 1, 1)

        self.pushB24 = CountingButton(Dialog)
        self.pushB24.setObjectName(u"pushB24")
        sizePolicy.setHeightForWidth(self.pushB24.sizePolicy().hasHeightForWidth())
        self.pushB24.setSizePolicy(sizePolicy)
        self.pushB24.setMinimumSize(QSize(25, 25))
        self.pushB24.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB24, 3, 7, 1, 1)

        self.pushB107 = CountingButton(Dialog)
        self.pushB107.setObjectName(u"pushB107")
        sizePolicy.setHeightForWidth(self.pushB107.sizePolicy().hasHeightForWidth())
        self.pushB107.setSizePolicy(sizePolicy)
        self.pushB107.setMinimumSize(QSize(25, 25))
        self.pushB107.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB107, 6, 8, 1, 1)

        self.pushB80 = CountingButton(Dialog)
        self.pushB80.setObjectName(u"pushB80")
        sizePolicy.setHeightForWidth(self.pushB80.sizePolicy().hasHeightForWidth())
        self.pushB80.setSizePolicy(sizePolicy)
        self.pushB80.setMinimumSize(QSize(25, 25))
        self.pushB80.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB80, 5, 13, 1, 1)

        self.pushB37 = CountingButton(Dialog)
        self.pushB37.setObjectName(u"pushB37")
        sizePolicy.setHeightForWidth(self.pushB37.sizePolicy().hasHeightForWidth())
        self.pushB37.setSizePolicy(sizePolicy)
        self.pushB37.setMinimumSize(QSize(25, 25))
        self.pushB37.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB37, 4, 2, 1, 1)

        self.pushB73 = CountingButton(Dialog)
        self.pushB73.setObjectName(u"pushB73")
        sizePolicy.setHeightForWidth(self.pushB73.sizePolicy().hasHeightForWidth())
        self.pushB73.setSizePolicy(sizePolicy)
        self.pushB73.setMinimumSize(QSize(25, 25))
        self.pushB73.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB73, 5, 6, 1, 1)

        self.pushB1 = CountingButton(Dialog)
        self.pushB1.setObjectName(u"pushB1")
        sizePolicy.setHeightForWidth(self.pushB1.sizePolicy().hasHeightForWidth())
        self.pushB1.setSizePolicy(sizePolicy)
        self.pushB1.setMinimumSize(QSize(25, 25))
        self.pushB1.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB1, 0, 18, 1, 1)

        self.pushB74 = CountingButton(Dialog)
        self.pushB74.setObjectName(u"pushB74")
        sizePolicy.setHeightForWidth(self.pushB74.sizePolicy().hasHeightForWidth())
        self.pushB74.setSizePolicy(sizePolicy)
        self.pushB74.setMinimumSize(QSize(25, 25))
        self.pushB74.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB74, 5, 7, 1, 1)

        self.pushB102 = CountingButton(Dialog)
        self.pushB102.setObjectName(u"pushB102")
        sizePolicy.setHeightForWidth(self.pushB102.sizePolicy().hasHeightForWidth())
        self.pushB102.setSizePolicy(sizePolicy)
        self.pushB102.setMinimumSize(QSize(25, 25))
        self.pushB102.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB102, 9, 17, 1, 1)

        self.pushB111 = CountingButton(Dialog)
        self.pushB111.setObjectName(u"pushB111")
        sizePolicy.setHeightForWidth(self.pushB111.sizePolicy().hasHeightForWidth())
        self.pushB111.setSizePolicy(sizePolicy)
        self.pushB111.setMinimumSize(QSize(25, 25))
        self.pushB111.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB111, 6, 12, 1, 1)

        self.pushB10 = CountingButton(Dialog)
        self.pushB10.setObjectName(u"pushB10")
        sizePolicy.setHeightForWidth(self.pushB10.sizePolicy().hasHeightForWidth())
        self.pushB10.setSizePolicy(sizePolicy)
        self.pushB10.setMinimumSize(QSize(25, 25))
        self.pushB10.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB10, 2, 1, 1, 1)

        self.pushB13 = CountingButton(Dialog)
        self.pushB13.setObjectName(u"pushB13")
        sizePolicy.setHeightForWidth(self.pushB13.sizePolicy().hasHeightForWidth())
        self.pushB13.setSizePolicy(sizePolicy)
        self.pushB13.setMinimumSize(QSize(25, 25))
        self.pushB13.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB13, 2, 14, 1, 1)

        self.pushB2 = CountingButton(Dialog)
        self.pushB2.setObjectName(u"pushB2")
        sizePolicy.setHeightForWidth(self.pushB2.sizePolicy().hasHeightForWidth())
        self.pushB2.setSizePolicy(sizePolicy)
        self.pushB2.setMinimumSize(QSize(25, 25))
        self.pushB2.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB2, 1, 1, 1, 1)

        self.pushB55 = CountingButton(Dialog)
        self.pushB55.setObjectName(u"pushB55")
        sizePolicy.setHeightForWidth(self.pushB55.sizePolicy().hasHeightForWidth())
        self.pushB55.setSizePolicy(sizePolicy)
        self.pushB55.setMinimumSize(QSize(25, 25))
        self.pushB55.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB55, 5, 2, 1, 1)

        self.pushB56 = CountingButton(Dialog)
        self.pushB56.setObjectName(u"pushB56")
        sizePolicy.setHeightForWidth(self.pushB56.sizePolicy().hasHeightForWidth())
        self.pushB56.setSizePolicy(sizePolicy)
        self.pushB56.setMinimumSize(QSize(25, 25))
        self.pushB56.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB56, 8, 3, 1, 1)

        self.pushB25 = CountingButton(Dialog)
        self.pushB25.setObjectName(u"pushB25")
        sizePolicy.setHeightForWidth(self.pushB25.sizePolicy().hasHeightForWidth())
        self.pushB25.setSizePolicy(sizePolicy)
        self.pushB25.setMinimumSize(QSize(25, 25))
        self.pushB25.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB25, 3, 8, 1, 1)

        self.pushB93 = CountingButton(Dialog)
        self.pushB93.setObjectName(u"pushB93")
        sizePolicy.setHeightForWidth(self.pushB93.sizePolicy().hasHeightForWidth())
        self.pushB93.setSizePolicy(sizePolicy)
        self.pushB93.setMinimumSize(QSize(25, 25))
        self.pushB93.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB93, 9, 8, 1, 1)

        self.pushB28 = CountingButton(Dialog)
        self.pushB28.setObjectName(u"pushB28")
        sizePolicy.setHeightForWidth(self.pushB28.sizePolicy().hasHeightForWidth())
        self.pushB28.setSizePolicy(sizePolicy)
        self.pushB28.setMinimumSize(QSize(25, 25))
        self.pushB28.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB28, 3, 11, 1, 1)

        self.pushB19 = CountingButton(Dialog)
        self.pushB19.setObjectName(u"pushB19")
        sizePolicy.setHeightForWidth(self.pushB19.sizePolicy().hasHeightForWidth())
        self.pushB19.setSizePolicy(sizePolicy)
        self.pushB19.setMinimumSize(QSize(25, 25))
        self.pushB19.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB19, 3, 2, 1, 1)

        self.pushB51 = CountingButton(Dialog)
        self.pushB51.setObjectName(u"pushB51")
        sizePolicy.setHeightForWidth(self.pushB51.sizePolicy().hasHeightForWidth())
        self.pushB51.setSizePolicy(sizePolicy)
        self.pushB51.setMinimumSize(QSize(25, 25))
        self.pushB51.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB51, 4, 16, 1, 1)

        self.pushB30 = CountingButton(Dialog)
        self.pushB30.setObjectName(u"pushB30")
        sizePolicy.setHeightForWidth(self.pushB30.sizePolicy().hasHeightForWidth())
        self.pushB30.setSizePolicy(sizePolicy)
        self.pushB30.setMinimumSize(QSize(25, 25))
        self.pushB30.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB30, 3, 13, 1, 1)

        self.pushB113 = CountingButton(Dialog)
        self.pushB113.setObjectName(u"pushB113")
        sizePolicy.setHeightForWidth(self.pushB113.sizePolicy().hasHeightForWidth())
        self.pushB113.setSizePolicy(sizePolicy)
        self.pushB113.setMinimumSize(QSize(25, 25))
        self.pushB113.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB113, 6, 14, 1, 1)

        self.pushB48 = CountingButton(Dialog)
        self.pushB48.setObjectName(u"pushB48")
        sizePolicy.setHeightForWidth(self.pushB48.sizePolicy().hasHeightForWidth())
        self.pushB48.setSizePolicy(sizePolicy)
        self.pushB48.setMinimumSize(QSize(25, 25))
        self.pushB48.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB48, 4, 13, 1, 1)

        self.pushB53 = CountingButton(Dialog)
        self.pushB53.setObjectName(u"pushB53")
        sizePolicy.setHeightForWidth(self.pushB53.sizePolicy().hasHeightForWidth())
        self.pushB53.setSizePolicy(sizePolicy)
        self.pushB53.setMinimumSize(QSize(25, 25))
        self.pushB53.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB53, 4, 18, 1, 1)

        self.pushB5 = CountingButton(Dialog)
        self.pushB5.setObjectName(u"pushB5")
        sizePolicy.setHeightForWidth(self.pushB5.sizePolicy().hasHeightForWidth())
        self.pushB5.setSizePolicy(sizePolicy)
        self.pushB5.setMinimumSize(QSize(25, 25))
        self.pushB5.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB5, 1, 14, 1, 1)

        self.pushB16 = CountingButton(Dialog)
        self.pushB16.setObjectName(u"pushB16")
        sizePolicy.setHeightForWidth(self.pushB16.sizePolicy().hasHeightForWidth())
        self.pushB16.setSizePolicy(sizePolicy)
        self.pushB16.setMinimumSize(QSize(25, 25))
        self.pushB16.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB16, 2, 17, 1, 1)

        self.pushB6 = CountingButton(Dialog)
        self.pushB6.setObjectName(u"pushB6")
        sizePolicy.setHeightForWidth(self.pushB6.sizePolicy().hasHeightForWidth())
        self.pushB6.setSizePolicy(sizePolicy)
        self.pushB6.setMinimumSize(QSize(25, 25))
        self.pushB6.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB6, 1, 15, 1, 1)

        self.pushB39 = CountingButton(Dialog)
        self.pushB39.setObjectName(u"pushB39")
        sizePolicy.setHeightForWidth(self.pushB39.sizePolicy().hasHeightForWidth())
        self.pushB39.setSizePolicy(sizePolicy)
        self.pushB39.setMinimumSize(QSize(25, 25))
        self.pushB39.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushB39, 4, 4, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.label_2, 7, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(True)
        self.lineEdit.setMaximumSize(QSize(100, 16777215))
        self.lineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"debyetools - [define compound...]", None))
        self.pushB88.setText(QCoreApplication.translate("Dialog", u"Ac", None))
        self.pushB66.setText(QCoreApplication.translate("Dialog", u"Ho", None))
        self.pushB85.setText(QCoreApplication.translate("Dialog", u"Rn", None))
        self.pushB75.setText(QCoreApplication.translate("Dialog", u"Os", None))
        self.pushB101.setText(QCoreApplication.translate("Dialog", u"No", None))
        self.pushB110.setText(QCoreApplication.translate("Dialog", u"Rg", None))
        self.pushB82.setText(QCoreApplication.translate("Dialog", u"Bi", None))
        self.pushB70.setText(QCoreApplication.translate("Dialog", u"Lu", None))
        self.pushB116.setText(QCoreApplication.translate("Dialog", u"Ts", None))
        self.pushB72.setText(QCoreApplication.translate("Dialog", u"Ta", None))
        self.pushB114.setText(QCoreApplication.translate("Dialog", u"Mc", None))
        self.pushB22.setText(QCoreApplication.translate("Dialog", u"V", None))
        self.pushB103.setText(QCoreApplication.translate("Dialog", u"Rf", None))
        self.pushB35.setText(QCoreApplication.translate("Dialog", u"Kr", None))
        self.pushB12.setText(QCoreApplication.translate("Dialog", u"Al", None))
        self.pushB18.setText(QCoreApplication.translate("Dialog", u"K", None))
        self.pushB60.setText(QCoreApplication.translate("Dialog", u"Pm", None))
        self.pushB98.setText(QCoreApplication.translate("Dialog", u"Es", None))
        self.pushB100.setText(QCoreApplication.translate("Dialog", u"Md", None))
        self.pushB54.setText(QCoreApplication.translate("Dialog", u"Cs", None))
        self.pushB79.setText(QCoreApplication.translate("Dialog", u"Hg", None))
        self.pushB11.setText(QCoreApplication.translate("Dialog", u"Mg", None))
        self.pushB63.setText(QCoreApplication.translate("Dialog", u"Gd", None))
        self.pushB91.setText(QCoreApplication.translate("Dialog", u"U", None))
        self.pushB42.setText(QCoreApplication.translate("Dialog", u"Tc", None))
        self.pushB62.setText(QCoreApplication.translate("Dialog", u"Eu", None))
        self.pushB64.setText(QCoreApplication.translate("Dialog", u"Tb", None))
        self.pushB0.setText(QCoreApplication.translate("Dialog", u"H", None))
        self.pushB69.setText(QCoreApplication.translate("Dialog", u"Yb", None))
        self.pushB50.setText(QCoreApplication.translate("Dialog", u"Sb", None))
        self.pushB29.setText(QCoreApplication.translate("Dialog", u"Zn", None))
        self.pushB96.setText(QCoreApplication.translate("Dialog", u"Bk", None))
        self.pushB38.setText(QCoreApplication.translate("Dialog", u"Y", None))
        self.pushB43.setText(QCoreApplication.translate("Dialog", u"Ru", None))
        self.pushB59.setText(QCoreApplication.translate("Dialog", u"Nd", None))
        self.pushB76.setText(QCoreApplication.translate("Dialog", u"Ir", None))
        self.pushB20.setText(QCoreApplication.translate("Dialog", u"Sc", None))
        self.pushB40.setText(QCoreApplication.translate("Dialog", u"Nb", None))
        self.pushB65.setText(QCoreApplication.translate("Dialog", u"Dy", None))
        self.pushB89.setText(QCoreApplication.translate("Dialog", u"Th", None))
        self.pushB81.setText(QCoreApplication.translate("Dialog", u"Pb", None))
        self.pushB52.setText(QCoreApplication.translate("Dialog", u"I", None))
        self.pushB32.setText(QCoreApplication.translate("Dialog", u"As", None))
        self.pushB8.setText(QCoreApplication.translate("Dialog", u"F", None))
        self.pushB117.setText(QCoreApplication.translate("Dialog", u"Og", None))
        self.pushB84.setText(QCoreApplication.translate("Dialog", u"At", None))
        self.pushB21.setText(QCoreApplication.translate("Dialog", u"Ti", None))
        self.pushB9.setText(QCoreApplication.translate("Dialog", u"Ne", None))
        self.pushB14.setText(QCoreApplication.translate("Dialog", u"P", None))
        self.pushB26.setText(QCoreApplication.translate("Dialog", u"Co", None))
        self.pushB33.setText(QCoreApplication.translate("Dialog", u"Se", None))
        self.pushB31.setText(QCoreApplication.translate("Dialog", u"Ge", None))
        self.pushB17.setText(QCoreApplication.translate("Dialog", u"Ar", None))
        self.pushB109.setText(QCoreApplication.translate("Dialog", u"Ds", None))
        self.pushB108.setText(QCoreApplication.translate("Dialog", u"Mt", None))
        self.pushB3.setText(QCoreApplication.translate("Dialog", u"Be", None))
        self.pushB78.setText(QCoreApplication.translate("Dialog", u"Au", None))
        self.pushB105.setText(QCoreApplication.translate("Dialog", u"Sg", None))
        self.pushB34.setText(QCoreApplication.translate("Dialog", u"Br", None))
        self.pushB87.setText(QCoreApplication.translate("Dialog", u"Ra", None))
        self.pushB23.setText(QCoreApplication.translate("Dialog", u"Cr", None))
        self.pushB4.setText(QCoreApplication.translate("Dialog", u"B", None))
        self.pushB83.setText(QCoreApplication.translate("Dialog", u"Po", None))
        self.pushB115.setText(QCoreApplication.translate("Dialog", u"Lv", None))
        self.pushB44.setText(QCoreApplication.translate("Dialog", u"Rh", None))
        self.pushB27.setText(QCoreApplication.translate("Dialog", u"Ni", None))
        self.pushB92.setText(QCoreApplication.translate("Dialog", u"Np", None))
        self.pushB61.setText(QCoreApplication.translate("Dialog", u"Sm", None))
        self.pushB41.setText(QCoreApplication.translate("Dialog", u"Mo", None))
        self.pushB57.setText(QCoreApplication.translate("Dialog", u"Ce", None))
        self.pushB95.setText(QCoreApplication.translate("Dialog", u"Cm", None))
        self.pushB97.setText(QCoreApplication.translate("Dialog", u"Cf", None))
        self.pushB99.setText(QCoreApplication.translate("Dialog", u"Fm", None))
        self.pushB47.setText(QCoreApplication.translate("Dialog", u"Cd", None))
        self.pushB106.setText(QCoreApplication.translate("Dialog", u"Bh", None))
        self.pushB71.setText(QCoreApplication.translate("Dialog", u"Hf", None))
        self.pushB58.setText(QCoreApplication.translate("Dialog", u"Pr", None))
        self.pushB104.setText(QCoreApplication.translate("Dialog", u"Db", None))
        self.pushB68.setText(QCoreApplication.translate("Dialog", u"Tm", None))
        self.pushB15.setText(QCoreApplication.translate("Dialog", u"S", None))
        self.pushB90.setText(QCoreApplication.translate("Dialog", u"Pa", None))
        self.pushB112.setText(QCoreApplication.translate("Dialog", u"Nh", None))
        self.pushB94.setText(QCoreApplication.translate("Dialog", u"Am", None))
        self.pushB77.setText(QCoreApplication.translate("Dialog", u"Pt", None))
        self.pushB49.setText(QCoreApplication.translate("Dialog", u"Sn", None))
        self.pushB45.setText(QCoreApplication.translate("Dialog", u"Pd", None))
        self.pushB7.setText(QCoreApplication.translate("Dialog", u"O", None))
        self.pushB86.setText(QCoreApplication.translate("Dialog", u"Fr", None))
        self.pushB46.setText(QCoreApplication.translate("Dialog", u"Ag", None))
        self.pushB36.setText(QCoreApplication.translate("Dialog", u"Rb", None))
        self.pushB67.setText(QCoreApplication.translate("Dialog", u"Er", None))
        self.pushB24.setText(QCoreApplication.translate("Dialog", u"Mn", None))
        self.pushB107.setText(QCoreApplication.translate("Dialog", u"Hs", None))
        self.pushB80.setText(QCoreApplication.translate("Dialog", u"Tl", None))
        self.pushB37.setText(QCoreApplication.translate("Dialog", u"Sr", None))
        self.pushB73.setText(QCoreApplication.translate("Dialog", u"W", None))
        self.pushB1.setText(QCoreApplication.translate("Dialog", u"He", None))
        self.pushB74.setText(QCoreApplication.translate("Dialog", u"Re", None))
        self.pushB102.setText(QCoreApplication.translate("Dialog", u"Lr", None))
        self.pushB111.setText(QCoreApplication.translate("Dialog", u"Cn", None))
        self.pushB10.setText(QCoreApplication.translate("Dialog", u"Na", None))
        self.pushB13.setText(QCoreApplication.translate("Dialog", u"Si", None))
        self.pushB2.setText(QCoreApplication.translate("Dialog", u"Li", None))
        self.pushB55.setText(QCoreApplication.translate("Dialog", u"Ba", None))
        self.pushB56.setText(QCoreApplication.translate("Dialog", u"La", None))
        self.pushB25.setText(QCoreApplication.translate("Dialog", u"Fe", None))
        self.pushB93.setText(QCoreApplication.translate("Dialog", u"Pu", None))
        self.pushB28.setText(QCoreApplication.translate("Dialog", u"Cu", None))
        self.pushB19.setText(QCoreApplication.translate("Dialog", u"Ca", None))
        self.pushB51.setText(QCoreApplication.translate("Dialog", u"Te", None))
        self.pushB30.setText(QCoreApplication.translate("Dialog", u"Ga", None))
        self.pushB113.setText(QCoreApplication.translate("Dialog", u"Fl", None))
        self.pushB48.setText(QCoreApplication.translate("Dialog", u"In", None))
        self.pushB53.setText(QCoreApplication.translate("Dialog", u"Xe", None))
        self.pushB5.setText(QCoreApplication.translate("Dialog", u"C", None))
        self.pushB16.setText(QCoreApplication.translate("Dialog", u"Cl", None))
        self.pushB6.setText(QCoreApplication.translate("Dialog", u"N", None))
        self.pushB39.setText(QCoreApplication.translate("Dialog", u"Zr", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Formula:", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi


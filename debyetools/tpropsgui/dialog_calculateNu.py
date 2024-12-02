from PySide6.QtWidgets import QDialog, QMessageBox

from debyetools.tpropsgui.ui_dialog_calculateNu import Ui_Form as Ui_iparams

from debyetools.poisson import poisson_ratio as dt_poisson_ratio

import numpy as np

from debyetools.tpropsgui.dialog_loadElastic import dialogLoadElastic

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QPalette

from debyetools.tpropsgui.dialog_elastic import dialogElastic

import debyetools.tpropsgui.elastic_props as elastic
import sys
def highlight_line_edit(line_edit, color="purple", duration=100):
    # Set the background color
    line_edit.setStyleSheet(f"background-color: {color};")

    # Create a QTimer to reset the color after `duration` milliseconds
    timer = QTimer(line_edit)
    timer.setSingleShot(True)  # Only trigger once
    timer.timeout.connect(lambda: line_edit.setStyleSheet(""))  # Reset the color
    timer.start(duration)


class dialogCalcNu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_iparams()
        self.ui.setupUi(self)

        self.ui.pushSave.clicked.connect(self.on_pushSave)
        self.ui.pushButton_2.clicked.connect(self.on_pushButton_calc_nu)

        self.ui.pushLoadElastic.clicked.connect(self.on_pushLoadElastic)

        self.dialog_loadElastic = dialogLoadElastic(self)

        # Connect the textChanged signals to a shared color change method
        self.ui.elastic_constants.textChanged.connect(lambda: self.on_text_changed(self.ui.elastic_constants))
        self.ui.lineEdit_5.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_5))
        self.ui.lineEdit_4.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_4))
        self.ui.lineEdit_6.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_6))
        self.ui.lineEdit_10.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_10))
        self.ui.lineEdit_9.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_9))
        self.ui.lineEdit_8.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_8))
        self.ui.lineEdit_7.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_7))
        self.ui.lineEdit_3.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_3))

        self.ui.pushMore.clicked.connect(self.on_pushMore_calcElastic)

        self.dialogElastic = dialogElastic(self)

    def on_pushLoadElastic(self):
        self.dialog_loadElastic.elastic_constants = self.ui.elastic_constants
        self.dialog_loadElastic.show()

    def on_pushSave(self):
        current_text = self.ui.lineEdit_3.text()
        self.external_nu.setText(current_text)
        self.close()

    def get_C(self):
        txt = self.ui.elastic_constants.toPlainText().replace('XX', ' ').replace('YY', ' ').replace('ZZ', ' ').replace(
            'XY', ' ').replace('YZ', ' ').replace('ZX', ' ').split('\n')
        data_lst = []
        for ti in txt:
            if len(ti) == 0: continue
            if ti[0] == '#': continue
            data_lst.append([float(tii) for tii in ti.replace('\t', ' ').split()])

        # print(data_lst)
        data = np.array(data_lst)

        return data

    def on_pushButton_calc_nu(self):
        C = self.get_C()
        BR, BV, B, GR, GV, S, AU, nu = dt_poisson_ratio(C, quiet=True)
        self.ui.lineEdit_3.setText('%.3f' % (nu))
        self.ui.lineEdit_4.setText('%.1f' % (BR * 10))
        self.ui.lineEdit_5.setText('%.1f' % (BV * 10))
        self.ui.lineEdit_6.setText('%.1f' % (B * 10))
        self.ui.lineEdit_9.setText('%.1f' % (GV * 10))
        self.ui.lineEdit_8.setText('%.1f' % (GR * 10))
        self.ui.lineEdit_7.setText('%.1f' % (S * 10))
        self.ui.lineEdit_10.setText('%.2f' % (AU))

    def is_dark_mode(self):
        # Detect if the application is in dark mode using the palette
        palette = self.palette()
        return palette.color(QPalette.ColorRole.Window).value() < 128  # Lightness threshold for dark mode

    def on_text_changed(self, line_edit):
        # Call the reusable highlight function
        dark_mode = self.is_dark_mode()
        color_p = "purple" if dark_mode else "#94a2c9"

        highlight_line_edit(line_edit, color=color_p, duration=500)
        # Update label with the current content of the edited line edit

    def on_pushMore_calcElastic(self):

        sys.stdout.reconfigure(encoding='utf-8')

        C = self.get_C()
        retxt, resdata=elastic.run_script(C)
        del resdata

        print(retxt.expandtabs(8))

        # # Assuming a font width of 8 pixels per character for 8 spaces
        # tab_width = 8 * 8  # 8 spaces * approx. 8 pixels per space in typical monospace font

        # # Set the tab width in the QPlainTextEdit
        # self.dialogElastic.ui.plainTextEdit.setTabStopDistance(tab_width)

        # Set the text content with expandtabs(8) to replace tabs with 8 spaces in the content itself
        self.dialogElastic.ui.plainTextEdit.setPlainText(res.expandtabs(8))
        self.dialogElastic.EM = C
        self.dialogElastic.show()


        # QMessageBox.information(self, 'Error', res.expandtabs(8), QMessageBox.Ok)


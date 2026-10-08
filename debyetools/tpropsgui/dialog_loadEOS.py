import warnings
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from debyetools.tpropsgui.ui_dialog_loadEOS import Ui_Dialog as Ui_loadEOS
# from atomtools import atomic_mass
from debyetools.aux_functions import load_V_E as dt_load_V_E

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QPalette
# def log_mean(lst):
#     import numpy as np
#     l = len(lst)
#     # lm = np.sum([np.log(li)/l for li in lst])
#     # m = np.exp(lm)
#     return np.sum([li for li in lst])/l


def highlight_line_edit(line_edit, color="purple", duration=100):
    # Set the background color
    line_edit.setStyleSheet(f"background-color: {color};")

    # Create a QTimer to reset the color after `duration` milliseconds
    timer = QTimer(line_edit)
    timer.setSingleShot(True)  # Only trigger once
    timer.timeout.connect(lambda: line_edit.setStyleSheet(""))  # Reset the color
    timer.start(duration)

class dialogLoadEOS(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_loadEOS()
        self.ui.setupUi(self)

        self.ui.browsesummary.clicked.connect(self.getfilessummary)
        self.ui.browseposcar.clicked.connect(self.getfilesposcar)
        self.ui.ok.clicked.connect(self.on_pushButton_OK)
        self.filepath='.'

        # Connect the textChanged signals to a shared color change method
        self.ui.summarypath.textChanged.connect(lambda: self.on_text_changed(self.ui.summarypath))
        self.ui.poscarpath.textChanged.connect(lambda: self.on_text_changed(self.ui.poscarpath))


    def getfilessummary(self):
        summarypath, _ = QFileDialog.getOpenFileName(self, caption='Select a SUMMARY file')
        self.ui.summarypath.setText(summarypath)
        self.summarypath = summarypath

    def getfilesposcar(self):
        poscarpath, _ = QFileDialog.getOpenFileName(self, caption='Select a POSCAR or CONTCAR file')
        self.ui.poscarpath.setText(poscarpath)
        self.poscarpath = poscarpath

    def on_pushButton_OK(self):
        """Read SUMMARY + POSCAR when OK is pressed (not on close) and paste E(V); errors are shown (G11)."""
        self.summarypath = self.ui.summarypath.text()
        self.poscarpath = self.ui.poscarpath.text()
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                V, E = dt_load_V_E(self.summarypath, self.poscarpath)  # energy: E0= (sigma -> 0), C-DOC3
        except Exception as e:
            QMessageBox.information(self, 'Error', 'Could not read the energy-volume data:\n%s' % e, QMessageBox.Ok)
            return
        if caught:
            QMessageBox.information(self, 'Note', '\n'.join(str(w.message) for w in caught), QMessageBox.Ok)
        txt2paste = '#V\tE\n'
        for v, e in zip(V, E):
            txt2paste = txt2paste + '%.6e\t%.6e'%(v, e)+'\n'
        self.EvVtext.setPlainText(txt2paste)
        self.close()

    def is_dark_mode(self):
        # Detect if the application is in dark mode using the palette
        palette = self.palette()
        return palette.color(QPalette.ColorRole.Window).value() < 128  # Lightness threshold for dark mode

    def on_text_changed(self, line_edit):
        # Call the reusable highlight function
        dark_mode = self.is_dark_mode()
        color_p = "purple" if dark_mode else "#94a2c9"

        highlight_line_edit(line_edit, color=color_p, duration=500)


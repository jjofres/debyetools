from PySide6.QtWidgets import  QDialog, QFileDialog, QMessageBox
from debyetools.tpropsgui.ui_dialog_loadElastic import Ui_Dialog as Ui_OUTCAR
from debyetools.aux_functions import load_EM as dt_load_EM

import numpy as np
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QPalette

def highlight_line_edit(line_edit, color="purple", duration=100):
    # Set the background color
    line_edit.setStyleSheet(f"background-color: {color};")

    # Create a QTimer to reset the color after `duration` milliseconds
    timer = QTimer(line_edit)
    timer.setSingleShot(True)  # Only trigger once
    timer.timeout.connect(lambda: line_edit.setStyleSheet(""))  # Reset the color
    timer.start(duration)

class dialogLoadElastic(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_OUTCAR()
        self.ui.setupUi(self)

        self.ui.browseoutcar.clicked.connect(self.getfilesoutcar)
#        self.ui.browseposcar.clicked.connect(self.getfilesposcar)
        self.ui.ok.clicked.connect(self.on_pushButton_OK)
        self.filepath='.'

        # Connect the textChanged signals to a shared color change method
        self.ui.outcarpath.textChanged.connect(lambda: self.on_text_changed(self.ui.outcarpath))


    def getfilesoutcar(self):
        outcarpath, _ = QFileDialog.getOpenFileName(self, caption='Select an OUTCAR file')
        self.ui.outcarpath.setText(outcarpath)

#    def getfilesposcar(self):
#        poscarpath, _ = QFileDialog.getOpenFileName(self, caption='Select a POSCAR or CONTCAR file')
#        self.ui.poscarpath.setText(poscarpath)

    def on_pushButton_OK(self):
        """Read the OUTCAR when OK is pressed (not on close) and paste the moduli in GPa; errors are shown (G11)."""
        self.outcarpath = self.ui.outcarpath.text()
        try:
            EM = dt_load_EM(self.outcarpath)  # kBar, relaxed-ion (D1)
        except Exception as e:
            QMessageBox.information(self, 'Error', 'Could not read the elastic constants:\n%s' % e, QMessageBox.Ok)
            return
        # VASP order (XX YY ZZ XY YZ ZX) -> Voigt order (XX YY ZZ YZ ZX XY): the directional properties
        # (elastic_props, ELATE) expect Voigt order; nu and the averages do not depend on it (G10)
        voigt = [0, 1, 2, 4, 5, 3]
        EM = np.asarray(EM, dtype=float)[np.ix_(voigt, voigt)]
        txt2paste = '# GPa, Voigt order: XX YY ZZ YZ ZX XY\n'
        for rowi in EM:
            txt2paste=txt2paste+' '.join(['%.2f'%(float(coli)/10) for coli in rowi])+'\n'
        self.elastic_constants.setText(txt2paste)
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
        # Update label with the current content of the edited line edit



# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

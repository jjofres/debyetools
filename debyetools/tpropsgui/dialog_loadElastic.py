from PySide6.QtWidgets import  QDialog, QFileDialog
from debyetools.tpropsgui.ui_dialog_loadElastic import Ui_Dialog as Ui_OUTCAR
from debyetools.aux_functions import load_EM as dt_load_EM

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
        self.outcarpath = self.ui.outcarpath.text()
#        self.poscarpath = self.ui.poscarpath.text()
        self.close()
    def closeEvent(self, event):
        EM = dt_load_EM(self.outcarpath)
#        print(EM)

        txt2paste = ''
        for rowi in EM:
            txt2paste=txt2paste+' '.join(['%.2f'%(float(coli)/10) for coli in rowi])+'\n'
#        print('event', event)
        self.elastic_constants.setText(txt2paste)

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

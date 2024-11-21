from PySide6.QtWidgets import  QDialog, QFileDialog
from debyetools.tpropsgui.ui_dialog_doscar import Ui_Dialog as Ui_DOSCAR

from debyetools.aux_functions import load_doscar as dt_load_doscar
from debyetools.electronic import fit_electronic as dt_fit_electronic

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




class dialogDoscar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DOSCAR()
        self.ui.setupUi(self)

        self.ui.browse.clicked.connect(self.getfiles)
        self.ui.pushExit.clicked.connect(self.on_pushButton_OK)
        self.ui.pushCalc.clicked.connect(self.on_pushCalc)
        self.filepath='.'

        # Connect the textChanged signals to a shared color change method
        self.ui.filepath.textChanged.connect(lambda: self.on_text_changed(self.ui.filepath))
        self.ui.lineEdit_el.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_el))


    def get_EvV(self):
        if self.ui.radioButton.isChecked():
            conv = [(1e-30 * 6.02e23), (0.160218e-18 * 6.02214e23)]
        elif self.ui.radioButton_3.isChecked():
            conv =[1, 1]

        txt = self.ui.EvVText.toPlainText().split('\n')
        data_lst = []
        for ti in txt:
            if len(ti)==0:continue
            if ti[0]=='#': continue
            data_lst.append([float(tii) for tii in ti.split()])
        data = np.array(data_lst)
        ncols = len(data.T)
        return (data[:,i]*conv[i] for i in range(ncols))


    def get_el_params(self):
        txt = self.external_iparams.text()
        if txt=='':
            return 3e-01, -1e+04, 5e-04, 1e-06
        return  [float(ti) for ti in txt.replace(' ','').split(',')]

    def on_pushCalc(self):
        # Vdata, Edata = self.get_EvV()
        status  = 0
        try:
            print(self.Vdata)
            status = 1
        except:
            print('error: Energy curve probably not loaded yet.')

        if status == 1:
            E, N, Ef = dt_load_doscar('', list_filetags = self.filepath_list)
            p_el_initial = self.get_el_params()
            p_electronic = dt_fit_electronic(self.Vdata, p_el_initial,E,N,Ef)
            self.ui.lineEdit_el.setText(', '.join(['%.9e' % (p) for p in p_electronic]))


    def getfiles(self):
        # Open the file dialog and allow multiple file selection
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "",
            "All Files (*);;Text Files (*.txt);;Python Files (*.py)",
            options=options
        )

        files.sort()
        if files:
            print("Selected files:")
            for file in files:
                print(file)
        filepath = '; '.join(files)
        #filepath = QFileDialog.getExistingDirectory(self, caption='Select a folder')
        self.ui.filepath.setText(filepath)
        self.filepath_list = files

    def on_pushButton_OK(self):
        # self.filepath_list = self.ui.filepath.text()
        self.external_iparams.setText(self.ui.lineEdit_el.text())
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

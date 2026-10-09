from PySide6.QtWidgets import  QDialog, QFileDialog, QMessageBox
from debyetools.tpropsgui.ui_dialog_doscar import Ui_Dialog as Ui_DOSCAR

from debyetools.aux_functions import load_doscar as dt_load_doscar
from debyetools.electronic import fit_electronic as dt_fit_electronic

import numpy as np

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QPalette
from debyetools.constants import A3_ATOM_TO_M3_MOL, EV_ATOM_TO_J_MOL

def highlight_line_edit(line_edit, color="purple", duration=100):
    # Set the background color
    line_edit.setStyleSheet(f"background-color: {color};")

    # Create a QTimer to reset the color after `duration` milliseconds
    timer = QTimer(line_edit)
    timer.setSingleShot(True)  # Only trigger once
    timer.timeout.connect(lambda: line_edit.setStyleSheet(""))  # Reset the color
    timer.start(duration)




def doscar_volume(path: str) -> float:
    """Volume per atom (A^3) written by VASP as the first number of line 2 of a DOSCAR."""
    with open(path) as f:
        f.readline()
        return float(f.readline().split()[0])


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
            conv = [A3_ATOM_TO_M3_MOL, EV_ATOM_TO_J_MOL]  # debyetools.constants
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
        """
        Fit N(E_F)(V) to the selected DOSCARs. Each DOS is paired with the volume written in its own file
        (line 2, A^3/atom), so the file order does not matter (G5); the E(V) volumes of the EOS fit, when
        loaded, are only used as a cross-check.
        """
        files = list(getattr(self, 'filepath_list', None) or [])
        if not files:
            QMessageBox.information(self, 'Error', 'Select the DOSCAR files first.', QMessageBox.Ok)
            return
        try:
            vols_A3 = [doscar_volume(fi) for fi in files]
            order = sorted(range(len(files)), key=lambda i: vols_A3[i])
            files = [files[i] for i in order]
            Vs = np.array([vols_A3[i] for i in order]) * A3_ATOM_TO_M3_MOL
            E, N, Ef = dt_load_doscar('', list_filetags=files)
            p_electronic = dt_fit_electronic(Vs, None, E, N, Ef)
        except Exception as e:
            QMessageBox.information(self, 'Error', 'The electronic fit failed:\n%s' % e, QMessageBox.Ok)
            return
        self.ui.lineEdit_el.setText(', '.join(['%.9e' % (p) for p in p_electronic]))
        Vdata = getattr(self, 'Vdata', None)
        if Vdata is not None and len(Vdata) > 0:
            Vd = np.sort(np.asarray(Vdata, dtype=float))
            if len(Vd) != len(Vs):
                note = '%d DOSCAR files but %d E(V) points.' % (len(Vs), len(Vd))
            else:
                dev = float(np.max(np.abs(Vd / Vs - 1)))
                note = '' if dev < 1e-3 else 'DOSCAR volumes differ from the E(V) volumes by up to %.2g %% (check the units of the E(V) data).' % (100 * dev)
            if note:
                QMessageBox.information(self, 'Warning', 'Fit done with the volumes written in the DOSCARs.\n' + note,
                                        QMessageBox.Ok)


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

        try:  # list the files in order of volume (the order used by the fit), not alphabetically
            files = sorted(files, key=doscar_volume)
        except Exception:
            files = sorted(files)
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

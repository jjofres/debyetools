from PySide6.QtWidgets import QDialog, QMessageBox

from debyetools.tpropsgui.ui_dialog_fitEOS import Ui_Form as Ui_iparams

from debyetools.tpropsgui.atomtools import dt_potentials

import numpy as np

from debyetools.tpropsgui.dialog_loadEOS import dialogLoadEOS

from PySide6.QtCore import QTimer

from debyetools.tpropsgui.plot_EV import windowPlot
from PySide6.QtGui import QPixmap, QPalette


def highlight_line_edit(line_edit, color="purple", duration=100):
    # Set the background color
    line_edit.setStyleSheet(f"background-color: {color};")

    # Create a QTimer to reset the color after `duration` milliseconds
    timer = QTimer(line_edit)
    timer.setSingleShot(True)  # Only trigger once
    timer.timeout.connect(lambda: line_edit.setStyleSheet(""))  # Reset the color
    timer.start(duration)


def calculate_r_squared(y_obs, y_pred):
    """
    Calculate the coefficient of determination (R^2) between observed and predicted data.

    Parameters:
        y_obs (array-like): Observed data values.
        y_pred (array-like): Predicted data values.

    Returns:
        float: The R^2 value.
    """
    y_obs = np.array(y_obs)
    y_pred = np.array(y_pred)

    # Calculate SS_res and SS_tot
    ss_res = np.sum((y_obs - y_pred) ** 2)
    ss_tot = np.sum((y_obs - np.mean(y_obs)) ** 2)

    # Calculate R^2
    r_squared = 1 - (ss_res / ss_tot)

    return r_squared

class dialogFitEOS(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_iparams()
        self.ui.setupUi(self)

        self.ui.pushClose.clicked.connect(self.on_pushSave)
        self.ui.pushButton_2.clicked.connect(self.on_pushButton_fitEOS)
        self.ui.pushloadEvV.clicked.connect(self.on_pushloadEvV)

        self.dialog_loadEOS = dialogLoadEOS(self)

        # Connect the textChanged signals to a shared color change method
        self.ui.EvVText_2.textChanged.connect(lambda: self.on_text_changed(self.ui.EvVText_2))
        self.ui.lineEdit_3.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_3))

        self.plotwindow = windowPlot(self)
        self.ui.pushPlot.clicked.connect(self.plotEV)

    def get_EvV(self):
        if self.ui.radioButton_2.isChecked():
            conv = [(1e-30 * 6.02e23), (0.160218e-18 * 6.02214e23)]
        elif self.ui.radioButton_4.isChecked():
            conv = [1, 1]

        txt = self.ui.EvVText_2.toPlainText().split('\n')
        data_lst = []
        for ti in txt:
            if len(ti) == 0: continue
            if ti[0] == '#': continue
            data_lst.append([float(tii) for tii in ti.split()])
        data = np.array(data_lst)
        ncols = len(data.T)
        return (data[:, i] * conv[i] for i in range(ncols))

    def get_EOS_params(self):
        txt = self.ui.lineEdit_3.text()
        if txt == '':
            return -3e5, 9e-6, 7e10, 4
        return [float(ti) for ti in txt.replace(' ', '').split(',')]

    def on_pushloadEvV(self):
        self.dialog_loadEOS.mass = 0
        self.dialog_loadEOS.EvVtext = self.ui.EvVText_2
        self.dialog_loadEOS.show()


    def on_pushSave(self):
        current_text = self.ui.comboBox_2.currentText()
        self.external_combobox.setCurrentText(current_text)
        self.external_EOS_txt.setText(self.ui.lineEdit_3.text())
        self.close()

    def on_pushButton_fitEOS(self):
        dict_eos = {'Birch-Murnaghan': 'BM', 'Rose-Vinet': 'RV', 'Mie-Gruneisen': 'MG', 'TB-SMA': 'TB',
                    'Murnaghan': 'MU', 'Poirier-Tarantola': 'PT', 'Morse potential': 'MP',
                    'EAM int. potential': 'EAM'}
        current_text = self.ui.comboBox_2.currentText()

        self.eos_str = dict_eos[current_text]

        self.ui.progress_3.setValue(33)
        args = (None,)
        if self.eos_str == 'MP':
            print(self.molecule.__dir__())
            print(self.molecule_from_crystal.__dir__())
            self.molecule.formula, self.molecule.cell, self.molecule.basis, self.molecule.cutoff, self.molecule.number_of_NNs = self.molecule_from_crystal.formula, self.molecule_from_crystal.cell, self.molecule_from_crystal.basis, self.molecule_from_crystal.cutoff, self.molecule_from_crystal.number_of_NNs
            args = self.molecule.formula, self.molecule.cell, self.molecule.basis, self.molecule.cutoff, self.molecule.number_of_NNs
        self.eos = getattr(dt_potentials, self.eos_str)(*args)  # *self.ipotparamsdialog.args)

        try:
            Vdata, Edata = self.get_EvV()
        except Exception as e:
            print(e)
            error_msg = 'Something is wrong with the data for energy versus volume.\n Please check and try again.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)


        self.Vdata = Vdata
        self.Edata = Edata

        initial_guess = self.get_EOS_params()
        self.eos.fitEOS(Vdata, Edata, initial_parameters=initial_guess, fit=True)

        self.ui.lineEdit_3.setText(', '.join(['%.9e' % (p) for p in self.eos.pEOS]))

        self.ui.progress_3.setValue(100)

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



    def plotEV(self):
        try:

            Xdata = self.Vdata/1e-5
            Ydata = self.Edata/1e3

            self.plotwindow.ax.cla()
            self.plotwindow.ax.plot(Xdata, Ydata, ls = '', marker='.', label = 'data', mfc='None', mec='black', markersize=10,mew=1)
            self.plotwindow.ax.plot(Xdata, [self.eos.E0(Vi)/1e3 for Vi in Xdata*1e-5], ls = '', marker='+', label = 'model', mfc='purple', mec='purple', markersize=10,mew=1)

            err = calculate_r_squared(Ydata, [self.eos.E0(Vi)/1e3 for Vi in Xdata*1e-5])
            self.plotwindow.ax.set_title(r'$R^2$ = ' + f'{err:.5f}')
            spanX = (max(Xdata) - min(Xdata))/20
            spanY = (max(Ydata) - min(Ydata))/20
            self.plotwindow.ax.set_xlim((min(Xdata)-spanX, max(Xdata)+spanX))
            self.plotwindow.ax.set_ylim((min(Ydata)-spanY, max(Ydata)+spanY))
            self.plotwindow.ax.legend(loc=9)
            self.plotwindow.ax.set_xlabel(r'$10^{-5}m^3/mol$-$at$')
            self.plotwindow.ax.set_ylabel(r'$kJ/mol$-$at$')

            self.plotwindow.show()
        except:
            # Create a message box
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Warning")
            msg_box.setText("Data not entered yet.\nPlease run the fitting first.")

            # Add Yes and No buttons
            msg_box.setStandardButtons(QMessageBox.Ok)
            response = msg_box.exec_()

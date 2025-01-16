import re
import traceback

import numpy as np
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QMessageBox
from debyetools.poisson import poisson_ratio as dt_poisson_ratio

from debyetools.tpropsgui.atomtools import dt_potentials, Molecule
from debyetools.tpropsgui.cp_window import dialogCpWindow
from debyetools.tpropsgui.ui_main_window_small import Ui_MainWindow

from debyetools.tpropsgui.dialog_fitEOS import dialogFitEOS
from debyetools.tpropsgui.dialog_calculateNu import dialogCalcNu
from debyetools.tpropsgui.dialog_doscar import dialogDoscar
from PySide6.QtCore import QTimer

from PySide6.QtGui import QPixmap, QPalette
from matplotlib import pyplot as plt
import sys
import io

from PySide6.QtCore import QByteArray, QBuffer
import base64

def pixmap_to_base64(pixmap):
    # Convert QPixmap to QByteArray
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QBuffer.WriteOnly)
    pixmap.save(buffer, "PNG")  # Save the QPixmap to buffer as PNG
    buffer.close()
    # Encode QByteArray to base64 and decode to string for HTML embedding
    return byte_array.toBase64().data().decode()

# Updated `create_latex_image` function as before
def create_latex_image(latex_str, color):

    plt.figure(figsize=(2, 1))
    plt.text(0.1, 0.1, f"{latex_str}", fontsize=12, ha='left', va='center', c=color)
    plt.axis('off')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    buffer.seek(0)

    pixmap = QPixmap()
    success = pixmap.loadFromData(buffer.getvalue())
    if not success:
        raise ValueError("Failed to load LaTeX image into QPixmap.")
    return pixmap


def highlight_line_edit(line_edit, color="purple", duration=100):
    # Set the background color
    line_edit.setStyleSheet(f"background-color: {color};")

    # Create a QTimer to reset the color after `duration` milliseconds
    timer = QTimer(line_edit)
    timer.setSingleShot(True)  # Only trigger once
    timer.timeout.connect(lambda: line_edit.setStyleSheet(""))  # Reset the color
    timer.start(duration)

def separate_atoms(formula):
    # This pattern matches element symbols (one or two letters, starting with an uppercase letter)
    # followed by optional counts (numbers)
    pattern = r"([A-Z][a-z]*)(\d*)"
    elements = re.findall(pattern, formula)
    separated = []

    for element, count in elements:
        # If count is empty, it means there is one atom of this element
        count = int(count) if count else 1
        separated.extend([element] * count)

    return separated


class dialogMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        my_icon = QIcon()
        my_icon.addFile('icon.ico')

        self.setWindowIcon(my_icon)

        self.cp_window = dialogCpWindow(self)

        self.ui.pushButton_5.clicked.connect(self.on_pushButton_Cp)
        self.ui.pushgoback.clicked.connect(self.on_pushButton_goback)

        self.eos_str = 'BM'

        self.molecule = Molecule()

        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)

        self.check_el, self.check_def, self.check_anh, self.check_xs = self.ui.checkBox, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4
        self.check_xspol = self.ui.checkBox_5

        self.state_el = False
        self.state_def = False
        self.state_anh = False
        self.state_xs = False
        self.state_xspol = False

        self.check_el.stateChanged.connect(self.on_check_el)
        self.check_def.stateChanged.connect(self.on_check_def)
        self.check_anh.stateChanged.connect(self.on_check_anh)
        self.check_xs.stateChanged.connect(self.on_check_xs)
        self.check_xspol.stateChanged.connect(self.on_check_xspol)

        self.dialogFitEOS = dialogFitEOS(self)
        self.dialogCalcNu = dialogCalcNu(self)

        self.ui.pushFitEOS.clicked.connect(self.on_pushFitEOS)

        self.ui.pushNu.clicked.connect(self.on_pushNu)

        self.ui.pushDoscar.clicked.connect(self.on_pushDoscar)

        self.dialogDoscar = dialogDoscar(self)

        self.ui.lineEdit.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit))
        self.ui.lineEdit_2.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_2))
        self.ui.lineEdit_3.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_3))
        self.ui.lineEdit_11.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_11))
        self.ui.lineEdit_el.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_el))
        self.ui.lineEdit_def.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_def))
        self.ui.lineEdit_anh.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_anh))
        self.ui.lineEdit_xs.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_xs))
        self.ui.lineEdit_xspol.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_xspol))
        self.ui.lineEdit_T.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_T))
        self.ui.lineEdit_P.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_P))

        # Generate LaTeX image and display it in tooltip
        # Usage in the main code
        latex_string = '- Birch-Murnaghan:\n' + r"    $E(V) = \left(-\frac{9}{16} V_0 B_0 B'_0 + \frac{27}{8} V_0 B_0 + E_0\right) + \frac{\frac{27}{16} V_0^{5/3} B_0 B'_0 - 9 V_0^{5/3} B_0}{V^{2/3}} + \frac{-\frac{27}{16} V_0^{7/3} B_0 B'_0 + \frac{63}{8} V_0^{7/3} B_0}{V^{4/3}} + \frac{\frac{9}{16} V_0^3 B_0 B'_0 - \frac{9}{4} V_0^3 B_0}{V^2}$" + \
        '\n- Rose-Vinet:\n' + r"    $E(V) = E_0 - \frac{2 B_0 V_0 \exp\left(-\frac{3}{2}(B'_0 - 1) \left(-1 + \left(\frac{V}{V_0}\right)^{\frac{1}{3}}\right)\right)}{(B'_0 - 1)^2} \left( 3 \left(\frac{V}{V_0}\right)^{\frac{1}{3}} B'_0 - 3 B'_0 - 3 \left(\frac{V}{V_0}\right)^{\frac{1}{3}} + 5 \right) + \frac{4 B_0 V_0}{(B'_0 - 1)^2}$" + \
        '\n- Mie-Gruneisen:\n' + r"    $E(V) = \frac{9 \left( 3 \left( B_0 V_0 + \frac{1}{3} B'_0 E_0 - \frac{7}{9} E_0 \right) \left( B'_0 - \frac{8}{3} \right) \left( \frac{V}{V_0} \right)^{\frac{1}{3}} + B_0 V_0 \left( \left( \frac{V}{V_0} \right)^{\frac{8}{3} - B'_0} - 3 B'_0 + 7 \right) \right)}{\left( \frac{V}{V_0} \right)^{\frac{1}{3}} \left( 9 {B'_0}^2 - 45 B'_0 + 56 \right)}$"+\
        '\n- TB-SMA:\n' + r"    $E(V) = -\frac{X_x \exp\left(3 B'_0 - 3 - \frac{X_x}{2 E_0}\right)}{2 \left(3 B'_0 - 3 - \frac{X_x}{E_0}\right)} \cdot \exp\left(-\frac{3 B'_0 - 3 - \frac{X_x}{2 E_0}}{V_0^{1/3}} V^{1/3}\right) + \frac{E_0 \left(3 B'_0 - 3 - \frac{X_x}{2 E_0}\right) \exp\left(\frac{X_x}{2 E_0}\right)}{3 B'_0 - 3 - \frac{X_x}{E_0}} \cdot \exp\left(-\frac{X_x}{2 E_0 V_0^{1/3}} V^{1/3}\right)$" + \
        '\n- Murnaghan:\n' + r"    $E(V) = E_0 + \frac{B_0 V_0}{B'_0 (B'_0 - 1)} \left( \frac{V}{V_0} \right)^{1 - B'_0} + \frac{B_0}{B'_0} V - \frac{B_0 V_0}{B'_0 - 1}$" + \
        '\n- Poirier-Tarantola:\n' + r"    $E(V) = E_0 + \frac{1}{2} B_0 V_0 \left( \ln \frac{V}{V_0} \right)^2 - \frac{1}{6} B_0 V_0 \left( B'_0 - 2 \right) \left( \ln \frac{V}{V_0} \right)^3$" + \
        '\n- Morse interatomic potential:\n' + r"    $E\left(V\right) = \sum_{ij}D_i\cdot\left(2e^{2\alpha_i (r_j-r^0_{ij})} - e^{-\alpha (r_j-r^0_{ij})}\right)$" + \
        '\n- Embeded-Atom model interatomic potential:\n' + r"    $E(V)=\sum_{i}F_{i}\left(\rho_{h,i}\right)+\frac{1}{2}\sum_{i\neq j}\phi_{ij}\left(R_{ij}\right)$"


        # Check if the system is in dark mode by detecting the background color
        dark_mode = self.is_dark_mode()
        color = "white" if dark_mode else "black"
        latex_pixmap = create_latex_image(latex_string, color)
        base64_image = pixmap_to_base64(latex_pixmap)
        tooltip_html = f'<img src="data:image/png;base64,{base64_image}">'
        self.ui.moreinfo.setToolTip(tooltip_html)

    def is_dark_mode(self):
        # Detect if the application is in dark mode using the palette
        palette = self.palette()
        return palette.color(QPalette.ColorRole.Window).value() < 128  # Lightness threshold for dark mode


    def selectionchange(self, i):
        # self.ui.progress_2.setValue(0)
        dict_eos = {'Birch-Murnaghan': 'BM', 'Rose-Vinet': 'RV', 'Mie-Gruneisen': 'MG', 'TB-SMA': 'TB',
                    'Murnaghan': 'MU', 'Poirier-Tarantola': 'PT', 'Morse potential': 'MP',
                    'EAM int. potential': 'EAM'}
        self.eos_str = dict_eos[self.ui.comboBox.itemText(i)]

        self.ui.lineEdit_2.setText('-3e5, 1e-5, 7e10, 4')

    def get_C(self):
        txt = self.ui.elastic_constants.toPlainText().replace('XX', ' ').replace('YY', ' ').replace('ZZ', ' ').replace(
            'XY', ' ').replace('YZ', ' ').replace('ZX', ' ').split('\n')
        data_lst = []
        for ti in txt:
            if len(ti) == 0: continue
            if ti[0] == '#': continue
            data_lst.append([float(tii) for tii in ti.replace('\t', ' ').split()])
        data = np.array(data_lst)

        return data

    def on_check_el(self):
        self.state_el = self.check_el.isChecked()
        self.ui.lineEdit_el.setEnabled(self.state_el)

    def on_check_def(self):
        self.state_def = self.check_def.isChecked()
        self.ui.lineEdit_def.setEnabled(self.state_def)

    def on_check_anh(self):
        self.state_anh = self.check_anh.isChecked()
        self.ui.lineEdit_anh.setEnabled(self.state_anh)

    def on_check_xs(self):
        self.state_xs = self.check_xs.isChecked()
        self.ui.lineEdit_xs.setEnabled(self.state_xs)

    def on_check_xspol(self):
        self.state_xspol = self.check_xspol.isChecked()
        self.ui.lineEdit_xspol.setEnabled(self.state_xspol)


    def on_pushButton_goback(self):
        self.close()


    def on_pushNu(self):
        self.dialogCalcNu.external_nu = self.ui.lineEdit_3
        self.dialogCalcNu.show()

    def on_pushFitEOS(self):
        # print(self.ui.lineEdit_2.text())
        self.dialogFitEOS.external_combobox = self.ui.comboBox
        self.dialogFitEOS.external_EOS_txt = self.ui.lineEdit_2
        self.dialogFitEOS.ui.lineEdit_3.setText(self.ui.lineEdit_2.text())
        list_items_in_combox = [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]
        # print(list_items_in_combox)

        self.dialogFitEOS.ui.comboBox_2.clear()
        for item_cb in list_items_in_combox:
            self.dialogFitEOS.ui.comboBox_2.addItem(item_cb)


        # print('CI', self.ui.comboBox.currentIndex())
        self.dialogFitEOS.ui.comboBox_2.setCurrentText(list_items_in_combox[self.ui.comboBox.currentIndex()])
        self.dialogFitEOS.molecule = self.molecule
        if self.eos_str == 'MP':
            self.dialogFitEOS.molecule_from_crystal = self.molecule_from_crystal



        self.dialogFitEOS.show()



    def on_pushButton_Cp(self):
        self.cp_window.app=self.app

        self.was_Cp_calculated = True
        pattern = r'[A-Z][a-z]?'
        error_msg = ''
        try:
            formula_comp = self.ui.lineEdit_11.text()
            self.molecule.r = len(set(re.findall(pattern, formula_comp)))
            self.molecule.nu = float(self.ui.lineEdit_3.text())
            self.molecule.mass = float(self.ui.lineEdit.text())

            self.molecule.p_anh = [float(si) for si in
                                   self.ui.lineEdit_anh.text().replace(',', ' ').split()] if self.state_anh else [0, 1]
            self.molecule.p_el = [float(si) for si in
                                  self.ui.lineEdit_el.text().replace(',', ' ').split()] if self.state_el else [0, 0, 0,
                                                                                                               0]
            self.molecule.p_def = [float(si) for si in
                                   self.ui.lineEdit_def.text().replace(',', ' ').split()] if self.state_def else [100,
                                                                                                                  1,
                                                                                                                  1000,
                                                                                                                  0.1]
            self.molecule.p_xs = [float(si) for si in
                                  self.ui.lineEdit_xs.text().replace(',', ' ').split()] if self.state_xs else [0, 0, 0]

            self.molecule.initial_params = [float(si) for si in self.ui.lineEdit_2.text().replace(',', ' ').split()]

            self.molecule.xsparams = [float(si) for si in
            self.ui.lineEdit_xspol.text().replace(',', ' ').split()] if self.state_xs else [0, 0, 0, 0, 0, 0]

            if self.eos_str in ['MP', 'EAM']:

                for karg in ['cell', 'basis', 'types', 'formula', 'number_of_NNs', 'cutoff', 'distances', 'num_bonds_per_formula', 'combs_types']:
                    setattr(self.molecule, karg, getattr(self.molecule_from_crystal, karg))

                args = [self.molecule.formula, self.molecule.cell, self.molecule.basis, self.molecule.cutoff,
                        self.molecule.number_of_NNs]
            else:
                args = [None]
            self.molecule.set_eos(self.eos_str, args)

            self.cp_window.ui.lineEdit.setText(self.ui.lineEdit_T.text())
            self.cp_window.ui.lineEdit_2.setText(self.ui.lineEdit_P.text())

            types = separate_atoms(self.ui.lineEdit_11.text())
            self.molecule.update_fomula(types)
            self.cp_window.debye_run(self.molecule, self.ui.progress, self.ui.lineEdit_11.text())
            self.cp_window.show()
        except Exception as e:
            print(e)
            error_message = f"An error occurred: {e}\n"
            error_traceback = traceback.format_exc()

            # Combine the error message with the traceback
            full_error_text = error_message + error_traceback
            print(full_error_text)


            if 'self.molecule.nu' in full_error_text:
                error_msg = "Something is wrong with the Poisson's ratio."
            elif 'self.molecule.mass' in full_error_text:
                error_msg = "Something is wrong with the mass."
            elif 'E0, V0, B0, Bp0 = pEOS' in full_error_text:
                error_msg = "Something is wrong with the EOS's parameters."
            elif 'q0, q1, q2, q3 = p_electronic' in full_error_text:
                error_msg = "Something is wrong with the parameters for the electronic contribution."
            elif 'self.molecule.p_el' in full_error_text:
                error_msg = "Something is wrong with the parameters for the electronic contribution."

            if error_msg == '':
                error_msg = full_error_text
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)

    def on_pushDoscar(self):
        status = 0
        try:
            self.dialogDoscar.Vdata = self.dialogFitEOS.Vdata
            status =1
        except AttributeError:
            QMessageBox.information(self, 'Warning', 'The volume data was not loaded!\n Please make sure you run the EOS fitting first.', QMessageBox.Ok)
        if status == 1:
            self.dialogDoscar.external_iparams = self.ui.lineEdit_el
            self.dialogDoscar.show()

    def on_text_changed(self, line_edit):
        # Call the reusable highlight function
        dark_mode = self.is_dark_mode()
        color_p = "purple" if dark_mode else "#94a2c9"

        highlight_line_edit(line_edit, color=color_p, duration=500)



from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from debyetools.tpropsgui.dialog_doscar import dialogDOSCAR
from debyetools.tpropsgui.dialog_summary import dialogSUMMARY
from debyetools.tpropsgui.dialog_outcar import dialogOUTCAR
from debyetools.tpropsgui.dialog_warning import dialogWarning
from debyetools.tpropsgui.window_cp import windowCp
from debyetools.tpropsgui.window_interatomicparams import windowInteratormic
from debyetools.tpropsgui.plot_EV import windowPlot

from debyetools.tpropsgui.ui_mainwindow import Ui_MainWindow as Ui_MW
from debyetools.tpropsgui.ui_missingkey import Ui_Form as Ui_KEY

from debyetools.tpropsgui.atomtools import Molecule, dt_potentials

import numpy as np

from debyetools.poisson import poisson_ratio as dt_poisson_ratio
from debyetools.aux_functions import load_doscar as dt_load_doscar
from debyetools.electronic import fit_electronic as dt_fit_electronic

from debyetools.tpropsgui.lock import keygen as kg

class MainWindow(QMainWindow):
    def __init__(self, parent=None, app=None):

        super().__init__(parent)

        key1 = kg()
        try:
            f = open('debyetools/tpropsgui/keydtgl','r')
            key0 = f.read().replace('\n','')
        except:
            key0=''
            passed=False
        if key0 != key1:
            passed = False
        else:
            passed = True

        if passed:
            self.ui = Ui_MW()
        else:
            self.ui = Ui_KEY()
            self.ui.setupUi(self)
            return

        self.ui.setupUi(self)
        my_icon = QIcon()
        my_icon.addFile('icon.ico')

        self.setWindowIcon(my_icon)

        self.cp_window = windowCp(self)
        self.cp_window.app = app
        self.doscardialog = dialogDOSCAR(self)
        self.summarydialog = dialogSUMMARY(self)
        self.outcardialog = dialogOUTCAR(self)
        self.warningdialog = dialogWarning(self)

        self.ui.pushButton.clicked.connect(self.on_pushButton_fitEOS)
        self.ui.pushButton_5.clicked.connect(self.on_pushButton_Cp)
        self.ui.pushButton_2.clicked.connect(self.on_pushButton_calc_nu)

        self.ui.pushButton_3.clicked.connect(self.on_pushButton_calculate_el)

        self.eos_str = 'BM'

        self.molecule = Molecule()

        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)


        self.check_el, self.check_def, self.check_anh, self.check_xs = self.ui.checkBox, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4

        self.state_el = False
        self.state_def = False
        self.state_anh = False
        self.state_xs = False

        self.check_el.stateChanged.connect(self.on_check_el)
        self.check_def.stateChanged.connect(self.on_check_def)
        self.check_anh.stateChanged.connect(self.on_check_anh)
        self.check_xs.stateChanged.connect(self.on_check_xs)

        self.ui.progress.setGeometry(450, 525, 80, 5)
        self.ui.progress_2.setGeometry(260, 165, 80, 5)

        self.ipotparamsdialog = windowInteratormic(self)
        self.ipotparamsdialog.args = (None,)
        self.ipotparamsdialog.external_params_lineText = self.ui.lineEdit_2

        self.plotwindow = windowPlot(self)
        self.ui.actionEV.triggered.connect(self.plotEV)

        self.ui.actionDOSCAR.triggered.connect(self.on_pushButton_loaddata)
        self.ui.actionSUMMARY.triggered.connect(self.on_pushButton_loadSUMMARY)
        self.ui.actionOUTCAR.triggered.connect(self.on_pushButton_loadOUTCAR)

    def plotEV(self):
        Xdata = self.Vdata/1e-5
        Ydata = self.Edata/1e3
        self.plotwindow.ax.cla()
        self.plotwindow.ax.plot(Xdata, Ydata, ls = '', marker='.', label = 'data', mfc='None', mec='black', markersize=10,mew=1)
        self.plotwindow.ax.plot(Xdata, [self.eos.E0(Vi)/1e3 for Vi in Xdata*1e-5], ls = '', marker='+', label = 'model', mfc='purple', mec='purple', markersize=10,mew=1)

        spanX = (max(Xdata) - min(Xdata))/20
        spanY = (max(Ydata) - min(Ydata))/20
        self.plotwindow.ax.set_xlim((min(Xdata)-spanX, max(Xdata)+spanX))
        self.plotwindow.ax.set_ylim((min(Ydata)-spanY, max(Ydata)+spanY))
        self.plotwindow.ax.legend(loc=9)
        self.plotwindow.ax.set_xlabel(r'$10^{-5}m^3/mol$-$at$')
        self.plotwindow.ax.set_ylabel(r'$kJ/mol$-$at$')
        self.plotwindow.show()

    def selectionchange(self, i):
        self.ui.progress_2.setValue(0)
        dict_eos = {'Birch-Murnaghan':'BM', 'Rose-Vinet':'RV', 'Mie-Gruneisen':'MG', 'TB-SMA':'TB',
                    'Murnaghan':'MU', 'Poirier-Tarantola':'PT', 'Morse int. potential':'MP', 'EAM int. potential':'EAM'}
        self.eos_str = dict_eos[self.ui.comboBox.itemText(i)]

        self.ipotparamsdialog.args = (None,)
        self.ui.lineEdit_2.setText('-3e5, 1e-5, 7e10, 4')
        if self.eos_str in ['MP', 'EAM']:
            self.ipotparamsdialog.ui.plainTextEdit.setPlainText('')
            for axi in self.ipotparamsdialog.ax:
                for line in axi.lines:
                    line.remove()

                self.ipotparamsdialog.ax[0].figure.canvas.draw()
            self.ipotparamsdialog.molecule = self.molecule
            self.ipotparamsdialog.eos_str = self.eos_str
            self.ipotparamsdialog.ui.OKbutton.setEnabled(False)
            self.ipotparamsdialog.show()

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

    def get_EOS_params(self):
        txt = self.ui.lineEdit_2.text()
        if txt=='':
            return -3e5,9e-6,7e10,4
        return  [float(ti) for ti in txt.replace(' ','').split(',')]

    def get_el_params(self):
        txt = self.ui.lineEdit_el.text()
        if txt=='':
            return 3e-01, -1e+04, 5e-04, 1e-06
        return  [float(ti) for ti in txt.replace(' ','').split(',')]

    def get_C(self):
        txt = self.ui.elastic_constants.toPlainText().replace('XX',' ').replace('YY',' ').replace('ZZ',' ').replace('XY',' ').replace('YZ',' ').replace('ZX',' ').split('\n')
        data_lst = []
        for ti in txt:
            if len(ti)==0:continue
            if ti[0]=='#': continue
            data_lst.append([float(tii) for tii in ti.replace('\t',' ').split()])
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

    def on_pushButton_fitEOS(self):
        self.ui.progress_2.setValue(33)
        self.eos = getattr(dt_potentials, self.eos_str)(*self.ipotparamsdialog.args)

        Vdata, Edata = self.get_EvV()
        self.Vdata = Vdata
        self.Edata = Edata

        initial_guess = self.get_EOS_params()
        self.eos.fitEOS(Vdata, Edata, initial_parameters = initial_guess, fit=True)

        self.ui.lineEdit_2.setText(', '.join(['%.9e' % (p) for p in self.eos.pEOS]))
        self.ui.progress_2.setValue(100)

    def on_pushButton_calc_nu(self):
        C = self.get_C()
        BR, BV, B, GR, GV, S, AU, nu = dt_poisson_ratio(C, quiet=True)
        self.ui.lineEdit_3.setText('%.3f'%(nu))
        self.ui.lineEdit_4.setText('%.1f'%(BR*10))
        self.ui.lineEdit_5.setText('%.1f'%(BV*10))
        self.ui.lineEdit_6.setText('%.1f'%(B*10))
        self.ui.lineEdit_9.setText('%.1f'%(GR*10))
        self.ui.lineEdit_8.setText('%.1f'%(GV*10))
        self.ui.lineEdit_7.setText('%.1f'%(S*10))
        self.ui.lineEdit_10.setText('%.2f'%(AU))

    def on_pushButton_Cp(self):
        self.molecule.nu = float(self.ui.lineEdit_3.text())
        self.molecule.mass = float(self.ui.lineEdit.text())

        self.molecule.p_anh = [float(si) for si in self.ui.lineEdit_anh.text().replace(',',' ').split()] if self.state_anh else [0,1]
        self.molecule.p_el = [float(si) for si in self.ui.lineEdit_el.text().replace(',',' ').split()] if self.state_el else [0,0,0,0]
        self.molecule.p_def = [float(si) for si in self.ui.lineEdit_def.text().replace(',',' ').split()] if self.state_def else [100, 1, 1000, 0.1]
        self.molecule.p_xs = [float(si) for si in self.ui.lineEdit_xs.text().replace(',',' ').split()] if self.state_xs else [0,0,0]

        self.molecule.initial_params = [float(si) for si in self.ui.lineEdit_2.text().replace(',',' ').split()]

        if self.eos_str in ['MP','EAM']:
            args = [self.molecule.formula, self.molecule.cell, self.molecule.basis, self.molecule.cutoff, self.molecule.number_of_NNs]
        else:
            args = [None]
        self.molecule.set_eos(self.eos_str, args)


        self.cp_window.debye_run(self.molecule, self.ui.progress)
        self.cp_window.show()

    def on_pushButton_loaddata(self):
        self.doscardialog.show()

    def on_pushButton_loadSUMMARY(self):
        self.summarydialog.mass = self.ui.lineEdit
        self.summarydialog.EvVtext = self.ui.EvVText
        self.summarydialog.show()

    def on_pushButton_loadOUTCAR(self):
        self.outcardialog.elastic_constants = self.ui.elastic_constants
        self.outcardialog.show()

    def on_pushButton_calculate_el(self):
        Vdata, Edata = self.get_EvV()
        self.Vdata = Vdata
        try:
            E, N, Ef = dt_load_doscar(self.doscardialog.filepath+'/DOSCAR.', list_filetags = [i+1 for i in range(len(Vdata))])
            p_el_initial = self.get_el_params()
            p_electronic = dt_fit_electronic(self.Vdata, p_el_initial,E,N,Ef)
            self.ui.lineEdit_el.setText(', '.join(['%.9e' % (p) for p in p_electronic]))
        except Exception as e:
            print(e)
            self.warningdialog.ui.label.setText(str(e)+"\n\nProbably you haven't set a filepath to the eDOS data yet.")
            self.warningdialog.show()
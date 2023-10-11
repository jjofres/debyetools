from PySide6.QtWidgets import  QDialog, QFileDialog
from debyetools.tpropsgui.ui_dialogSUMMARY import Ui_Dialog as Ui_SUMMARY
from debyetools.tpropsgui.atomtools import atomic_mass
from debyetools.aux_functions import load_V_E as dt_load_V_E

def log_mean(lst):
    import numpy as np
    l = len(lst)
    lm = np.sum([np.log(li)/l for li in lst])
    m = np.exp(lm)
    return m
class dialogSUMMARY(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SUMMARY()
        self.ui.setupUi(self)

        self.ui.browsesummary.clicked.connect(self.getfilessummary)
        self.ui.browseposcar.clicked.connect(self.getfilesposcar)
        self.ui.ok.clicked.connect(self.on_pushButton_OK)
        self.filepath='.'

    def getfilessummary(self):
        summarypath, _ = QFileDialog.getOpenFileName(self, caption='Select a SUMMARY file')
        self.ui.summarypath.setText(summarypath)
        self.summarypath = summarypath

    def getfilesposcar(self):
        poscarpath, _ = QFileDialog.getOpenFileName(self, caption='Select a POSCAR or CONTCAR file')
        self.ui.poscarpath.setText(poscarpath)
        self.poscarpath = poscarpath

    def on_pushButton_OK(self):
        self.summarypath = self.ui.summarypath.text()
        self.poscarpath = self.ui.poscarpath.text()
        self.close()

    def closeEvent(self, event):
        V, E = dt_load_V_E(self.summarypath, self.poscarpath)
        with open(self.poscarpath) as f:
            poscar_lines = f.readlines()
        elmnts = poscar_lines[5].split()
        mult = poscar_lines[6].split()
        elmntsall = []
        for e, m in zip(elmnts, mult):
            elmntsall = elmntsall + [e]*int(m)
        masses = [float(atomic_mass[e])/100. for e in elmntsall]
#        print(elmntsall, masses, log_mean(masses))
        txt2paste = '#V\tE\n'
        for v, e in zip(V, E):
            txt2paste = txt2paste + '%.6e\t%.6e'%(v, e)+'\n'
        self.EvVtext.setPlainText(txt2paste)
        self.mass.setText(str(log_mean(masses)))
#        print('event', event)

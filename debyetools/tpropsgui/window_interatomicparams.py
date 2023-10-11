from PySide6.QtWidgets import QMainWindow

from debyetools.tpropsgui.ui_interatomic_params import Ui_Form as Ui_iparams

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

import debyetools.tpropsgui.get_functions as get
from debyetools.tpropsgui.atomtools import atomic_color, atomic_radii, atomsPositions

def print_to_box(ptedit, txt=''):
    txt = ptedit.toPlainText()+txt
    ptedit.setPlainText(txt)
    ptedit.verticalScrollBar().setValue(ptedit.verticalScrollBar().maximum())

class windowInteratormic(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_iparams()
        self.ui.setupUi(self)

        self.cellparamsTable = self.ui.tableWidget
        self.basisTable = self.ui.tableWidget_2

        self.fig = Figure(figsize=(3, 3))
        self.canvas = FigureCanvas(self.fig)
        self.canvas_configuration()

        llayout = self.ui.horizontalLayout
        llayout.addWidget(self.canvas, 88)

        self.ui.pushButton.clicked.connect(self.on_pushButton_create_cell_clicked)
        self.ui.OKbutton.clicked.connect(self.close)

    def canvas_configuration(self):
        self.fig.set_canvas(self.canvas)

        self.ax = []
        for i in range(4):
            self.ax.append(self.canvas.figure.add_subplot(2, 2, i+1))

        for axi in self.ax:
            axi.set_axis_off()

        self.fig.subplots_adjust(hspace=0.05, right=0.99, top=.99, bottom=.01, left=0.01, wspace=0.05)

    def on_pushButton_create_cell_clicked(self):
        self.molecule.cell = get.cell(self)
        self.molecule.basis = get.basis(self)
        self.molecule.update_fomula(get.formula(self))

        self.plot_cell()


        cutoff = int(self.ui.lineEdit.text())
        self.molecule.run_pa(cutoff)
#        print('bkp1')

        ds, ns, cts = self.molecule.distances, self.molecule.num_bonds_per_formula, self.molecule.combs_types

        self.ui.plainTextEdit.setPlainText('')
        print_to_box(self.ui.plainTextEdit,'Pair analysis:\n')
        print_to_box(self.ui.plainTextEdit,'distances  | # of pairs per type\n')
        print_to_box(self.ui.plainTextEdit,'           | ' + '  '.join(['%s' for _ in cts])%tuple(cts)+'\n')
        for d, n in zip(ds, ns):
            print_to_box(self.ui.plainTextEdit,'%.6f  '%(d)+' | ' + ' '.join(['%.2f' for _ in n])%tuple(n)+'\n')

        a, b, c = 0.5, 0.5, -len(cts)
        ntypes =(-b+np.sqrt(b**2-4*a*c))/(2*a)
        if self.eos_str == 'MP':
            params = [0.35, 1, 3.2]*len(cts)
        elif self.eos_str == 'EAM':
            params = [3.65e-03, 1.24e-02, 2.68e-04, 1.03e-02,
                        1.49e-01, 5.22e-02]*len(cts)+[2.26e+00,
                        6.61e-02, 3.01e-01, 5.31e-05]*int(ntypes)

        params = ', '.join([str(pi) for pi in params])
        self.params_interatomic = ', '.join([params for _ in range(len(cts))])

        self.ui.lineEdit_3.setText(self.params_interatomic)

        self.ui.OKbutton.setEnabled(True)

    def plot_atom_xy(self, ax, atom_position, atom_type):
        x, y, z = atom_position
        ax.plot(x, y, marker='o', mfc=atomic_color[atom_type], mec='black', ms=10*atomic_radii[atom_type])
    def plot_atom_xz(self, ax, atom_position, atom_type):
        x, y, z = atom_position
        ax.plot(x, -z, marker='o', mfc=atomic_color[atom_type], mec='black', ms=10*atomic_radii[atom_type])
    def plot_atom_yz(self, ax, atom_position, atom_type):
        x, y, z = atom_position
        ax.plot(-z, y, marker='o', mfc=atomic_color[atom_type], mec='black', ms=10*atomic_radii[atom_type])

    def plot_cell_xy(self, ax, cell):
        x, y = self.gen_cell_points_xy(cell)
        ax.plot(x, y, linestyle='--', color='gray', linewidth=1)
    def plot_cell_xz(self, ax, cell):
        x, y = self.gen_cell_points_xz(cell)
        ax.plot(x, -1*np.array(y), linestyle='--', color='gray', linewidth=1)
    def plot_cell_yz(self, ax, cell):
        y, z = self.gen_cell_points_yz(cell)
        ax.plot(-1*np.array(z), y, linestyle='--', color='gray', linewidth=1)

    def gen_cell_points_xy(self, cell):
        xbox1 = [
         0, #1
         cell[0, 0], #2
         cell[0, 0] + cell[1, 0], #5
         cell[1, 0], #3
         0, #1
         ]
        ybox1 = [
        0, #1
        cell[0, 1], #2
        cell[0, 1] + cell[1, 1], #5
        cell[1, 1], #3
        0, #1
        ]

        return xbox1, ybox1

    def gen_cell_points_xz(self, cell):
        xbox1 = [
         0, #1
         cell[0, 0], #2
         cell[0, 0] + cell[2, 0], #6
         cell[2, 0], #4
         0, #1
        ]
        zbox1 = [
         0, #1
         cell[0, 2], #2
         cell[0, 2] + cell[2, 2], #6
         cell[2, 2], #4
         0, #1
        ]
        return xbox1, zbox1

    def gen_cell_points_yz(self, cell):
        ybox1 = [
         0, #1
         cell[1, 1], #3
         cell[1, 1] + cell[2, 1], #7
         cell[2, 1], #4
         0, #1
        ]
        zbox1 = [
         0, #1
         cell[1, 2], #3
         cell[1, 2] + cell[2, 2], #7
         cell[2, 2], #4
         0, #1
        ]

        return ybox1, zbox1

    def plot_cell(self):
        for axi in self.ax:
            axi.cla()
            axi.set_axis_off()

        atoms = atomsPositions(self.molecule.formula, self.molecule.cell, self.molecule.basis)

        for ai in atoms:
            self.plot_atom_xz(self.ax[3], ai.position, ai.type)
        self.plot_cell_xz(self.ax[3], self.molecule.cell)
        for ai in atoms:
            self.plot_atom_xy(self.ax[1], ai.position, ai.type)
        self.plot_cell_xy(self.ax[1], self.molecule.cell)

        for ai in atoms:
            self.plot_atom_yz(self.ax[0], ai.position, ai.type)
        self.plot_cell_yz(self.ax[0], self.molecule.cell)


        self.ax[1].plot([-0.5,0.5],[-0.5,-0.5], 'b', linewidth=1)
        self.ax[1].plot([-0.5,-0.5],[-0.5,0.5], 'r', linewidth=1)

        self.ax[0].plot([0.5,0.5],[-0.5,0.5], 'r', linewidth=1)
        self.ax[0].plot([0.5,-0.5],[-0.5,-0.5], 'g', linewidth=1)

        self.ax[3].plot([-0.5,0.5],[0.5,0.5], 'b', linewidth=1)
        self.ax[3].plot([-0.5,-0.5],[0.5,-0.5], 'g', linewidth=1)

        self.canvas.draw()

    def closeEvent(self, event):
        self.molecule.number_of_NNs = int(self.ui.lineEdit_2.text())
        self.args = self.molecule.formula, self.molecule.cell, self.molecule.basis, self.molecule.cutoff, self.molecule.number_of_NNs
        self.external_params_lineText.setText(self.params_interatomic)
        self.ui.lineEdit_3.setText('')
        event.accept()

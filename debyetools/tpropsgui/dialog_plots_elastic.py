from PySide6.QtWidgets import QDialog

from debyetools.tpropsgui.ui_dialog_plots_elastic import Ui_Dialog as Ui_plots

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
import numpy as np


def print_to_box(ptedit, txt=''):
    txt = ptedit.toPlainText()+txt
    ptedit.setPlainText(txt)
    ptedit.verticalScrollBar().setValue(ptedit.verticalScrollBar().maximum())

class dialogPlots(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_plots()
        self.ui.setupUi(self)

        self.fig1 = Figure(figsize=(9, 3))
        self.fig2 = Figure(figsize=(9, 3))
        self.fig3 = Figure(figsize=(9, 3))
        self.fig4 = Figure(figsize=(9, 3))

        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas3 = FigureCanvas(self.fig3)
        self.canvas4 = FigureCanvas(self.fig4)

        self.canvas_configuration()

        llayout1 = self.ui.hLplots1
        llayout1.addWidget(self.canvas1, 88)

        llayout2 = self.ui.hLplots2
        llayout2.addWidget(self.canvas2, 100)

        llayout3 = self.ui.hLplots3
        llayout3.addWidget(self.canvas3, 80)

        llayout4 = self.ui.hLplots4
        llayout4.addWidget(self.canvas4, 100)

    def canvas_configuration(self):
        self.fig1.set_canvas(self.canvas1)
        self.fig2.set_canvas(self.canvas2)
        self.fig3.set_canvas(self.canvas3)
        self.fig4.set_canvas(self.canvas4)

        self.ax1 = []
        self.ax2 = []
        self.ax3 = []
        self.ax4 = []
        for i in range(3):
            self.ax1.append(self.canvas1.figure.add_subplot(1, 3, i+1, polar=True))
            self.ax2.append(self.canvas2.figure.add_subplot(1, 3, i+1, polar=True))
            self.ax3.append(self.canvas3.figure.add_subplot(1, 3, i+1, polar=True))
            self.ax4.append(self.canvas4.figure.add_subplot(1, 3, i+1, polar=True))

            # axi.set_axis_off()

        # self.fig.subplots_adjust(hspace=0.05, right=0.99, top=.99, bottom=.01, left=0.01, wspace=0.05)


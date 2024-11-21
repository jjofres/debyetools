from PySide6.QtWidgets import QDialog
from debyetools.tpropsgui.ui_dialog_elastic import Ui_Dialog as Ui_elastic
from debyetools.tpropsgui.dialog_plots_elastic import dialogPlots
import debyetools.tpropsgui.elastic_props as elastic
import numpy as np
class dialogElastic(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_elastic()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.on_pushPlots)

        self.dialog_plots = dialogPlots(self)





    def on_pushPlots(self):
        # print('ssss')
        self.dialog_plots.ax1, self.dialog_plots.ax2, self.dialog_plots.ax3, self.dialog_plots.ax4 = elastic.run_script_plots([self.dialog_plots.ax1, self.dialog_plots.ax2, self.dialog_plots.ax3, self.dialog_plots.ax4], self.EM)

        # self.dialog_plots.ax1[0].plot([0,1],[0,1])

        self.dialog_plots.fig1.subplots_adjust(wspace=0.8)
        self.dialog_plots.fig2.subplots_adjust(wspace=0.8)
        self.dialog_plots.fig3.subplots_adjust(wspace=0.8)
        self.dialog_plots.fig4.subplots_adjust(wspace=0.8)

        planestr = ['xy', 'xz', 'yz']
        for i, axi in enumerate(self.dialog_plots.ax1):
            axi.text(5/4*np.pi, axi.get_rmax()*2.1, f'{planestr[i]} plane', fontsize=8, ha='center')
        for i, axi in enumerate(self.dialog_plots.ax2):
            axi.text(5/4*np.pi, axi.get_rmax()*2, f'{planestr[i]} plane', fontsize=8, ha='center')
        for i, axi in enumerate(self.dialog_plots.ax3):
            axi.text(5/4*np.pi, axi.get_rmax()*2, f'{planestr[i]} plane', fontsize=8, ha='center')
        for i, axi in enumerate(self.dialog_plots.ax4):
            axi.text(5/4*np.pi, axi.get_rmax()*2, f'{planestr[i]} plane', fontsize=8, ha='center')

        self.dialog_plots.show()

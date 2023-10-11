from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMenu
from PySide6.QtCore import Qt

from debyetools.tpropsgui.ui_heatcapacitywindow import Ui_MainWindow as Ui_Cp

from debyetools.fs_compound_db import fit_FS as dt_fit_FS
#from debyetools.fs_compound_db import Cp2fit as dt_Cp2fit

# from  debyetools.tpropsgui.backend_qt_patched.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.backends.backend_mixed import FigureCanvas
# print(hola)

# from matplotlib.backends.backend_qtagg import FigureCanvas
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.widgets import Cursor
from matplotlib.figure import Figure

import numpy as np

class windowCp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Cp()
        self.ui.setupUi(self)
        # self.app = app

        self.fig = Figure(figsize=(3, 3))
        self.canvas = FigureCanvas(self.fig)
        self.set_canvas_configuration()

        llayout = self.ui.horizontalLayout#QHBoxLayout()
        llayout.addWidget(self.canvas, 88)
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.customContextMenuRequested.connect(self.right_menu)

        self.ui.pushButton.clicked.connect(self.on_click_recalc)
        self.ui.lineEdit.textChanged.connect(self.update_FS_Tto)
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)

        self.ui.comboBox_2.currentIndexChanged.connect(self.selectionchange_plot)
        self.current_plot = 9

        self.ui.progress.setGeometry(700, 505, 81, 5)



    def selectionchange_plot(self, i):
        self.current_plot = i
        self.plot_prop('T', self.proplist[i])



    def selectionchange(self, i):
        Pi = self.Ps[i]
        self.ui.tableWidget.setItem(0,0,QTableWidgetItem('%.5e' % (self.dict_H298['%.1f'%(Pi/1e9)])))
        self.ui.tableWidget.setItem(1,0,QTableWidgetItem('%.5e' % (self.dict_S298['%.1f'%(Pi/1e9)])))
        for ix, p in enumerate(self.dict_FS['%.1f'%(Pi/1e9)]['Cp']):
            self.ui.tableWidget.setItem(ix+2,0,QTableWidgetItem('%.5e' % (p)))



    def get_T(self):
        T_initial, T_final, Tstep = (float(sti) for sti in self.ui.lineEdit.text().split())
        T = np.arange(T_initial, T_final+Tstep, Tstep)
        T = np.r_[T, [298.15]]
        T.sort()

        return T

    def get_P(self):
        Ps = self.ui.lineEdit_2.text().split()
        if len(Ps)==1:
            return np.array([float(sti) for sti in Ps])
        T_initial, T_final, Tstep = (float(sti) for sti in self.ui.lineEdit_2.text().split())
        T = np.arange(T_initial, T_final+Tstep, Tstep)
        T.sort()

        return T

    def get_FS_T(self):
        return float(self.ui.lineEdit_3.text()), float(self.ui.lineEdit_4.text())

    def set_canvas_configuration(self):
        self.canvas.figure.set_constrained_layout(True)
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(111)
        self.cursor = Cursor(self._ax, useblit=True, linewidth=0.8, color='lightgray')


    def plot_prop(self, str_x, str_y):
        import matplotlib.cm as cm
        self._ax.cla()

        self.data_dict={pi_str:{} for pi_str in self.dict_tp.keys()}

        len_Ps = len(self.dict_tp.keys())
        for i, Pi_str in enumerate(self.dict_tp.keys()):
            tprops_dict = self.dict_tp[Pi_str]

            X = tprops_dict[str_x]
            Y = tprops_dict[str_y]

            self.data_dict[Pi_str] = {str_x: X, str_y:Y}

            c = cm.PuRd((i+1)/len_Ps,1)
            self._ax.plot(X, Y, label='debyetools', color=c)
            self._ax.text(X[-1]-100,Y[-1],'P='+Pi_str+'GPa', size=5)

        self._ax.set_xlabel(str_x)
        self._ax.set_ylabel(str_y)

        self.canvas.draw()


    def debye_run(self, molecule, ui_progress):
        if self.ui.radioButton.isChecked():
            mode ='jjsl'
        elif self.ui.radioButton_2.isChecked():
            mode = 'jjdm'
        elif self.ui.radioButton_3.isChecked():
            mode = 'jjfv'
        self.ui.comboBox.clear()
        self.molecule = molecule
        molecule.initialize_ndeb(mode)
        self.ndeb_obj = molecule.ndeb

        T = self.get_T()
        Ps = self.get_P()*1e9
        self.Ps = Ps


        self.dict_tp = {'%.1f'%(Pi/1e9):'' for Pi in Ps}
        self.dict_FS = {'%.1f'%(Pi/1e9):{'Cp':[0]} for Pi in Ps}
        self.dict_H298 = {'%.1f'%(Pi/1e9):0 for Pi in Ps}
        self.dict_S298 = {'%.1f'%(Pi/1e9):-1 for Pi in Ps}



        lP = len(Ps)
        progress = (0)/lP
        ui_progress.setValue(progress*100)
        for ix, P in enumerate(Ps):

            self.ui.comboBox.addItem('%.1f'%(P/1e9))

            molecule.min_G(T, P)

            molecule.eval_props()

            progress =(ix+1)/lP
            ui_progress.setValue(progress*100)

            self.dict_tp['%.1f'%(P/1e9)] =  molecule.tprops_dict

            self.FS_Tfrom, self.FS_Tto = self.get_FS_T()

            self.dict_FS['%.1f'%(P/1e9)] = dt_fit_FS(molecule.tprops_dict, self.FS_Tfrom, self.FS_Tto)

            ix_T0 = np.where(np.round(molecule.tprops_dict['T'],2) == np.round(298.15,2))[0][0]

            self.dict_H298['%.1f'%(P/1e9)] = molecule.tprops_dict['G'][ix_T0]+molecule.tprops_dict['T'][ix_T0]*molecule.tprops_dict['S'][ix_T0]
            self.dict_S298['%.1f'%(P/1e9)] = molecule.tprops_dict['S'][ix_T0]

#            self.plot_Cp(self.dict_tp['%.1f'%(P/1e9)], self.dict_FS['%.1f'%(P/1e9)])

        self.ui.tableWidget.setItem(0,0,QTableWidgetItem('%.5e' % (self.dict_H298['%.1f'%(0/1e9)])))
        self.ui.tableWidget.setItem(1,0,QTableWidgetItem('%.5e' % (self.dict_S298['%.1f'%(0/1e9)])))
        for ix, p in enumerate(self.dict_FS['%.1f'%(0/1e9)]['Cp']):
            self.ui.tableWidget.setItem(ix+2,0,QTableWidgetItem('%.5e' % (p)))

#            self._ax.text(Y[-1],X[-1],'P=')


#        print('xxxx', list(self.dict_tp[list(self.dict_tp.keys())[0]].keys()))
        self.proplist = list(self.dict_tp[list(self.dict_tp.keys())[0]].keys())
        current_plot = self.current_plot
        self.ui.comboBox_2.clear()

        for k in self.proplist:
            self.ui.comboBox_2.addItem(k)
        self.current_plot = current_plot

        self.ui.comboBox_2.setCurrentIndex(self.current_plot)

        self.plot_prop('T', self.proplist[self.current_plot])


#        handles_1, labels_1 = self._ax.get_legend_handles_labels()
#        by_label_1 = dict(zip(labels_1, handles_1))
#        self._ax.legend(by_label_1.values(), by_label_1.keys())

    def right_menu(self, pos):
         menu = QMenu()

         # Add menu options
         hello_option = menu.addAction('Copy data')

         # Menu option events
         hello_option.triggered.connect(self.on_click_copydata)

         # Position
         menu.exec(self.mapToGlobal(pos))

    def on_click_copydata(self):
#        app = QApplication(sys.argv)

        txt2copy = ''
        for k in self.data_dict:
            txt2copy = txt2copy + '#P = '+ k +' GPa\n'
            txt2copy = txt2copy + '#'
            for ki in self.data_dict[k].keys():
                txt2copy = txt2copy + ki + '    '
            txt2copy = txt2copy + '\n'
            data=[]
            for ki in self.data_dict[k].keys():
                data.append(self.data_dict[k][ki])

            data=np.array(data).T
            for d in data:
                for di in d:
                    txt2copy = txt2copy + str(di) + '    '
                txt2copy = txt2copy + '\n'
        clipboard=self.app.clipboard()
        clipboard.setText(txt2copy)



    def on_click_recalc(self):
        self._ax.cla()
        self.debye_run(self.molecule, self.ui.progress)

    def update_FS_Tto(self):
        try:
            Tf =self.get_T()[-1]
            self.ui.lineEdit_4.setText(str(Tf))
        except:
            pass

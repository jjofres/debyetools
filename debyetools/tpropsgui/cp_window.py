import numpy as np
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMenu, QMessageBox, QApplication
from debyetools.fs_compound_db import fit_FS as dt_fit_FS
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor

from debyetools.tpropsgui.atomtools import atom_energy
from debyetools.tpropsgui.ui_cp_window import Ui_MainWindow as Ui_Cp
from PySide6.QtGui import QPixmap, QPalette


# from debyetools.fs_compound_db import Cp2fit as dt_Cp2fit


def highlight_line_edit(line_edit, color="purple", duration=100):
    # Set the background color
    line_edit.setStyleSheet(f"background-color: {color};")

    # Create a QTimer to reset the color after `duration` milliseconds
    timer = QTimer(line_edit)
    timer.setSingleShot(True)  # Only trigger once
    timer.timeout.connect(lambda: line_edit.setStyleSheet(""))  # Reset the color
    timer.start(duration)


# Function to normalize data to range [0, 1]
def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


class dialogCpWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Cp()
        self.ui.setupUi(self)
        #        self.app = app

        self.fig = Figure(figsize=(3, 3))
        self.canvas = FigureCanvas(self.fig)
        self.set_canvas_configuration()

        llayout = self.ui.horizontalLayout  # QHBoxLayout()
        llayout.addWidget(self.canvas, 88)
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.customContextMenuRequested.connect(self.right_menu)

        self.ui.pushButton.clicked.connect(self.on_click_recalc)
        self.ui.lineEdit.textChanged.connect(self.update_FS_Tto)
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)

        self.ui.comboBox_2.currentIndexChanged.connect(self.selectionchange_plot)
        self.current_plot = 9

        self.ui.progress.setGeometry(700, 505, 81, 5)

        self.ui.pushBack.clicked.connect(self.on_pushBack)

        self.ui.pushExport.clicked.connect(self.on_pushExport)
        self.ui.pushCloseAll.clicked.connect(self.on_pushCloseAll)

        # Connect the textChanged signals to a shared color change method
        self.ui.lineEdit.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit))
        self.ui.lineEdit_2.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_2))
        self.ui.lineEdit_3.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_3))
        self.ui.lineEdit_4.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_4))
        self.ui.tableWidget.cellChanged.connect(lambda: self.on_text_changed(self.ui.tableWidget))


    def on_pushCloseAll(self):

        # Create a message box
       msg_box = QMessageBox()
       msg_box.setWindowTitle("Confirm Action")
       msg_box.setText("Do you want to proceed?")

       # Add Yes and No buttons
       msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

       # Execute the message box and capture the response
       response = msg_box.exec_()

       # Check which button was clicked
       if response == QMessageBox.Yes:
           QApplication.instance().closeAllWindows()
           # Trigger Yes action
       elif response == QMessageBox.No:
           pass
           # Trigger No action

    def on_pushExport(self):
        txt4output = f'{self.formula}$'

        txt4output += f'{self.Ef:.7e}'

        txt4output += f'${self.S298:7e}$'

        lst4output = []
        rcount = self.ui.tableWidget.rowCount()
        for ix in range(2, rcount):
            p = self.ui.tableWidget.item(ix, 0).text()
            lst4output.append(f'{p}')
        txt4output += '&'.join(lst4output)
        txt4output += '$'
        t4out = [f'{p:.2e}' for p in [self.FS_Tfrom, self.FS_Tto]]
        txt4output += '&'.join(t4out)

        with open('export_dtoutput4cmpnd', 'w') as f:
            f.write(txt4output)

        QMessageBox.information(self, 'Parameters Saved', "Data was saved as \n'export_dtoutput4cmpnd' file.", QMessageBox.Ok)




    def selectionchange_plot(self, i):
        self.current_plot = i
        self.plot_prop('T', self.proplist[i])

    def selectionchange(self, i):
        Pi = self.Ps[i]
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem('%.5e' % (self.dict_H298['%.1f' % (Pi / 1e9)])))
        self.ui.tableWidget.setItem(1, 0, QTableWidgetItem('%.5e' % (self.dict_S298['%.1f' % (Pi / 1e9)])))
        for ix, p in enumerate(self.dict_FS['%.1f' % (Pi / 1e9)]['Cp']):
            self.ui.tableWidget.setItem(ix + 2, 0, QTableWidgetItem('%.5e' % (p)))

    def get_T(self):
        T_initial, T_final, Tstep = (float(sti) for sti in self.ui.lineEdit.text().split())
        T = np.arange(T_initial, T_final + Tstep, Tstep)
        T = np.r_[T, [298.15]]
        T.sort()

        return T

    def get_P(self):
        Ps = self.ui.lineEdit_2.text().split()
        if len(Ps) == 1:
            return np.array([float(sti) for sti in Ps])
        T_initial, T_final, Tstep = (float(sti) for sti in self.ui.lineEdit_2.text().split())
        T = np.arange(T_initial, T_final + Tstep, Tstep)
        T.sort()

        return T

    def get_FS_T(self):
        return float(self.ui.lineEdit_3.text()), float(self.ui.lineEdit_4.text())

    def set_canvas_configuration(self):

        self.canvas.figure.set_constrained_layout(True)
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(111)
        self.cursor = Cursor(self._ax, useblit=True, linewidth=0.8, color='lightgray')

        # Create a scatter plot for the hover marker (initially invisible)
        hover_marker, = self._ax.plot([], [], 'o', color='red', markersize=10, visible=False)

        # Function to check if the cursor is near a datapoint with normalized data
        def is_cursor_near_datapoint(event, line, threshold=0.02):
            """Check if the cursor is near any datapoint for a given line"""
            x_data = normalize(line.get_xdata())  # Retrieve and normalize x data
            y_data = normalize(line.get_ydata())  # Retrieve and normalize y data

            # Normalize the event data as well
            x_cursor = (event.xdata - np.min(line.get_xdata())) / (np.max(line.get_xdata()) - np.min(line.get_xdata()))
            y_cursor = (event.ydata - np.min(line.get_ydata())) / (np.max(line.get_ydata()) - np.min(line.get_ydata()))

            for (xi, yi) in zip(x_data, y_data):
                if (event.xdata is not None) and (event.ydata is not None):
                    distance = np.sqrt((x_cursor - xi) ** 2 + (y_cursor - yi) ** 2)
                    if distance < threshold:
                        # Rescale xi, yi back to original scale for display
                        original_x = xi * (np.max(line.get_xdata()) - np.min(line.get_xdata())) + np.min(
                            line.get_xdata())
                        original_y = yi * (np.max(line.get_ydata()) - np.min(line.get_ydata())) + np.min(
                            line.get_ydata())
                        return original_x, original_y, line.get_label()
            return None, None, None

        # Function to handle mouse movement
        def on_move(event):
            if event.inaxes == self._ax:  # Check if the mouse is within the axes
                # Loop through all lines and check if the cursor is near any datapoint
                for line in self.lines:
                    near_x, near_y, line_label = is_cursor_near_datapoint(event, line)
                    if near_x is not None and near_y is not None:
                        # Update plot title with the coordinates of the datapoint, line label, and x-axis label
                        line_label = line.get_label()
                        str_2_cursor = f'{self._ax.get_xlabel()}: {event.xdata:.2f}, {self._ax.get_ylabel()}: {event.ydata:.2f}\n'
                        str_2_cursor += f'Compound: {self.molecule.formula}\n'
                        str_2_cursor += f'EOS: {self.molecule.eos_str}\nApprox.: {self.modestr}\n'
                        str_2_cursor += f'P:{line_label}\n'
                        self._ax.set_title(str_2_cursor, y=0.95, x=0.01, fontsize=6, loc='left', color='black',
                                           alpha=0.9, va='top')

                        # Update hover marker position and make it visible
                        hover_marker.set_data(near_x, near_y)
                        hover_marker.set_visible(True)
                        self.fig.canvas.draw_idle()  # Redraw the figure to update the title and point colors

                        return

                # If no point is near the cursor, reset the title
                line_label = line.get_label()
                str_2_cursor = f'{self._ax.get_xlabel()}: {event.xdata:.2f}, {self._ax.get_ylabel()}: {event.ydata:.2f}\n'
                # str_2_cursor += f'Compound: {self.molecule.formula}\n'
                # str_2_cursor += f'\nEOS: {self.molecule.eos_str}\nApprox.: {self.modestr}'
                self._ax.set_title(str_2_cursor, y=0.95, x=0.01, fontsize=6, loc='left', color='black', alpha=0.6,
                                   va='top')
                # Reset the color of the markers to the default color when not hovering

                # Hide hover marker when not hovering over any point
                hover_marker.set_visible(False)

                self.fig.canvas.draw_idle()  # Redraw the figure to update the title and point colors

        # Connect the event handler
        self.fig.canvas.mpl_connect('motion_notify_event', on_move)

    def plot_prop(self, str_x, str_y):
        import matplotlib.cm as cm
        self._ax.cla()

        self.data_dict = {pi_str: {} for pi_str in self.dict_tp.keys()}

        len_Ps = len(self.dict_tp.keys())

        self.lines = []
        for i, Pi_str in enumerate(self.dict_tp.keys()):
            tprops_dict = self.dict_tp[Pi_str]

            X = tprops_dict[str_x]
            Y = tprops_dict[str_y]

            self.data_dict[Pi_str] = {str_x: X, str_y: Y}

            c = cm.PuRd((i + 1) / len_Ps, 1)
            line, = self._ax.plot(X, Y, label=Pi_str + 'GPa', color=c)
            self.lines.append(line)
            self._ax.text(X[-1] - 100, Y[-1], 'P=' + Pi_str + 'GPa', size=8)

        self._ax.set_xlabel(str_x)
        self._ax.set_ylabel(str_y)

        self.canvas.draw()

    def debye_run(self, molecule, ui_progress, formula):
        self.formula = formula
        txt4output = f'{formula}$'
        if self.ui.radioButton.isChecked():
            mode = 'jjsl'
            self.modestr = 'Slater'
        elif self.ui.radioButton_2.isChecked():
            mode = 'jjdm'
            self.modestr = 'Dugdale-MacDonald'
        elif self.ui.radioButton_3.isChecked():
            mode = 'jjfv'
            self.modestr = 'FVT'

        self.ui.comboBox.clear()
        self.molecule = molecule
        molecule.initialize_ndeb(mode)
        self.ndeb_obj = molecule.ndeb

        T = self.get_T()
        Ps = self.get_P() * 1e9
        self.Ps = Ps

        self.dict_tp = {'%.1f' % (Pi / 1e9): '' for Pi in Ps}
        self.dict_FS = {'%.1f' % (Pi / 1e9): {'Cp': [0]} for Pi in Ps}
        self.dict_H298 = {'%.1f' % (Pi / 1e9): 0 for Pi in Ps}
        self.dict_S298 = {'%.1f' % (Pi / 1e9): -1 for Pi in Ps}

        lP = len(Ps)
        progress = (0) / lP
        ui_progress.setValue(progress * 100)
        for ix, P in enumerate(Ps):

            self.ui.comboBox.addItem('%.1f' % (P / 1e9))

            molecule.min_G(T, P)

            molecule.eval_props()

            progress = (ix + 1) / lP
            ui_progress.setValue(progress * 100)

            self.dict_tp['%.1f' % (P / 1e9)] = molecule.tprops_dict

            self.FS_Tfrom, self.FS_Tto = self.get_FS_T()

            self.dict_FS['%.1f' % (P / 1e9)] = dt_fit_FS(molecule.tprops_dict, self.FS_Tfrom, self.FS_Tto)

            ix_T0 = np.where(np.round(molecule.tprops_dict['T'], 2) == np.round(298.15, 2))[0][0]

            self.dict_H298['%.1f' % (P / 1e9)] = molecule.tprops_dict['G'][ix_T0] + molecule.tprops_dict['T'][ix_T0] * \
                                                 molecule.tprops_dict['S'][ix_T0]
            self.dict_S298['%.1f' % (P / 1e9)] = molecule.tprops_dict['S'][ix_T0]

            #            self.plot_Cp(self.dict_tp['%.1f'%(P/1e9)], self.dict_FS['%.1f'%(P/1e9)])
            nats = len(molecule.types)
            if P == 0:
                # print(molecule.__dict__.keys())
                Ef = molecule.eos.E0(molecule.eos.V0) - sum([atom_energy[ti] for ti in molecule.types]) * (
                            0.160218e-18 * 6.02214e23) / len(molecule.types)
                self.Ef = Ef*nats
                txt4output += f'{Ef * nats:.7e}'
        self.S298 = self.dict_S298['%.1f' % (0 / 1e9)] * nats
        txt4output += f'${self.dict_S298['%.1f' % (0 / 1e9)] * nats:.7e}$'

        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem('%.5e' % (self.dict_H298['%.1f' % (0 / 1e9)])))
        self.ui.tableWidget.setItem(1, 0, QTableWidgetItem('%.5e' % (self.dict_S298['%.1f' % (0 / 1e9)])))

        lst4output = []
        for ix, p in enumerate(self.dict_FS['%.1f' % (0 / 1e9)]['Cp']):
            lst4output.append(f'{p * nats:.7e}')
            self.ui.tableWidget.setItem(ix + 2, 0, QTableWidgetItem('%.5e' % (p)))
        txt4output += '&'.join(lst4output)
        txt4output += '$'
        t4out = [f'{p:.2e}' for p in [self.FS_Tfrom, self.FS_Tto]]
        txt4output += '&'.join(t4out)

        with open('dtoutput4cmpnd', 'w') as f:
            f.write(txt4output)
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

    def on_pushBack(self):
        self.close()

    def on_click_copydata(self):
        #        app = QApplication(sys.argv)

        txt2copy = ''
        for k in self.data_dict:
            txt2copy = txt2copy + '#P = ' + k + ' GPa\n'
            txt2copy = txt2copy + '#'
            for ki in self.data_dict[k].keys():
                txt2copy = txt2copy + ki + '    '
            txt2copy = txt2copy + '\n'
            data = []
            for ki in self.data_dict[k].keys():
                data.append(self.data_dict[k][ki])

            data = np.array(data).T
            for d in data:
                for di in d:
                    txt2copy = txt2copy + str(di) + '    '
                txt2copy = txt2copy + '\n'
        clipboard = self.app.clipboard()
        clipboard.setText(txt2copy)

    def on_click_recalc(self):
        self._ax.cla()
        self.debye_run(self.molecule, self.ui.progress, self.formula)

    def update_FS_Tto(self):
        try:
            Tf = self.get_T()[-1]
            self.ui.lineEdit_4.setText(str(Tf))
        except:
            pass

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

import numpy as np
import warnings
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMenu, QMessageBox, QApplication, QPushButton
from debyetools.fs_compound_db import fit_FS as dt_fit_FS
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor

from debyetools.tpropsgui.atomtools import REFERENCES
from debyetools.tpropsgui.dialog_refEnergies import dialogRefEnergies
from debyetools.tpropsgui.ui_cp_window import Ui_MainWindow as Ui_Cp
from PySide6.QtGui import QPixmap, QPalette
from debyetools.constants import EV_ATOM_TO_J_MOL


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
        # elemental reference energies of the formation energy, editable for the session (G2)
        self.pushRefs = QPushButton('Reference energies...', self.ui.centralwidget)
        self.ui.verticalLayout_5.insertWidget(1, self.pushRefs)
        self.pushRefs.clicked.connect(self.on_pushRefs)
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
        # same content as dtoutput4cmpnd: Ef, S298 and Cp coefficients all per formula unit, at the reference
        # pressure (was: Cp coefficients per mol-atom from the table next to Ef, S298 per formula unit, G7)
        txt4output = getattr(self, 'txt4output', None)
        if txt4output is None:
            QMessageBox.information(self, 'Warning', 'Nothing to export yet.', QMessageBox.Ok)
            return
        with open('export_dtoutput4cmpnd', 'w') as f:
            f.write(txt4output)

        QMessageBox.information(self, 'Parameters Saved', "Data was saved as \n'export_dtoutput4cmpnd' file.", QMessageBox.Ok)




    def selectionchange_plot(self, i):
        self.current_plot = i
        self.plot_prop('T', self.proplist[i])

    def selectionchange(self, i):
        if i < 0 or i >= len(self.Ps):
            return
        Pi = self.Ps[i]
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem('%.5e' % (self.dict_H298['%.1f' % (Pi / 1e9)])))
        self.ui.tableWidget.setItem(1, 0, QTableWidgetItem('%.5e' % (self.dict_S298['%.1f' % (Pi / 1e9)])))
        for ix, p in enumerate(self.dict_FS['%.1f' % (Pi / 1e9)]['Cp']):
            self.ui.tableWidget.setItem(ix + 2, 0, QTableWidgetItem('%.5e' % (p)))

    @staticmethod
    def _grid(txt):
        """'x0 x1 step' -> x0, x0 + step, ... up to x1 (never beyond, G12); a single number -> that number."""
        vals = [float(sti) for sti in txt.split()]
        if len(vals) == 1:
            return np.array(vals)
        x0, x1, step = vals
        if step <= 0 or x1 < x0:
            raise ValueError('expected "start end step" with step > 0 and end >= start, got %r' % txt)
        n = int(np.floor((x1 - x0) / step + 1e-9)) + 1
        return x0 + step * np.arange(n)

    def get_T(self):
        T = self._grid(self.ui.lineEdit.text())
        T = np.unique(np.where(T <= 0, 0.1, T))  # min_G needs T > 0: a start at 0 K is computed at 0.1 K
        if not np.any(np.abs(T - 298.15) < 1e-6):  # 298.15 K is needed for H298 and S298
            T = np.sort(np.r_[T, [298.15]])
        return T

    def get_P(self):
        return self._grid(self.ui.lineEdit_2.text())

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

    def compute_Ef(self):
        """Static formation energy per formula unit, Ef = nats * (E0(V0) - mean_i E_i^ref), with E_i^ref the
        reference energy of the exact POTCAR used for element i (G2). Returns the notes for the user."""
        molecule = self.molecule
        elements = list(dict.fromkeys(molecule.types))
        notes = []
        missing = [el for el in elements if REFERENCES.energy(REFERENCES.potential(el)) is None]
        assumed = [el for el in elements if REFERENCES.assumed(el)]
        if assumed:
            notes.append('POTCAR not read from an OUTCAR for %s; assumed %s. Check it with "Reference energies...".'
                         % (', '.join(assumed), ', '.join("'%s'" % REFERENCES.potential(el) for el in assumed)))
        if missing:
            self.Ef = np.nan
            notes.append('No reference energy for %s: the formation energy is not computed. Enter the value with '
                         '"Reference energies...".'
                         % ', '.join('%s (%s)' % (el, REFERENCES.potential(el)) for el in missing))
        else:
            E_ref = np.mean([REFERENCES.energy(REFERENCES.potential(ti)) for ti in molecule.types]) * EV_ATOM_TO_J_MOL
            self.Ef = (molecule.eos.E0(molecule.eos.V0) - E_ref) * len(molecule.types)
        return notes

    def store_element_H298(self):
        """A pure-element run at P = 0 stores its H(298.15 K) as the H298 reference of its POTCAR (G14)."""
        elements = list(dict.fromkeys(self.molecule.types))
        H = self.dict_H298['%.1f' % (self.P_ref / 1e9)]
        if len(elements) != 1 or not np.isfinite(H):
            return []
        if self.P_ref != 0:
            return ['H298 of %s not stored as a reference: the run does not include P = 0.' % elements[0]]
        pot = REFERENCES.potential(elements[0])
        source = 'run %s (%s, %s)' % (self.formula, type(self.molecule.eos).__name__, self.modestr)
        REFERENCES.h298_runs[pot] = (float(H), source, self.modestr)
        return []

    def compute_H298(self):
        """H298 for the FactSage Compound module (G14): formation enthalpy per formula unit,
        DH298 = nats * (H_cmp(298.15) - mean_i H_i(298.15)), with H = G + TS of the compound run (J/mol-atom, at the
        reference pressure) and H_i the H298 reference of the POTCAR of element i (pure-element run of this session
        or entered). Without all H_i: the static Ef (no zero-point or thermal part), with a note.
        Sets self.Ef and self.H298, self.H298_kind ('DH298' or 'static Ef'); returns the notes for the user."""
        notes = self.compute_Ef()
        molecule = self.molecule
        elements = list(dict.fromkeys(molecule.types))
        H_cmp = self.dict_H298['%.1f' % (self.P_ref / 1e9)]
        missing = [el for el in elements if REFERENCES.h298(REFERENCES.potential(el)) is None]
        if np.isfinite(H_cmp) and not missing:
            H_ref = np.mean([REFERENCES.h298(REFERENCES.potential(ti)) for ti in molecule.types])
            self.H298 = (H_cmp - H_ref) * len(molecule.types)
            self.H298_kind = 'DH298'
            # the static Ef is not needed for DH298: no note about a missing static reference energy
            notes = [n for n in notes if not n.startswith('No reference energy')]
            if self.P_ref != 0:
                notes.append('H298: compound enthalpy taken at %.1f GPa (P = 0 not computed).' % (self.P_ref / 1e9))
            other_mode = [el for el in elements if REFERENCES.potential(el) in REFERENCES.h298_runs
                          and REFERENCES.potential(el) not in REFERENCES.h298_edited
                          and REFERENCES.h298_runs[REFERENCES.potential(el)][2] != self.modestr]
            if other_mode:
                notes.append('H298 reference of %s computed with another Debye model than this run (%s).'
                             % (', '.join(other_mode), self.modestr))
        else:
            self.H298 = self.Ef
            self.H298_kind = 'static Ef'
            if not np.isfinite(H_cmp):
                notes.append('298.15 K not reached: the exported H298 is the static Ef.')
            if missing:
                notes.append('No H298 reference for %s: the exported H298 is the static Ef (no zero-point or thermal '
                             'part). Run the pure element(s) in this session (same POTCAR and settings, P = 0) or '
                             'enter the value with "Reference energies...".'
                             % ', '.join('%s (%s)' % (el, REFERENCES.potential(el)) for el in missing))
        return notes

    def show_export_rows(self):
        """Two rows below the per-pressure values: the exported H298 and S298, per formula unit (G14)."""
        table = self.ui.tableWidget
        if table.rowCount() < 10:
            table.setRowCount(10)
        rows = [('H298 export (%s)' % self.H298_kind, self.H298, 'J/mol-formula'),
                ('S298 export', self.S298, 'J/K/mol-formula')]
        for i, (label, value, unit) in enumerate(rows):
            table.setVerticalHeaderItem(8 + i, QTableWidgetItem(label))
            for j, txt in enumerate(['%.5e' % value, unit]):
                item = QTableWidgetItem(txt)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(8 + i, j, item)

    def build_export(self):
        """One export text, every value per formula unit (H298, S298 and the Cp coefficients) at the reference
        pressure; written to dtoutput4cmpnd now and to export_dtoutput4cmpnd by the Export button (G7, G14)."""
        key = '%.1f' % (self.P_ref / 1e9)
        nats = self.nats
        txt4output = f'{self.formula}$' + f'{self.H298:.7e}' + f'${self.S298:.7e}$'
        txt4output += '&'.join([f'{p * nats:.7e}' for p in self.dict_FS[key]['Cp']])
        txt4output += '$' + '&'.join([f'{p:.2e}' for p in [self.FS_Tfrom, self.FS_Tto]])
        self.txt4output = txt4output
        with open('dtoutput4cmpnd', 'w') as f:
            f.write(txt4output)

    def on_pushRefs(self):
        if getattr(self, 'txt4output', None) is None:
            QMessageBox.information(self, 'Warning', 'Run a calculation first.', QMessageBox.Ok)
            return
        self.dialog_refs = dialogRefEnergies(self.molecule.types, self, on_apply=self.on_refs_applied)
        self.dialog_refs.show()

    def on_refs_applied(self):
        notes = self.compute_H298()
        self.build_export()
        self.show_export_rows()
        msg = ['Exported H298 = %.6e J/mol per formula unit (%s).' % (self.H298, self.H298_kind),
               'Static Ef = %.6e J/mol per formula unit.' % self.Ef]
        QMessageBox.information(self, 'Formation enthalpy', '\n'.join(notes + msg), QMessageBox.Ok)

    def debye_run(self, molecule, ui_progress, formula):
        self.formula = formula
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
        self.FS_Tfrom, self.FS_Tto = self.get_FS_T()

        key = lambda Pi: '%.1f' % (Pi / 1e9)
        self.dict_tp = {key(Pi): '' for Pi in Ps}
        self.dict_FS = {key(Pi): {'Cp': [np.nan] * 6} for Pi in Ps}
        self.dict_H298 = {key(Pi): np.nan for Pi in Ps}
        self.dict_S298 = {key(Pi): np.nan for Pi in Ps}
        notes = []

        lP = len(Ps)
        ui_progress.setValue(0)
        for ix, P in enumerate(Ps):
            self.ui.comboBox.addItem(key(P))

            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                molecule.min_G(T, P)
            # min_G truncation (D10) is reported instead of only printed to the console (G6)
            notes += ['P = %s GPa: %s' % (key(P), w.message) for w in caught if 'min_G' in str(w.message)]
            if len(molecule.T) == 0:
                notes.append('P = %s GPa: no stable volume at any temperature; nothing computed.' % key(P))
                continue

            molecule.eval_props()
            ui_progress.setValue(int((ix + 1) / lP * 100))
            tp = molecule.tprops_dict
            self.dict_tp[key(P)] = tp

            # FactSage Cp fit only inside the computed temperature range
            Tmax = float(tp['T'][-1])
            if Tmax < self.FS_Tto - 1e-6:
                notes.append('P = %s GPa: FactSage Cp fit limited to %.1f K (last stable temperature).' % (key(P), Tmax))
            if np.sum((tp['T'] >= self.FS_Tfrom) & (tp['T'] <= self.FS_Tto)) >= 6:
                self.dict_FS[key(P)] = dt_fit_FS(tp, self.FS_Tfrom, min(self.FS_Tto, Tmax))
            else:
                notes.append('P = %s GPa: fewer than 6 temperatures between %.2f and %.2f K; no FactSage fit.'
                             % (key(P), self.FS_Tfrom, self.FS_Tto))

            ix_T0 = np.where(np.abs(tp['T'] - 298.15) < 1e-6)[0]
            if len(ix_T0):
                i0 = ix_T0[0]
                self.dict_H298[key(P)] = tp['G'][i0] + tp['T'][i0] * tp['S'][i0]
                self.dict_S298[key(P)] = tp['S'][i0]
            else:
                notes.append('P = %s GPa: 298.15 K was not reached; H298 and S298 not available.' % key(P))

        computed = [Pi for Pi in Ps if isinstance(self.dict_tp[key(Pi)], dict)]
        if not computed:
            QMessageBox.information(self, 'Warning', '\n'.join(notes) or 'Nothing was computed.', QMessageBox.Ok)
            return

        # reference pressure for the table and the export: P = 0 if computed, otherwise the lowest pressure (G7)
        self.P_ref = min(computed, key=abs)
        nats = len(molecule.types)
        self.nats = nats
        notes += self.store_element_H298()
        notes += self.compute_H298()
        self.S298 = self.dict_S298[key(self.P_ref)] * nats
        self.build_export()
        self.show_export_rows()

        self.ui.comboBox.setCurrentText(key(self.P_ref))
        self.selectionchange(self.ui.comboBox.currentIndex())

        self.proplist = list(self.dict_tp[key(self.P_ref)].keys())
        current_plot = self.current_plot
        self.ui.comboBox_2.clear()

        for k in self.proplist:
            self.ui.comboBox_2.addItem(k)
        self.current_plot = current_plot

        self.ui.comboBox_2.setCurrentIndex(self.current_plot)

        self.plot_prop('T', self.proplist[self.current_plot])

        if notes:
            QMessageBox.information(self, 'Warning', '\n'.join(notes), QMessageBox.Ok)

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

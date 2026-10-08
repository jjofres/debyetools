"""Editable table of the elemental references used for the formation energy (G2) and enthalpy (G14).

One row per element of the formula: POTCAR name (read from an OUTCAR / POTCAR or typed), static reference energy
in eV/atom (from atomtools.atom_energy for that exact POTCAR name, or typed), H at 298.15 K in J/mol-atom (from a
pure-element run of this session, or typed) and where they come from. Changes are kept for the current session
(atomtools.REFERENCES); 'Save table...' / 'Load table...' write and read them as a CSV file, so element runs and
entered values carry over between sessions.
"""
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QDialog, QFileDialog, QHBoxLayout, QHeaderView, QLabel, QMessageBox, QPushButton,
                               QTableWidget, QTableWidgetItem, QVBoxLayout)

from debyetools.tpropsgui.atomtools import (REFERENCES, REF_FUNCTIONAL, atom_energy, element_of,
                                            save_reference_table, load_reference_table)

COL_EL, COL_X, COL_POT, COL_E, COL_H, COL_SRC = range(6)
EDITABLE = (COL_POT, COL_E, COL_H)


class dialogRefEnergies(QDialog):
    def __init__(self, types, parent=None, on_apply=None):
        """types: element symbol of every atom of the formula unit (e.g. ['Al', 'Al', 'Al', 'Li']);
        on_apply: called after OK (e.g. to recompute Ef)."""
        super().__init__(parent)
        self.setWindowTitle('Reference energies')
        self.on_apply = on_apply
        self.elements = list(dict.fromkeys(types))
        self.counts = {el: types.count(el) for el in self.elements}
        self._filling = False

        self.table = QTableWidget(len(self.elements), 6, self)
        self.table.setHorizontalHeaderLabels(['element', 'atoms', 'POTCAR', 'E ref (eV/atom)',
                                              'H298 ref (J/mol-atom)', 'source'])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.cellChanged.connect(self.on_cell_changed)

        self.label = QLabel(self)
        self.label.setWordWrap(True)

        self.button_outcar = QPushButton('Read POTCAR names from OUTCAR...', self)
        self.button_outcar.clicked.connect(self.on_read_outcar)
        self.button_save = QPushButton('Save table...', self)
        self.button_save.clicked.connect(self.on_save)
        self.button_load = QPushButton('Load table...', self)
        self.button_load.clicked.connect(self.on_load)
        self.button_ok = QPushButton('OK', self)
        self.button_ok.clicked.connect(self.on_ok)
        self.button_cancel = QPushButton('Cancel', self)
        self.button_cancel.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addWidget(self.button_outcar)
        buttons.addWidget(self.button_save)
        buttons.addWidget(self.button_load)
        buttons.addStretch(1)
        buttons.addWidget(self.button_ok)
        buttons.addWidget(self.button_cancel)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.label)
        layout.addLayout(buttons)
        self.resize(760, 160 + 30 * len(self.elements))

        # session values are copied and only written back on OK
        self.potentials = {el: REFERENCES.potential(el) for el in self.elements}
        self.sources = {el: REFERENCES.sources.get(el, 'assumed (no OUTCAR read)') for el in self.elements}
        self.edited = dict(REFERENCES.edited)
        self.h298_edited = dict(REFERENCES.h298_edited)
        self.h298_runs = dict(REFERENCES.h298_runs)
        self.functional = REFERENCES.functional
        self.fill()

    def energy(self, potential):
        e = self.edited.get(potential, atom_energy.get(potential))
        return None if e is None else float(e)

    def h298(self, potential):
        if potential in self.h298_edited:
            return float(self.h298_edited[potential])
        if potential in self.h298_runs:
            return float(self.h298_runs[potential][0])
        return None

    def h298_source(self, potential):
        if potential in self.h298_edited:
            return 'entered'
        if potential in self.h298_runs:
            return self.h298_runs[potential][1]
        return 'none: H298 exported as static Ef'

    def fill(self):
        self._filling = True
        for i, el in enumerate(self.elements):
            pot = self.potentials[el]
            e = self.energy(pot)
            if e is None:
                e_src = 'no value for this POTCAR: enter one'
            elif pot in self.edited:
                e_src = 'entered'
            else:
                e_src = 'table'
            h = self.h298(pot)
            values = [el, str(self.counts[el]), pot, '' if e is None else '%.5f' % e,
                      '' if h is None else '%.6e' % h,
                      'POTCAR: %s; E: %s; H298: %s' % (self.sources[el], e_src, self.h298_source(pot))]
            for j, v in enumerate(values):
                item = QTableWidgetItem(v)
                if j not in EDITABLE:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if e is None and j in (COL_POT, COL_E):
                    item.setBackground(QColor('#e8a0a0'))
                if h is None and j == COL_H:
                    item.setBackground(QColor('#ecd59a'))
                self.table.setItem(i, j, item)
        self._filling = False
        self.update_label()

    def update_label(self):
        missing = [el for el in self.elements if self.energy(self.potentials[el]) is None]
        assumed = [el for el in self.elements if self.sources[el].startswith('assumed')]
        txt = []
        if missing:
            txt.append('No reference energy for %s: the formation energy is not computed until a value is entered.'
                       % ', '.join('%s (%s)' % (el, self.potentials[el]) for el in missing))
        no_h = [el for el in self.elements if self.h298(self.potentials[el]) is None]
        if no_h:
            txt.append('No H298 reference for %s: the exported H298 is the static Ef (no zero-point or thermal part). '
                       'Run the pure element in this session (same POTCAR and settings, P = 0) or enter its H298; '
                       'for a gas (O2, N2, ...) enter H298 per mol of atoms.' % ', '.join(no_h))
        if assumed:
            txt.append('POTCAR not read from an OUTCAR for %s: check that it is the one used in the calculations.'
                       % ', '.join(assumed))
        if self.functional is not None and self.functional != REF_FUNCTIONAL:
            txt.append('The OUTCAR uses %s; the tabulated values are %s.' % (self.functional, REF_FUNCTIONAL))
        txt.append('Values must come from the same VASP settings as the compound (ENCUT, k-points, functional). '
                   'Changes are kept for this session only.')
        self.label.setText('\n'.join(txt))

    def on_cell_changed(self, row, col):
        if self._filling:
            return
        el = self.elements[row]
        text = self.table.item(row, col).text().strip()
        if col == COL_POT:
            if text and element_of(text) != el:
                QMessageBox.information(self, 'Warning', "'%s' is not a POTCAR of %s." % (text, el), QMessageBox.Ok)
            elif text:
                self.potentials[el] = text
                self.sources[el] = 'entered'
        elif col == COL_E:
            pot = self.potentials[el]
            if text == '':
                self.edited.pop(pot, None)
            else:
                try:
                    self.edited[pot] = float(text)
                except ValueError:
                    QMessageBox.information(self, 'Warning', "'%s' is not a number." % text, QMessageBox.Ok)
        elif col == COL_H:
            pot = self.potentials[el]
            if text == '':
                self.h298_edited.pop(pot, None)
            else:
                try:
                    self.h298_edited[pot] = float(text)
                except ValueError:
                    QMessageBox.information(self, 'Warning', "'%s' is not a number." % text, QMessageBox.Ok)
        self.fill()

    def on_read_outcar(self):
        path, _ = QFileDialog.getOpenFileName(self, caption='Select an OUTCAR or POTCAR file')
        if path:
            self.read_outcar(path)

    def read_outcar(self, path):
        from debyetools.tpropsgui.atomtools import read_potentials
        try:
            functional, potentials = read_potentials(path)
        except Exception as e:
            QMessageBox.information(self, 'Error', 'Could not read the POTCAR names:\n%s' % e, QMessageBox.Ok)
            return
        found = {element_of(p): p for p in potentials}
        for el in self.elements:
            if el in found:
                self.potentials[el] = found[el]
                self.sources[el] = path
        self.functional = functional
        notes = []
        not_found = [el for el in self.elements if el not in found]
        extra = [p for el, p in found.items() if el not in self.elements]
        if not_found:
            notes.append('Not in this OUTCAR: %s.' % ', '.join(not_found))
        if extra:
            notes.append('In the OUTCAR but not in the formula: %s.' % ', '.join(extra))
        if notes:
            QMessageBox.information(self, 'Warning', '\n'.join(notes), QMessageBox.Ok)
        self.fill()

    def on_save(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save the reference table',
                                              REFERENCES.table_path or 'debyetools_references.csv',
                                              'CSV files (*.csv);;All files (*)')
        if path:
            self.save_table(path)

    def save_table(self, path):
        """Write every reference of the session (all POTCARs, not only this formula), including unapplied edits."""
        try:
            n = save_reference_table(path, self.edited, self.h298_runs, self.h298_edited)
        except Exception as e:
            QMessageBox.information(self, 'Error', 'Could not save the reference table:\n%s' % e, QMessageBox.Ok)
            return
        REFERENCES.table_path = path
        QMessageBox.information(self, 'Reference table', '%d POTCAR(s) saved to\n%s' % (n, path), QMessageBox.Ok)

    def on_load(self):
        start = REFERENCES.table_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reference_tables')
        path, _ = QFileDialog.getOpenFileName(self, 'Load a reference table', start,
                                              'CSV files (*.csv);;All files (*)')
        if path:
            self.load_table(path)

    def load_table(self, path):
        """Merge a saved table into the dialog (values from the file replace those of the session for the same
        POTCAR); applied to the session with OK."""
        try:
            edited, h298_runs, h298_edited = load_reference_table(path)
        except Exception as e:
            QMessageBox.information(self, 'Error', 'Could not read the reference table:\n%s' % e, QMessageBox.Ok)
            return
        replaced = sorted(p for p in set(edited) | set(h298_runs) | set(h298_edited)
                          if self.h298(p) is not None or p in self.edited)
        self.edited.update(edited)
        for pot, value in h298_runs.items():
            self.h298_runs[pot] = value
            self.h298_edited.pop(pot, None)  # the file says this H298 comes from a run
        for pot, value in h298_edited.items():
            self.h298_edited[pot] = value
        REFERENCES.table_path = path
        n = len(set(edited) | set(h298_runs) | set(h298_edited))
        msg = '%d POTCAR(s) read from\n%s' % (n, path)
        if replaced:
            msg += '\nReplaced session values for: %s' % ', '.join(replaced)
        QMessageBox.information(self, 'Reference table', msg + '\nPress OK to apply.', QMessageBox.Ok)
        self.fill()

    def on_ok(self):
        for el in self.elements:
            if not self.sources[el].startswith('assumed'):
                REFERENCES.potentials[el] = self.potentials[el]
                REFERENCES.sources[el] = self.sources[el]
        REFERENCES.edited = dict(self.edited)
        REFERENCES.h298_edited = dict(self.h298_edited)
        REFERENCES.h298_runs = dict(self.h298_runs)
        if self.functional is not None:
            REFERENCES.functional = self.functional
        self.accept()
        if self.on_apply is not None:
            self.on_apply()

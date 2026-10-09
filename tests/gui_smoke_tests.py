"""Headless smoke tests of the GUI (debyetools.tpropsgui), from the GUI review (claude/findings_gui.md, G1-G23).

The windows and dialogs are driven through their own slots with the offscreen Qt platform; message boxes are
captured instead of shown. Skipped when PySide6 (or the Qt libraries it needs) cannot be loaded. Every test runs in
a temporary working directory (the Cp window writes dtoutput4cmpnd there).
"""
import contextlib
import io
import os
import types
import warnings
from pathlib import Path

import numpy as np
import pytest

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
try:
    from PySide6.QtWidgets import QApplication, QMessageBox, QTextEdit, QPlainTextEdit, QLineEdit
except Exception as e:  # PySide6 missing, or Qt libraries (libEGL, ...) missing
    pytest.skip('PySide6 not usable: %s' % e, allow_module_level=True)

TI = Path(__file__).resolve().parent / 'inpt_files'
M_AL, M_LI = 0.0269815385, 0.00694


# ---------------------------------------------------------------------------------------------------------- fixtures
@pytest.fixture(scope='module')
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def msgs(monkeypatch, tmp_path, qapp):
    """Captured message boxes [(kind, text)]; QMessageBox.question answers msgs.answer (default No)."""
    box = _Box()
    box_answer = types.SimpleNamespace(value=QMessageBox.No)

    def info(*a, **k):
        box.append(('info', a[2]))
        return QMessageBox.Ok

    def question(*a, **k):
        box.append(('question', a[2]))
        return box_answer.value

    monkeypatch.setattr(QMessageBox, 'information', staticmethod(info))
    monkeypatch.setattr(QMessageBox, 'question', staticmethod(question))
    monkeypatch.chdir(tmp_path)
    import debyetools.tpropsgui.atomtools as at
    reset = getattr(at.REFERENCES, '__init__', None) if hasattr(at, 'REFERENCES') else None
    if reset:
        reset()  # session store of the reference energies
    box.answer = box_answer
    yield box
    if reset:
        reset()


class _Box(list):
    pass


def texts(box):
    return ' | '.join(t for _, t in box)


# ----------------------------------------------------------------------------------------------------------- helpers
def summary(mat):
    return str(next((TI / mat).glob('SUMMARY*')))


def eos_params(mat):
    from debyetools.aux_functions import load_V_E
    from debyetools.potentials import BM
    V, E = load_V_E(summary(mat), str(TI / mat / 'CONTCAR.5'), units='J/mol')
    eos = BM()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        eos.fitEOS(V, E)
    return eos


def nu_of(mat):
    from debyetools.aux_functions import load_EM
    from debyetools.poisson import poisson_ratio
    return poisson_ratio(load_EM(str(TI / mat / 'OUTCAR.eps')))


def run_cp(qapp, box, mat, formula, mass, T='0.1 1000.1 100', P='0', nu=None, mode=1, setup=None):
    """StartWindow -> main window -> Cp window with BM parameters fitted to the test E(V) data."""
    from debyetools.tpropsgui.start_window import StartWindow
    sw = StartWindow()
    sw.app = qapp
    sw.ui.lineEdit_compoundname.setText(formula)
    sw.ui.lineEdit_mass.setText(str(mass))
    sw.showDialogNext()
    mw = sw.dialogmainwindow
    eos = eos_params(mat)
    mw.ui.lineEdit_2.setText(', '.join('%.9e' % p for p in eos.pEOS))
    mw.ui.lineEdit_3.setText('%.4f' % (nu_of(mat) if nu is None else nu))
    mw.ui.lineEdit_T.setText(T)
    mw.ui.lineEdit_P.setText(P)
    mw.cp_window.ui.radioButton.setChecked(mode == 1)
    mw.cp_window.ui.radioButton_2.setChecked(mode == 2)
    if setup is not None:
        setup(mw)
    box.clear()
    with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter('ignore')
        mw.on_pushButton_Cp()
    return mw, mw.cp_window, eos


def at298(tp, key):
    return tp[key][int(np.argmin(np.abs(tp['T'] - 298.15)))]


# -------------------------------------------------------------------------------------------------- Cp window (main)
def test_cp_window_element_export(qapp, msgs):
    """Al: full run, H298 of a pure element = 0 (DH298), S298, export button = dtoutput4cmpnd (G6, G7, G14)."""
    mw, cw, _ = run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL, P='0 10 10')
    assert cw.H298_kind == 'DH298' and cw.H298 == 0.0
    assert cw.S298 == pytest.approx(26.8184, rel=1e-4)  # E0= energies (C-DOC3); 26.8999 with F=
    out = Path('dtoutput4cmpnd').read_text()
    cw.on_pushExport()
    assert Path('export_dtoutput4cmpnd').read_text() == out
    fields = out.split('$')
    assert fields[0] == 'Al' and len(fields[3].split('&')) == 6
    assert cw.ui.tableWidget.verticalHeaderItem(8).text() == 'H298 export (DH298)'
    assert 'POTCAR not read from an OUTCAR' in texts(msgs)


def test_r_is_one_for_compounds(qapp, msgs):
    """CaO per mol-atom: Cp(298) ~ 21 J/mol-atom/K (was 46 with r = number of element types, G1)."""
    mw, cw, _ = run_cp(qapp, msgs, 'CaO_Fm3m', 'CaO', 0.0280385)
    assert mw.molecule.r == 1
    assert at298(cw.dict_tp['0.0'], 'Cp') == pytest.approx(20.94, abs=0.05)


def test_truncation_and_grids(qapp, msgs):
    """Li to 3000 K: truncation reported, no FactSage fit on < 6 points; P list without 0; T grid from 0 K (G6, G7, G12)."""
    mw, cw, _ = run_cp(qapp, msgs, 'Li_bcc', 'Li', M_LI, T='0.1 3000.1 100')
    t = texts(msgs)
    assert 'no stable equilibrium volume' in t and 'fewer than 6 temperatures' in t
    assert np.all(np.isnan(cw.dict_FS['0.0']['Cp']))
    mw, cw, _ = run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL, P='5 15 10')
    assert cw.P_ref == 5e9
    mw, cw, _ = run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL, T='0 1000 300')
    T = cw.dict_tp['0.0']['T']
    assert T[0] == pytest.approx(0.1) and np.any(np.abs(T - 298.15) < 1e-9) and T[-1] <= 1000
    assert cw._grid('0 1000 300').tolist() == [0, 300, 600, 900] and cw._grid('5').tolist() == [5]


def test_close_pressures_keep_their_own_results(qapp, msgs):
    """Pressures closer than 0.05 GPa get distinct labels (were merged by '%.1f' and overwrote each other, G17);
    a pressure without a stable volume is skipped in the plots."""
    mw, cw, _ = run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL, T='0.1 600.1 100', P='0 0.1 0.02')
    keys = list(cw.dict_tp)
    assert keys == ['0.00', '0.02', '0.04', '0.06', '0.08', '0.10']
    assert [cw.ui.comboBox.itemText(i) for i in range(cw.ui.comboBox.count())] == keys
    V298 = [at298(cw.dict_tp[k], 'V') for k in keys]
    assert np.all(np.diff(V298) < 0)  # one volume per pressure, decreasing with P
    assert cw.pkey(cw.P_ref) == '0.00' and cw.H298_kind == 'DH298'
    mw, cw, _ = run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL, T='0.1 600.1 100', P='0 10 10')
    assert list(cw.dict_tp) == ['0.0', '10.0']  # usual grids keep one decimal
    mw, cw, _ = run_cp(qapp, msgs, 'Li_bcc', 'Li', M_LI, T='0.1 300.1 100', P='-3 3 3')
    assert cw.dict_tp['-3.0'] == '' and isinstance(cw.dict_tp['0.0'], dict)
    assert len(cw.lines) == 2  # -3 GPa (no stable volume) not plotted
    assert 'P = -3.0 GPa: no stable volume' in texts(msgs)


def test_explicit_anharmonicity_and_excess_boxes(qapp, msgs):
    """Excess polynomial read only when its box is checked; explicit anharmonicity only with its own box (G4)."""
    def g298(setup):
        return at298(run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL, nu=0.337, setup=setup)[1].dict_tp['0.0'], 'G')
    g0 = g298(None)

    def xs_only(mw):
        mw.check_xspol.setChecked(True)
        mw.ui.lineEdit_xspol.setText('100')

    def anh_only(mw):
        mw.check_xs.setChecked(True)
        mw.ui.lineEdit_xs.setText('1e-4')
        mw.ui.lineEdit_xspol.setText('100')
    assert g298(xs_only) - g0 == pytest.approx(100.0, abs=1e-6)
    assert g298(anh_only) - g0 == pytest.approx(-1e-4 * 298.15 ** 2 / 2, rel=1e-3)


def test_cp_T3_switch(qapp, msgs):
    """T^-3 check box refits without recomputing; off again restores the export exactly (G16)."""
    from debyetools.fs_compound_db import fit_FS
    mw, cw, _ = run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL)
    out0 = Path('dtoutput4cmpnd').read_text()
    cw.checkCpT3.setChecked(True)
    ref = fit_FS(cw.dict_tp['0.0'], cw.FS_Tfrom, cw.FS_Tto, cp_T3=True)['Cp']
    assert np.allclose(cw.dict_FS['0.0']['Cp'], ref, rtol=0, atol=0) and ref[5] != 0
    assert Path('dtoutput4cmpnd').read_text() != out0
    cw.checkCpT3.setChecked(False)
    assert Path('dtoutput4cmpnd').read_text() == out0


# ------------------------------------------------------------------------------------ formation enthalpy (G2, G14)
def test_formation_enthalpy_from_element_runs(qapp, msgs):
    """Al3Li L12: static Ef alone; DH298 after Al and Li runs in the same session (G2, G14)."""
    m = (3 * M_AL + M_LI) / 4
    mw, cw, _ = run_cp(qapp, msgs, 'Al3Li_L12', 'Al3Li', m)
    assert cw.H298_kind == 'static Ef' and cw.H298 == pytest.approx(-38062.1, abs=1)
    assert 'No H298 reference for Al (Al), Li (Li)' in texts(msgs)
    run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL)
    run_cp(qapp, msgs, 'Li_bcc', 'Li', M_LI)
    mw, cw, _ = run_cp(qapp, msgs, 'Al3Li_L12', 'Al3Li', m)
    assert cw.H298_kind == 'DH298' and cw.H298 == pytest.approx(-38343.0, abs=1)  # -38015.1 with F=
    assert cw.S298 == pytest.approx(83.176, abs=1e-3)
    assert Path('dtoutput4cmpnd').read_text().split('$')[1] == '%.7e' % cw.H298


def test_reference_energy_dialog(qapp, msgs):
    """CaO: O missing -> nan + note; values entered in the dialog -> hand value; POTCAR names from an OUTCAR (G2)."""
    import debyetools.tpropsgui.atomtools as at
    from debyetools.constants import EV_ATOM_TO_J_MOL
    mw, cw, eos = run_cp(qapp, msgs, 'CaO_Fm3m', 'CaO', 0.0280385)
    assert np.isnan(cw.Ef) and 'No reference energy for O (O)' in texts(msgs)
    cw.on_pushRefs()
    d = cw.dialog_refs
    d.table.item(0, 2).setText('Mg_pv')  # not a POTCAR of Ca
    d.table.item(1, 3).setText('abc')
    assert "'Mg_pv' is not a POTCAR of Ca" in texts(msgs) and "'abc' is not a number" in texts(msgs)
    d.table.item(0, 2).setText('Ca_sv')
    d.table.item(1, 3).setText('-4.9')
    d.on_ok()
    hand = 2 * (eos.E0(eos.V0) - (at.atom_energy['Ca_sv'] - 4.9) / 2 * EV_ATOM_TO_J_MOL)
    assert cw.Ef == pytest.approx(hand, rel=1e-6)
    # POTCAR names: exact lookup (V_sv, not V)
    found = at.REFERENCES.read_outcar(str(TI / 'V_bcc' / 'OUTCAR.eps'))
    assert found == {'V': 'V_sv'} and at.REFERENCES.energy('V_sv') == at.atom_energy['V_sv']
    with pytest.raises(ValueError):
        at.read_potentials(str(TI / 'CaO_Fm3m' / 'OUTCAR.eps'))  # moduli only, no TITEL


def test_reference_table_save_and_load(qapp, msgs):
    """Element runs saved to a CSV file and loaded in a new session give the same DH298 (reference-table workflow)."""
    import debyetools.tpropsgui.atomtools as at
    m = (3 * M_AL + M_LI) / 4
    run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL)
    run_cp(qapp, msgs, 'Li_bcc', 'Li', M_LI)
    mw, cw, _ = run_cp(qapp, msgs, 'Al3Li_L12', 'Al3Li', m)
    dh = cw.H298
    cw.on_pushRefs()
    d = cw.dialog_refs
    d.table.item(1, 3).setText('-1.95')  # an entered static energy for Li, kept in the file
    d.save_table('refs.csv')
    rows = Path('refs.csv').read_text().splitlines()
    assert rows[2].split(',') == at.REF_TABLE_COLUMNS
    assert any(r.startswith('Al,,') and ',run,Slater,' in r for r in rows)
    assert any(r.startswith('Li,-1.95,') for r in rows)
    d.reject()
    at.REFERENCES.__init__()  # new session
    mw, cw, _ = run_cp(qapp, msgs, 'Al3Li_L12', 'Al3Li', m)
    assert cw.H298_kind == 'static Ef'
    cw.on_pushRefs()
    d = cw.dialog_refs
    d.load_table('refs.csv')
    assert 'Press OK to apply' in texts(msgs)
    d.on_ok()
    assert cw.H298_kind == 'DH298' and cw.H298 == pytest.approx(dh, rel=1e-12)
    assert at.REFERENCES.edited == {'Li': -1.95} and set(at.REFERENCES.h298_runs) == {'Al', 'Li'}
    Path('bad.csv').write_text('POTCAR,E_ref_eV_atom,H298_J_mol_atom,H298_from,Debye_model,source\nAl,abc,,,,\n')
    msgs.clear()
    cw.on_pushRefs()
    cw.dialog_refs.load_table('bad.csv')
    assert 'line 2' in texts(msgs)


# ------------------------------------------------------------------------------------------- start window (G15)
def test_mean_mass_switch(qapp, msgs):
    from debyetools.tpropsgui.start_window import StartWindow
    from debyetools.tpropsgui.atomtools import atomic_mass
    sw = StartWindow()
    sw.app = qapp
    d = sw.dialogperiodictable
    d.updateFormula('Al', 3)
    d.updateFormula('Li', 1)
    d.close()
    arith = (3 * atomic_mass['Al'] + atomic_mass['Li']) / 4 / 1000
    assert float(sw.ui.lineEdit_mass.text()) == pytest.approx(arith, rel=1e-12)
    sw.radio_mass_log.setChecked(True)
    log = np.exp((3 * np.log(atomic_mass['Al']) + np.log(atomic_mass['Li'])) / 4) / 1000
    assert float(sw.ui.lineEdit_mass.text()) == pytest.approx(log, rel=1e-12)
    sw.showDialogNext()
    assert float(sw.dialogmainwindow.ui.lineEdit.text()) == pytest.approx(log, rel=1e-12)
    d.updateFormula('Al', 0)
    d.updateFormula('Li', 0)
    assert d.mass == 0  # was ZeroDivisionError


# ---------------------------------------------------------------------------------------------- dialogs (G5, G8, G11)
def test_doscar_dialog_pairs_files_with_their_volume(qapp, msgs):
    import random
    from debyetools.tpropsgui.dialog_doscar import dialogDoscar
    from debyetools.aux_functions import load_V_E, load_doscar
    from debyetools.electronic import fit_electronic
    d = TI / 'V_bcc'
    tags = ['-0.%02d' % i for i in range(10, -1, -1)] + ['0.%02d' % i for i in range(1, 11)]
    V, _ = load_V_E(str(d / 'SUMMARY.fcc'), str(d / 'CONTCAR.5'), units='J/mol')
    E, N, Ef = load_doscar(str(d / 'DOSCAR.EvV.'), tags)
    ref = fit_electronic(V, None, E, N, Ef)
    files = [str(d / ('DOSCAR.EvV.' + t)) for t in tags]
    dlg = dialogDoscar()
    dlg.external_iparams = QLineEdit()
    for fl, Vd in [(sorted(files), V), (random.Random(1).sample(files, len(files)), None)]:
        dlg.filepath_list, dlg.Vdata = fl, Vd
        dlg.ui.lineEdit_el.setText('')
        dlg.on_pushCalc()
        q = np.array([float(x) for x in dlg.ui.lineEdit_el.text().split(',')])
        NfV = lambda p: p[0] + p[1] * V + p[2] * V ** 2 + p[3] * V ** 3
        assert np.max(np.abs(NfV(q) / NfV(ref) - 1)) < 1e-6
    msgs.clear()
    dlg.filepath_list = []
    dlg.on_pushCalc()
    assert msgs  # no files -> message, no exception


def test_eos_fit_dialog(qapp, msgs):
    from debyetools.tpropsgui.dialog_fitEOS import dialogFitEOS
    from debyetools.aux_functions import load_V_E
    V, E = load_V_E(summary('Al_fcc'), str(TI / 'Al_fcc' / 'CONTCAR.5'))
    good = '#V E\n' + '\n'.join('%.6e %.6e' % (v, e) for v, e in zip(V, E))

    def fit(text, p0):
        dlg = dialogFitEOS()
        dlg.ui.comboBox_2.clear()
        dlg.ui.comboBox_2.addItem('Birch-Murnaghan')
        dlg.ui.EvVText_2.setPlainText(text)
        dlg.ui.lineEdit_3.setText(p0)
        dlg.molecule, dlg.molecule_from_crystal = types.SimpleNamespace(), None
        msgs.clear()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            dlg.on_pushButton_fitEOS()
        return dlg.ui.lineEdit_3.text()
    p = [float(x) for x in fit(good, '').split(',')]
    assert len(p) == 4 and not msgs
    p2 = [float(x) for x in fit(good, '0, 1e-4, 1e6, 40').split(',')]
    assert np.allclose(p, p2, rtol=1e-6) and msgs  # rejected start reported, same fit
    assert fit('garbage x', '') == '' and msgs


def test_load_dialogs_read_on_ok(qapp, msgs):
    from debyetools.tpropsgui.dialog_loadEOS import dialogLoadEOS
    from debyetools.tpropsgui.dialog_loadElastic import dialogLoadElastic
    le = dialogLoadEOS()
    le.EvVtext = QPlainTextEdit()
    le.show()
    le.ui.summarypath.setText('')
    le.ui.poscarpath.setText('')
    le.on_pushButton_OK()
    assert le.isVisible() and msgs
    le.close()  # no exception without OK
    le.show()
    le.ui.summarypath.setText(summary('Al_fcc'))
    le.ui.poscarpath.setText(str(TI / 'Al_fcc' / 'CONTCAR.5'))
    msgs.clear()
    le.on_pushButton_OK()
    assert not le.isVisible() and len(le.EvVtext.toPlainText().splitlines()) > 5 and not msgs
    E_txt = float(le.EvVtext.toPlainText().splitlines()[1].split()[1])
    assert E_txt == pytest.approx(-.12831042E+02 / 4, abs=1e-6)  # E0= of the first line (C-DOC3)
    le.show()
    le.ui.summarypath.setText(summary('CaO_Fm3m'))  # 'E0= 0' placeholders: F= read, with a note
    le.ui.poscarpath.setText(str(TI / 'CaO_Fm3m' / 'CONTCAR.5'))
    le.on_pushButton_OK()
    assert not le.isVisible() and "no usable 'E0=' value" in texts(msgs)
    lE = dialogLoadElastic()
    lE.elastic_constants = QTextEdit()
    lE.show()
    msgs.clear()
    lE.ui.outcarpath.setText('nope')
    lE.on_pushButton_OK()
    assert lE.isVisible() and msgs
    lE.ui.outcarpath.setText(str(TI / 'Cr_bcc' / 'OUTCAR.eps'))
    lE.on_pushButton_OK()
    assert lE.elastic_constants.toPlainText().startswith('# GPa, Voigt order')
    import debyetools.tpropsgui.atomtools as at
    assert at.REFERENCES.potentials == {'Cr': 'Cr_pv'}  # POTCAR names read with the moduli (G2)


# ------------------------------------------------------------------------------------------------ crystal dialog (G9)
def test_crystal_dialog_cutoff_and_initial_guess(qapp, msgs):
    from PySide6.QtWidgets import QTableWidgetItem
    from debyetools.tpropsgui.dialog_crystal import dialogCrystal
    from debyetools.tpropsgui.atomtools import Molecule
    from debyetools.aux_functions import load_cell
    f, c, b = load_cell(str(TI / 'CaO_Fm3m' / 'CONTCAR.5'))
    dc = dialogCrystal()
    dc.molecule, dc.eos_str = Molecule(), 'MP'
    for i in range(3):
        for j in range(3):
            dc.ui.tableCell.setItem(i, j, QTableWidgetItem(str(c[i, j])))
    dc.ui.tableBasis.setRowCount(len(b) + 1)
    for i, (row, t) in enumerate(zip(b, ['Ca'] * 4 + ['O'] * 4)):
        for j in range(3):
            dc.ui.tableBasis.setItem(i, j, QTableWidgetItem(str(row[j])))
        dc.ui.tableBasis.setItem(i, 3, QTableWidgetItem(t))
    dc.ui.lineEditNnn.setText('3')
    dc.ui.lineEditCutoff.setText('4.5')
    with contextlib.redirect_stdout(io.StringIO()):
        dc.on_pushButton_create_cell_clicked()
    assert dc.molecule.cutoff == 4.5
    assert len(dc.ui.lineEditInitialGuess.text().split(',')) == 3 * len(dc.molecule.combs_types) == 9


# ------------------------------------------------------------------------------- interatomic potentials (Morse, EAM)
def crystal_path(qapp, box, mat, name, mass, eos_text):
    """Start window with the crystal option -> crystal dialog (CONTCAR) -> main window -> EOS fit dialog -> Cp."""
    import re
    from PySide6.QtWidgets import QTableWidgetItem
    from debyetools.tpropsgui.start_window import StartWindow
    from debyetools.aux_functions import load_cell, load_V_E
    sw = StartWindow()
    sw.app = qapp
    sw.ui.lineEdit_compoundname.setText(name)
    sw.ui.lineEdit_mass.setText(str(mass))
    sw.ui.checkBox.setChecked(True)
    sw.showDialogNext()
    dc = sw.dialogcrystal
    f, c, b = load_cell(str(TI / mat / 'CONTCAR.5'))
    types = [el for el, n in re.findall(r'([A-Z][a-z]?)(\d*)', f) for _ in range(int(n or 1))]
    for i in range(3):
        for j in range(3):
            dc.ui.tableCell.setItem(i, j, QTableWidgetItem(str(c[i, j])))
    dc.ui.tableBasis.setRowCount(len(b) + 1)
    for i, (row, t) in enumerate(zip(b, types)):
        for j in range(3):
            dc.ui.tableBasis.setItem(i, j, QTableWidgetItem(str(row[j])))
        dc.ui.tableBasis.setItem(i, 3, QTableWidgetItem(t))
    dc.ui.lineEditNnn.setText('3')
    dc.ui.lineEditCutoff.setText('5')
    with contextlib.redirect_stdout(io.StringIO()):
        dc.on_pushButton_create_cell_clicked()
    dc.on_pushButton_goto_main()
    mw = sw.dialogmainwindow
    mw.ui.comboBox.setCurrentText(eos_text)
    mw.on_pushFitEOS()
    fd = mw.dialogFitEOS
    V, E = load_V_E(summary(mat), str(TI / mat / 'CONTCAR.5'))
    fd.ui.EvVText_2.setPlainText('#V E\n' + '\n'.join('%.6e %.6e' % (v, e) for v, e in zip(V, E)))
    box.clear()
    with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter('ignore')
        fd.on_pushButton_fitEOS()
    assert fd.ui.progress_3.value() == 100, texts(box)
    fd.on_pushSave()
    mw.ui.lineEdit_3.setText('%.4f' % nu_of(mat))
    mw.ui.lineEdit_T.setText('0.1 600.1 100')
    mw.ui.lineEdit_P.setText('0')
    with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter('ignore')
        mw.on_pushButton_Cp()
    return mw, fd


def test_eos_list_without_crystal(qapp, msgs):
    """Without the crystal option only the analytic EOS are offered (Morse and EAM need the structure)."""
    mw, cw, _ = run_cp(qapp, msgs, 'Al_fcc', 'Al', M_AL)
    items = [mw.ui.comboBox.itemText(i) for i in range(mw.ui.comboBox.count())]
    assert items == ['Birch-Murnaghan', 'Rose-Vinet', 'Mie-Gruneisen', 'TB-SMA', 'Murnaghan', 'Poirier-Tarantola']


@pytest.mark.parametrize('eos', ['Morse potential', 'EAM int. potential'])
def test_interatomic_potentials_end_to_end(qapp, msgs, eos):
    """Al fcc through the crystal dialog: Morse and EAM offered, start of the selected potential, fit, Cp run."""
    mw, fd = crystal_path(qapp, msgs, 'Al_fcc', 'Al', M_AL, eos)
    items = [mw.ui.comboBox.itemText(i) for i in range(mw.ui.comboBox.count())]
    assert items == ['Morse potential', 'EAM int. potential']
    n = len(mw.ui.lineEdit_2.text().split(','))
    assert n == {'Morse potential': 3, 'EAM int. potential': 10}[eos]  # 1 pair type, 1 element type
    assert mw.eos_str == {'Morse potential': 'MP', 'EAM int. potential': 'EAM'}[eos]
    assert type(mw.molecule.eos).__name__ == mw.eos_str
    cw = mw.cp_window
    tp = cw.dict_tp['0.0']
    assert at298(tp, 'Cp') == pytest.approx(23.9, rel=0.03)  # BM: 23.88 J/mol-atom/K
    assert mw.molecule.eos.V0 == pytest.approx(9.93e-6, rel=0.01) and cw.H298 == 0.0


# ------------------------------------------------------------------------------------ elastic properties (G10, G18-G23)
_IDX = {(0, 0): 0, (1, 1): 1, (2, 2): 2, (1, 2): 3, (2, 1): 3, (0, 2): 4, (2, 0): 4, (0, 1): 5, (1, 0): 5}


def _compliance(Cv):
    Sv = np.linalg.inv(Cv)
    T = np.zeros((3, 3, 3, 3))
    for (i, j), p in _IDX.items():
        for (k, l), q in _IDX.items():
            T[i, j, k, l] = Sv[p, q] * (1 if p < 3 else .5) * (1 if q < 3 else .5)
    return T


def _reference(T, d):
    """Young's modulus, linear compressibility (TPa^-1), shear and Poisson extrema over 3601 transverse directions."""
    t = np.array([1., 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1., 0])
    e1 = np.cross(d, t)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(d, e1)
    chi = np.linspace(0, np.pi, 3601)
    n = np.outer(np.cos(chi), e1) + np.outer(np.sin(chi), e2)
    s = np.einsum('ijkl,i,j,k,l', T, d, d, d, d)
    G = 1 / (4 * np.einsum('ijkl,i,nj,k,nl->n', T, d, n, d, n))
    nu = -np.einsum('ijkl,i,j,nk,nl->n', T, d, d, n, n) / s
    return 1 / s, 1000 * np.einsum('ijkk,i,j', T, d, d), (G.min(), G.max()), (nu.min(), nu.max())


def _elastic_dialog(mat):
    """Poisson dialog -> load OUTCAR -> More (report window); returns the report dialog, C (GPa) and the console text."""
    from debyetools.tpropsgui.dialog_calculateNu import dialogCalcNu
    d = dialogCalcNu()
    lE = d.dialog_loadElastic
    lE.elastic_constants = d.ui.elastic_constants
    lE.ui.outcarpath.setText(str(TI / mat / 'OUTCAR.eps'))
    lE.on_pushButton_OK()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        d.on_pushMore_calcElastic()
    return d.dialogElastic, np.array(d.dialogElastic.EM), out.getvalue()


MATS = ['Al_fcc', 'Ti_hcp', 'Nb2O5_P2']


@pytest.mark.parametrize('mat', MATS)
def test_elastic_report_averages(qapp, msgs, mat):
    """Voigt/Reuss/Hill table: K, E, G, nu in the right columns; A^U equal to the core poisson_ratio (G21)."""
    from debyetools.poisson import poisson_ratio
    de, C, _ = _elastic_dialog(mat)
    report = de.ui.plainTextEdit.toPlainText()
    BR, BV, B, GR, GV, G, AU, nu = poisson_ratio(C * 10, quiet=True)
    assert 'Universal anisotropy index (A^U): %.4f' % AU in report
    hill = [float(x) for x in report.split('Hill:')[1].split('\n')[0].split()]
    E = 9 * B * G / (3 * B + G)  # poisson_ratio takes kBar and returns the moduli in GPa
    assert hill == pytest.approx([B, E, G, nu], abs=2e-3)


@pytest.mark.parametrize('mat', MATS)
def test_elastic_report_extrema(qapp, msgs, mat):
    """Min/max of Young's modulus, shear modulus and Poisson's ratio over all directions (G22)."""
    import debyetools.tpropsgui.elastic_props as el
    _, C, _ = _elastic_dialog(mat)
    T = _compliance(C)
    vp = el.run_script(C)[1]['variation_properties']
    k = np.arange(3000) + 0.5
    th, ph = np.arccos(1 - 2 * k / 3000), np.pi * (1 + 5 ** 0.5) * k
    D = np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], 1)
    R = [_reference(T, x) for x in D[::3]]
    dense = {'Young': [r[0] for r in R], 'Shear2': [r[2][1] for r in R], 'Poisson': [r[3][0] for r in R],
             'Poisson2': [r[3][1] for r in R]}
    for key, vals in dense.items():
        assert vp[key]['min'] <= min(vals) + 1e-9 * abs(min(vals)) + 1e-3 * (max(vals) - min(vals))
        assert vp[key]['max'] >= max(vals) - 1e-9 * abs(max(vals)) - 1e-3 * (max(vals) - min(vals))
    assert vp['Young']['max'] == pytest.approx(_reference(T, np.array(vp['Young']['max_direction']))[0], rel=1e-9)


@pytest.mark.parametrize('mat', MATS)
def test_elastic_plots(qapp, msgs, mat):
    """Polar plots vs the tensor calculation, negative Poisson's ratio drawn (G18), exact transverse extrema (G19),
    second press not doubled (G20), no console copy of the report (G23)."""
    de, C, console = _elastic_dialog(mat)
    T = _compliance(C)
    de.on_pushPlots()
    de.on_pushPlots()
    p = de.dialog_plots
    dirs = {0: lambda a: np.array([np.cos(a), np.sin(a), 0]), 1: lambda a: np.array([np.cos(a), 0, np.sin(a)]),
            2: lambda a: np.array([0, np.cos(a), np.sin(a)])}
    for row, axs in enumerate([p.ax1, p.ax2, p.ax3, p.ax4]):
        for plane, ax in enumerate(axs):
            assert len(ax.lines) == [1, 1, 2, 3][row]  # not doubled by the second press
            for il, line in enumerate(ax.lines):
                a, r = line.get_xdata(), line.get_ydata()
                for kk in range(0, len(a), 7):
                    Eref, beta, G, nu = _reference(T, dirs[plane](a[kk]))
                    ref = [Eref, beta, G[il] if row == 2 else None,
                           [-min(0, nu[0]), max(0, nu[0]), nu[1]][il] if row == 3 else None][row]
                    assert r[kk] == pytest.approx(ref, rel=1e-5, abs=1e-6)
    assert console == ''

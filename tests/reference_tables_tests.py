"""GUI reference tables (no Qt): CSV round trip and the Materials Project placeholder script with fake entries."""
import types

import pytest

from debyetools.tpropsgui.atomtools import save_reference_table, load_reference_table, REF_TABLE_COLUMNS
from debyetools.tpropsgui.reference_tables import fetch_mp_references as fmp


def test_csv_round_trip(tmp_path):
    p = tmp_path / 'refs.csv'
    edited = {'O': -4.93, 'Li': -1.95}
    runs = {'Al': (-352459.1436, 'run Al (BM, Slater)', 'Slater')}
    entered = {'O': -470000.0}
    assert save_reference_table(str(p), edited, runs, entered) == 3
    assert load_reference_table(str(p)) == (edited, runs, entered)


def test_bad_rows_are_reported(tmp_path):
    p = tmp_path / 'bad.csv'
    p.write_text(','.join(REF_TABLE_COLUMNS) + '\nAl,1,2,maybe,,\n')
    with pytest.raises(ValueError, match='line 2'):
        load_reference_table(str(p))
    p.write_text('a,b\n')
    with pytest.raises(ValueError, match='not a reference table'):
        load_reference_table(str(p))


def _entry(formula_els, e, run_type='GGA', pot='PBE O', mid='mp-1', hubbard=False):
    comp = types.SimpleNamespace(elements=formula_els, reduced_formula=''.join(formula_els))
    return types.SimpleNamespace(composition=comp, uncorrected_energy_per_atom=e, entry_id=mid,
                                 parameters={'run_type': run_type, 'is_hubbard': hubbard, 'potcar_symbols': [pot]})


def test_mp_placeholder_rows_pick_lowest_plain_pbe(tmp_path):
    entries = {'O': [_entry(['O'], -4.90, mid='mp-a'), _entry(['O'], -4.95, mid='mp-b'),
                     _entry(['O'], -6.0, run_type='R2SCAN', mid='mp-c'), _entry(['Li', 'O'], -9.0, mid='mp-d')],
               'Mg': [_entry(['Mg'], -1.60, pot='PBE Mg_pv', mid='mp-153')],
               'Xx': []}
    rows = fmp.rows_for(['O', 'Mg', 'Xx'], lambda el: entries[el])
    assert [r[:2] for r in rows] == [['O', '-4.95'], ['Mg_pv', '-1.6']]
    assert 'mp-b' in rows[0][5] and 'placeholder' in rows[0][5]
    p = tmp_path / 'mp.csv'
    fmp.write_table(str(p), rows)
    edited, runs, entered = load_reference_table(str(p))
    assert edited == {'O': -4.95, 'Mg_pv': -1.6} and runs == {} and entered == {}


def test_mp_potcar_from_spec_or_missing(capsys):
    """Newer MP entries give the POTCAR as potcar_spec titles; an entry without a POTCAR name is skipped, not a crash."""
    spec = _entry(['N'], -8.3, mid='mp-n')
    spec.parameters = {'run_type': 'GGA', 'potcar_spec': [{'titel': 'PAW_PBE N 08Apr2002', 'hash': 'x'}]}
    none = _entry(['H'], -3.4, mid='mp-h')
    none.parameters = {'run_type': 'GGA', 'potcar_symbols': ['?']}
    rows = fmp.rows_for(['N', 'H'], lambda el: {'N': [spec], 'H': [none]}[el])
    assert [r[:2] for r in rows] == [['N', '-8.3']]
    assert 'H: no POTCAR name in mp-h' in capsys.readouterr().err

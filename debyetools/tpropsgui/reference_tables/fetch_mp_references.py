"""Placeholder elemental reference energies from the Materials Project, written as a GUI reference table.

For the elements that have no value in debyetools.tpropsgui.atomtools.atom_energy (or a broken one), this script
takes, for each element, the lowest-energy pure-element entry computed with plain PBE (run type 'GGA', not GGA+U
or r2SCAN) in the Materials Project, and writes its *uncorrected* energy per atom (eV/atom, no MP2020 fitted
corrections) with the POTCAR it was computed with. The file can be loaded in the Cp window with
Reference energies... -> Load table... .

These are placeholders: they come from MP's settings (520 eV cutoff, MP POTCAR choices, MP k-point density, and
for O, N, H, F, Cl, Br, I a molecular crystal, not the isolated molecule). Replace them with your own calculations
done with the same settings as the compound (see README.md in this folder).

Usage (needs an MP API key, https://next-gen.materialsproject.org/api, and recent packages:
`pip install -U mp-api pymatgen`; an older pymatgen fails with "No module named 'pymatgen.core.entries'"):

    python fetch_mp_references.py --api-key YOUR_KEY            # or set MP_API_KEY
    python fetch_mp_references.py --elements O N Sb --out my.csv
"""
import argparse
import csv
import datetime
import os
import re
import sys

# elements without a value in atom_energy (Z <= 94, noble gases left out), plus Mg for Mg_pv / Mg_sv
DEFAULT_ELEMENTS = ['H', 'N', 'O', 'F', 'P', 'S', 'Cl', 'Br', 'I', 'Sb', 'Sm', 'Mg',
                    'Th', 'Pa', 'U', 'Np', 'Ra', 'Fr', 'Po', 'At']
COLUMNS = ['POTCAR', 'E_ref_eV_atom', 'H298_J_mol_atom', 'H298_from', 'Debye_model', 'source']  # = REF_TABLE_COLUMNS


def potcar_name(symbol):
    """'PBE Mg_pv' or 'PAW_PBE Mg_pv 06Sep2000' -> 'Mg_pv'."""
    words = symbol.split()
    return words[1] if len(words) > 1 else words[0]


def best_gga_entry(element, entries):
    """Lowest uncorrected energy per atom among the plain-PBE entries made only of `element`.
    entries: objects with .composition (pymatgen), .uncorrected_energy_per_atom, .parameters, .entry_id."""
    pure = [e for e in entries
            if [str(el) for el in e.composition.elements] == [element]
            and e.parameters.get('run_type', '') == 'GGA'
            and not e.parameters.get('is_hubbard', False)]
    return min(pure, key=lambda e: e.uncorrected_energy_per_atom) if pure else None


def rows_for(elements, get_entries):
    """Rows of the reference table; get_entries(element) -> list of entries. Elements without a GGA entry are
    reported on stderr and left out."""
    today = datetime.date.today().isoformat()
    rows = []
    for el in elements:
        entry = best_gga_entry(el, get_entries(el))
        if entry is None:
            print('%s: no plain-PBE entry in the Materials Project, skipped' % el, file=sys.stderr)
            continue
        pots = entry.parameters.get('potcar_symbols') or ['?']
        pot = potcar_name(pots[0])
        if re.match('[A-Z][a-z]?', pot).group(0) != el:
            print('%s: unexpected POTCAR %r, skipped' % (el, pot), file=sys.stderr)
            continue
        rows.append([pot, repr(round(float(entry.uncorrected_energy_per_atom), 6)), '', '', '',
                     'placeholder: Materials Project %s %s, PBE (GGA) uncorrected, 520 eV, retrieved %s'
                     % (entry.entry_id, entry.composition.reduced_formula, today)])
    return rows


def write_table(path, rows):
    with open(path, 'w', newline='') as f:
        f.write('# debyetools reference energies (GUI). E_ref: static energy, eV/atom; H298: H at 298.15 K, J/mol-atom,\n'
                '# PLACEHOLDERS from the Materials Project (fetch_mp_references.py): MP settings, not yours.\n')
        w = csv.writer(f)
        w.writerow(COLUMNS)
        w.writerows(rows)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--api-key', default=os.environ.get('MP_API_KEY'))
    p.add_argument('--elements', nargs='+', default=DEFAULT_ELEMENTS)
    p.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mp_placeholders_PBE.csv'))
    a = p.parse_args(argv)
    if not a.api_key:
        p.error('an MP API key is needed (--api-key or MP_API_KEY)')
    from mp_api.client import MPRester
    with MPRester(a.api_key) as mpr:
        def get_entries(el):
            return mpr.get_entries(el, compatible_only=False, additional_criteria={'thermo_types': ['GGA_GGA+U']})
        try:
            rows = rows_for(a.elements, get_entries)
        except ModuleNotFoundError as e:
            if 'pymatgen' not in str(e):
                raise
            sys.exit('%s\nThe Materials Project server sends classes that this pymatgen does not have; update both '
                     'packages:  pip install -U pymatgen mp-api' % e)
    write_table(a.out, rows)
    print('%d element(s) written to %s' % (len(rows), a.out))
    for r in rows:
        print('  %-8s %12s  %s' % (r[0], r[1], r[5]))


if __name__ == '__main__':
    main()

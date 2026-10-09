# Elemental reference tables for the GUI formation energy / enthalpy

The Cp window computes

* the static formation energy `Ef = nats·(E0(V0) − mean_i E_i^ref)` from the elemental reference energies
  `E_ref` (eV/atom) of the exact POTCAR used for each element, and
* the formation enthalpy exported to FactSage, `ΔH298 = H_cmp(298.15) − Σ n_i H_i(298.15)`, from the elements'
  `H298` (J/mol-atom, same energy scale as the E(V) data).

Built-in values: `atomtools.atom_energy` (copy of `examples/Nb/calculations/elements_energies.out`; PBE PAW,
ground-state structure of each POTCAR; Al agrees with the Materials Project value to 1 meV/atom). The values are
consistent with VASP's `E0=` (energy at σ → 0), the energy `load_V_E` reads: the E0 fits of the V_sv, Cu and
Li_sv test sets agree to about 1 meV/atom, the `F=` fits differ by up to 8 meV/atom (V). Values added by hand
should also be E0 (σ → 0). Missing there:
H, N, O, F, P, S, Cl, Br, I, Sb, Sm, Mg_pv, Mg_sv, Th, Pa, U, Np, Ra, Fr, Po, At, noble gases.

Any value can be added or overridden for a session in **Reference energies…** and kept in a CSV file with
**Save table… / Load table…** (format below). Files in this folder:

| File | Content |
|------|---------|
| `fetch_mp_references.py` | writes `mp_placeholders_PBE.csv`: lowest-energy plain-PBE (GGA) entry of each missing element in the Materials Project, *uncorrected* energy per atom and its POTCAR. Placeholders only (MP settings). Needs `pip install mp-api` and an MP API key. |
| `mp_placeholders_PBE.csv` | output of the script (once run). |

## CSV format

```
# comment lines start with '#'
POTCAR,E_ref_eV_atom,H298_J_mol_atom,H298_from,Debye_model,source
O,-4.9,,,,"placeholder: ..."
Al,,-352459.14,run,Slater,"run Al (BM, Slater)"
```

`E_ref_eV_atom` and `H298_J_mol_atom` may be empty; `H298_from` is `run` (pure-element run in the GUI) or
`entered`.

## Computing your own references (replaces the placeholders)

Use **exactly** the settings of the compound calculations: same POTCAR files (PBE set and version), ENCUT,
PREC, smearing, k-point density (per Å⁻¹), and the same EDIFF. The reference energy is the total energy per atom
(`energy(sigma->0)` / number of atoms) of the fully relaxed ground state.

**Solids** (Sb, Sm, Mg_pv, Mg_sv, P, S, Br, I, actinides): relax cell and ions (`IBRION = 2`, `ISIF = 3`, then a
final static run at the relaxed volume, or an E(V) series like the compound). Ground states commonly used:
Sb A7 (R-3m), Mg hcp, Sm α-Sm (R-3m, Sm_3 = f in core), P black (Cmce), S α-S8 (Fddd, large cell), Br2 and I2
molecular crystals (Cmce), Th fcc, Pa bct, U α (Cmcm), Np α (Pnma). Check magnetism (`ISPIN = 2`) where relevant
and keep spin–orbit coupling consistent with the compound.

**Diatomic gases** (H2, N2, O2, F2, Cl2): one molecule in a large asymmetric box (e.g. 15 × 15.5 × 16 Å),
Γ point only, `ISPIN = 2`, `ISMEAR = 0`, small `SIGMA` (≤ 0.01), relax the bond (`IBRION = 2`, `ISIF = 2`); O2 is a
triplet (`NUPDOWN = 2`), the others singlets. `E_ref = E(X2)/2`. PBE overbinds O2 (by ≈ 1 eV per molecule):
whether to apply a fitted correction is a choice left open (decision pending). For `H298` of a gas, the per-atom
value is `½·[E(X2)·N_A·e + ZPE + 7/2·R·298.15]` with the zero-point energy from a frequency calculation
(`IBRION = 5`); also pending.

Enter or load the values, check them in the table (E ref and H298 columns), and save the table for later sessions.

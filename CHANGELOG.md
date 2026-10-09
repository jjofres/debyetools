# Changelog

## 3.0.0 (2026-10)

Version 3.0.0 is the result of a complete review of the code (formulas, derivatives, units, file readers,
fitting, GUI and documentation). The public API is almost unchanged, but **the same inputs give different
numbers than in 2.8.3**: several formulas were wrong, some defaults changed, and V(T) is now solved exactly.
Do not compare 3.0.0 results with 2.8.3 results without checking the list below. Where the old behaviour is
still available, the argument that restores it is given.

All inputs and outputs are SI per mole of atoms (V in m³/mol-at, energies in J/mol-at, pressures and moduli in
Pa, mass in kg/mol-at).

### Changes that give different results

**Input files**

- `load_V_E` reads the energy after the label `E0=` (energy extrapolated to zero smearing, σ → 0) instead of
  the 4th column, which is `F=` (VASP's TOTEN, E − σS, an electronic entropy at the smearing temperature σ/k_B
  that the separate electronic term counts again). Effect on the Al example data (Fermi smearing,
  σ = 0.1 eV): E(V) shifted by 2–4 meV/atom, K0 +0.5 %, α(298 K) −1.4 %, Cp(1000 K) −0.3 J/mol-at/K.
  `load_V_E(..., energy='F')` reproduces 2.8.3. Lines without a usable `E0=` (missing, or `E0= 0`) read `F=`,
  lines without labels read column 4; both warn.
- `load_V_E`, `load_cell`: new POSCAR/CONTCAR reader. The reference volume is |det(cell)| × scale / atoms (was
  the product of the cell diagonal, without the scale factor – wrong for scale ≠ 1 and non-orthogonal cells).
  Negative scale (= volume), three scale factors, Cartesian coordinates, Selective dynamics and VASP 4 files are
  read correctly; SUMMARY lines may have any spacing.
- `load_EM` returns the relaxed-ion elastic constants (`TOTAL ELASTIC MODULI`, or `SYMMETRIZED` + ionic
  relaxation contribution) instead of the clamped-ion `SYMMETRIZED ELASTIC MODULI`. ν changes for structures
  with internal relaxation, e.g. hcp Ti 0.306 → 0.343, D0₂₃ Al₃Sr 0.255 → 0.346; fcc, bcc and L1₂ are
  unchanged. `load_EM(..., block='clamped')` reproduces 2.8.3.
- `load_doscar` reads only the total-DOS block and sums both spin channels for ISPIN = 2 (2.8.3 used spin up
  only and also read the projected blocks); the DOS is per atom.
- `get_elastic.get_EM` returns kBar like `load_EM` (was GPa), and `parse_outcar` takes the volume of the final
  cell (2.8.3 took the first "volume of cell", which can be the primitive cell: Nb C11 578 → 289 GPa).

**Electronic contribution**

- F_el = −(π²/6) k_B² T² N(E_F)(V) with N(E_F) the total DOS (spins summed, per atom), evaluated in every DOSCAR
  at its own Fermi level and fitted with a cubic in V (`fit_electronic(..., mode='dos')`, default). 2.8.3 used a
  single-DOS scaling with the wrong volume trend and spin-up only: |F_el| was 1.7–2.9 times too small and
  dlnN/dlnV had the wrong sign for most metals. `mode='scaling'` gives N(E_F)(V0)·(V/V0)^(2/3) from one DOS.
- The electronic term also uses the constants of `debyetools.constants`.

**Free-energy minimisation**

- `nDeb.min_G` solves ∂F/∂V + P = 0 exactly (bracketed root, following the stable branch from one temperature
  to the next) instead of minimising F with `fmin`. V(T) changes by 1e-5 to 1e-3 relative (noise and pressure
  residuals of up to 20 MPa removed; |P| now < 1e-3 Pa).
- `min_G` stops at the last temperature with a mechanically stable volume (K_T > 0, finite θ_D) and warns
  (UserWarning with T and reason); **the returned T and V can be shorter than the input T**. The status of every
  temperature is in `nDeb.min_G_info`. 2.8.3 returned unstable or spinodal states.
- The reference volume V0_DM of the Debye modes Sl, DM, VZ and mfv is the EOS V0 (was V at the first
  temperature after one pass): θ_D +0.3 to +0.6 % for DM, VZ and mfv.
- EOS V0 is the fitted V0 parameter (Morse and EAM: the root of dE0/dV), not a bounded minimisation that
  stopped up to 5e-4 short of the minimum.

**Per-mol-atom convention (r)**

- The vibrational and vacancy free energies and all their derivatives carry r consistently; with all inputs
  per mol-atom, r = 1 and r cancels exactly. nDeb warns when r ≠ 1 (formula-unit inputs). The GUI used
  r = number of element types: compound Cp was multiplied by that number (CaO 46.0 → 21.0 J/mol-at/K) – it now
  uses r = 1.

**Formula and derivative corrections**

- Non-jj Debye modes (Sl, DM, VZ, mfv) with intrinsic anharmonicity: the θ_D derivatives include the
  anharmonic factor (were missing; S at 10 K ×3.7, Cp −2 % at 1000 K). Sl now equals jjsl.
- jjdm and jjfv: 4th volume derivative of θ_D (affects K_T″ and G²).
- Rose–Vinet 6th derivative, EAM 5th and 6th derivatives, vacancy 4th volume derivative (K_T″, K_S′, dCp/dP).
- `eval_props`: Evib = Fvib + T·Svib (sign error).
- `eval_Cp` equals `eval_props(...)['Cp']` (excess term and r factors were missing).
- Debye function and derivatives rewritten (series for x < 2, exact asymptotic form above): no clamps, correct
  T³ law at low temperature (Cp(0.1 K) 1.05e-4 → 8.97e-5 J/mol-at/K) and no 1e10 penalty in `F` above 25 θ_D.
- Unit constants: exact SI-2019 values in `debyetools.constants` everywhere (were mixed rounded values;
  changes of 1e-6 to 4e-4).
- Voigt–Reuss–Hill averages with the Reuss bounds from the compliance matrix: exact for every symmetry
  (trigonal Al₂O₃ and monoclinic Nb₂O₅ were wrong).
- Pair analysis: neighbour search exact for any cell shape and cut-off; a shell lying exactly at the cut-off is
  its own shell (was merged into the previous one).

**Fitting**

- EOS fits minimise least-squares residuals with V0 > 0, B0 > 0 bounds; each fit is checked (finite, minimum
  exists, B0 > 0, V0 near the data, rms ≤ `rel_tol` × energy range) and other starting points are tried if it
  fails (UserWarning naming the rejected start). If none passes, `EOSFitError` is raised
  (`on_failure='warn'` keeps the best attempt). Attempts are in `eos.fit_info`.
- `fit_FS` (FactSage parameters) solves the four fits exactly by linear least squares. The T⁻³ coefficient of Cp
  is 0 unless `cp_T3=True` (2.8.3 left it at its start value 1.0, i.e. effectively the same 5-term fit). The fit
  window no longer needs T_from and T_to on the temperature grid. The return value is the same dict
  ('Cp', 'a', '1/Ks', 'Ksp').
- `optim.ga_fitting`: exact elitism (the best fitness never gets worse), failed or non-finite model evaluations
  get infinite error instead of stopping the run.
- `gen_Ts`, `gen_Ps`: `linspace` grids; 2.8.3 could return points beyond the last temperature (e.g. up to
  1333 K for `gen_Ts(0.1, 1000.1, 4)`) and too few pressures.

### New

- `load_V_E(..., energy='E0' | 'F')`; `load_EM(..., block='relaxed' | 'clamped')`.
- `fitEOS(..., rel_tol, max_starts, on_failure)`, `potentials.EOSFitError`, `eos.fit_info`; the analytic EOS
  fit without initial parameters (start from the data); `MP.default_initial_parameters`.
- `fit_electronic(..., mode, V0, sigma, order)`, `electronic.N_at_Fermi`.
- `fit_FS(..., cp_T3=False)`.
- `nDeb.min_G_info`.
- Excess term: each coefficient A_i can be a polynomial in V (`xsparams`).
- `optim.ga_fitting(..., zero_scale, seed)`.
- `load_data_from_DFT.extract_from_DFT(..., vi, vf, step, ref, energies_file)`.
- `debyetools.constants`.
- GUI:
  - EAM can be selected (with a crystal).
  - Reference-energies table: POTCAR read from the OUTCAR, values editable, saved and loaded as CSV.
    Materials Project placeholders are in `tpropsgui/reference_tables`.
  - Exported H298 = ΔH298 from pure-element runs of the same session, with the static formation energy as
    fallback.
  - Arithmetic or logarithmic mean mass; T⁻³ switch for the FactSage Cp fit.
  - DOSCARs paired with their volumes in any file order.
  - Elastic constants in Voigt order; corrected elastic averages, extrema and plots.
  - Messages instead of silent failures (EOS fit, file loading, truncated V(T)).
  - Pressure labels that stay distinct for small pressure steps.

### Deprecated and removed

- `BM3` is an alias of `BM` with a DeprecationWarning (its derivatives had wrong signs).
- `BM4` and `MU2` are placeholders (not validated) and warn when created.
- `nDeb(..., units=...)` is ignored (DeprecationWarning).
- Removed: `Vibrational.set_theta_4minF`, `Vibrational.set_int_anh_4minF` (internal) and dead code; the
  dependencies `mpmath`, `deap` and `pandas`.

### Requirements

- Python 3.10–3.12 (the GUI did not start on Python 3.10 and 3.11 in 2.8.3), numpy 1.26 or 2.x, scipy ≥ 1.11.

### Documentation and tests

- Documentation rewritten and checked against the code: every example runs (doctests), file formats, units,
  GUI; the PDF and ePub builds work.
- Regression baseline (2876 values) and tests for the core, the file readers, the documentation examples and the
  GUI (headless).

# Superconducting Qubit Lab

A minimal open research environment for exploring the physics of superconducting qubits using reproducible Python simulations.

This project implements the first numerical foundations required to study LC resonators, Josephson junctions and transmon qubits.
The current implementation focuses on physically correct baseline models and executable validations.

The long-term goal is to grow this into an interactive superconducting qubit simulation lab including circuit QED, control pulses, noise models and benchmarking tools.

---

# Current Status

Phase 1 is implemented and validated.

Implemented modules:
- LC resonator physics
- Josephson junction energy model
- Transmon qubit Hamiltonian baseline
- Numerical spectrum calculation
- Charge dispersion estimation
- Automated tests

Not yet implemented:
- circuit QED coupling
- control pulse simulation
- open quantum noise models
- benchmarking protocols
- quantum error correction

The HTML interface reflects this implementation status and does not advertise features that do not exist yet.

---

# Repository Structure

```
superconducting-qubit-lab/
  core/
    lc_resonator.py
    josephson.py
    transmon.py

  experiments/
    lc_resonance_validation.py
    transmon_spectrum.py

  tests/
    test_phase1.py
    test_transmon.py

  index.html
  README.md
  requirements.txt
```

core/
    Physics models and Hamiltonians

experiments/
    Executable validation experiments

tests/
    Automated regression tests

index.html
    Documentation and visual overview

---

# Physics Implemented

## LC Resonator

The LC oscillator is implemented using the standard resonance relation:

```
f = 1 / (2*pi*sqrt(L*C))
```

This provides the electromagnetic baseline required for superconducting circuit models.

---

## Josephson Junction

The Josephson energy is defined as:

```
E_J = Phi0 * I_c / (2*pi)
```

where

- Phi0 is the magnetic flux quantum
- I_c is the critical current

This energy term introduces the nonlinearity required for qubit formation.

---

## Transmon Qubit

The transmon Hamiltonian used is:

```
H = 4*E_C*(n - n_g)^2 - E_J*cos(phi)
```

Key properties derived numerically include:
- transition frequency E01
- anharmonicity alpha
- charge dispersion

The implementation targets the typical transmon regime:

```
E_J / E_C >> 1
```

which suppresses charge-noise sensitivity.

---

# Validation

Two executable validation experiments are included.

LC resonance validation

```
python -m experiments.lc_resonance_validation
```

Expected output

```
Validation PASS
RMS error: 0.0%
```

Transmon spectrum baseline

```
python -m experiments.transmon_spectrum
```

Example result

```
EJ/EC = 50
E01 ~= 4.735 GHz
alpha ~= -287 MHz
charge dispersion ~= 9.9 kHz
```

These values are consistent with typical transmon parameters reported in superconducting qubit literature.

---

# Running Tests

```
python -m unittest discover -s tests -v
```

Expected

```
Ran 8 tests

OK
```

---

# Quick Demo (copy/paste)

```
python3 -m experiments.lc_resonance_validation
python3 -m experiments.transmon_spectrum
python3 -m analysis.transmon_parameter_sweep --ej-ec-start 20 --ej-ec-stop 80 --num 10 --out data/transmon_sweep.csv
python3 -m analysis.transmon_plots --csv data/transmon_sweep.csv --out plots
python3 -m experiments.cqed_spectrum
python3 -m experiments.rabi_simulation
python3 -m experiments.vacuum_rabi
python3 -m experiments.dispersive_shift
python3 -m experiments.t1_decay
python3 -m experiments.t2_ramsey_decay
python3 -m experiments.rabi
python3 -m experiments.ramsey
python3 -m experiments.echo
```

Both scripts are self-contained and print PASS/summary lines for sanity checks.

---

# Installation

Clone repository

```
git clone <repo>
cd superconducting-qubit-lab
```

Install dependencies

```
pip install -r requirements.txt
```

Requirements are intentionally minimal:
- numpy
- scipy

---

# Design Philosophy

The project prioritizes:
- physically correct models
- reproducible experiments
- explicit separation between implemented and planned features
- minimal dependencies
- transparent validation

The aim is to create a clear bridge between superconducting qubit theory and executable simulations.

---

# References

- Koch et al. (2007): Charge-insensitive qubit design derived from the Cooper pair box
- Devoret & Schoelkopf (2013): Superconducting circuits for quantum information
- Blais et al. (2021): Circuit Quantum Electrodynamics

---

# License

MIT License

---

# Roadmap Tecnico

Esto es critico: el roadmap debe seguir la estructura natural de la fisica de circuitos superconductores.

No puedes saltar directo a QEC.

La secuencia correcta es:

Circuit Physics
-> Qubit Hamiltonian
-> Coupled Systems (cQED)
-> Control
-> Noise
-> Benchmarking
-> Error Correction

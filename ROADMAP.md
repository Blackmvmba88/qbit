# Development Roadmap

The roadmap follows the natural hierarchy of superconducting quantum systems.

---

# Phase 1 - Circuit Foundations (Completed)

Implemented

- LC resonator physics
- Josephson junction energy
- Transmon Hamiltonian baseline
- Spectrum calculation
- Charge dispersion analysis
- Automated tests

Validation scripts

- experiments/lc_resonance_validation.py
- experiments/transmon_spectrum.py

---

# Phase 2 - Transmon Simulator

Goal

Extend the transmon module into a full parameter exploration simulator.

Planned features

- parameter sweeps (EJ/EC ratio)
- frequency vs capacitance/current plots
- anharmonicity scaling
- automatic spectrum visualization
- numerical vs analytical comparison

New modules

```
analysis/
  transmon_parameter_sweep.py
  transmon_plots.py
```

---

# Phase 3 - Circuit QED

Goal

Couple the transmon to a microwave resonator.

Hamiltonian

```
H = w_r a^\dagger a + w_q b^\dagger b + g (a^\dagger b + a b^\dagger)
```

Features

- Jaynes-Cummings model
- vacuum Rabi splitting
- dispersive regime simulation
- readout frequency shifts

New modules

```
core/cqed.py
experiments/cqed_spectrum.py
```

---

# Phase 4 - Quantum Control

Goal

Simulate qubit manipulation using microwave pulses.

Features

- Rabi oscillations
- pi pulses
- DRAG pulses
- Bloch sphere dynamics

Dependencies

- scipy.integrate

New modules

```
control/pulses.py
control/time_evolution.py
experiments/rabi_simulation.py
```

---

# Phase 5 - Noise and Decoherence

Goal

Introduce realistic noise channels.

Models

- T1 relaxation
- T2 dephasing
- thermal noise

Methods

- Lindblad master equation

New modules

```
noise/lindblad.py
noise/decoherence_models.py
```

---

# Phase 6 - Benchmarking

Goal

Evaluate gate performance.

Protocols

- Randomized benchmarking
- gate fidelity estimation
- error scaling

---

# Phase 7 - Quantum Error Correction

Goal

Simulate logical qubits and stabilizer measurements.

Possible implementations

- 3-qubit bit flip code
- surface code toy model

This phase will depend on previous modules.

---

# Long-Term Vision

Transform the project into a complete superconducting qubit simulation lab with:

- interactive browser interface
- live parameter exploration
- visualized Hamiltonians
- educational demonstrations que tenemos de aqui

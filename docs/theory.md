# Theory Notes

This repository models superconducting transmon qubits from circuit quantization through control, noise, readout, and benchmarking. Each section states the governing Hamiltonian, the regime of validity, and the code modules that implement it.

---

## 1. Circuit Quantization (LC)
Classical energy:  
H = Q^2 / (2C) + Phi^2 / (2L)  
Canonical commutator: [Phi, Q] = i hbar.  
Mode frequency: omega = 1 / sqrt(LC).  
Code: `core/lc_resonator.py`.

---

## 2. Josephson Junction
Current-phase: I = Ic sin(phi).  
Josephson energy: EJ = Phi0 Ic / (2 pi).  
Adds the nonlinearity needed for qubits.  
Code: `core/josephson.py`.

---

## 3. Cooper Pair Box → Transmon
Hamiltonian: H = 4 EC (n - ng)^2 - EJ cos(phi).  
Transmon regime: EJ / EC >> 1. Consequences:  
- Transition E01 set by EJ, EC.  
- Anharmonicity breaks equal spacing.  
- Charge dispersion suppressed exponentially.  
Code: `core/transmon.py`; spectra and properties derived numerically.

---

## 4. Circuit QED
Jaynes–Cummings:  
H = hbar omega_r a† a + (hbar omega_q / 2) sigma_z + g (a sigma+ + a† sigma-).  
Dispersive limit: delta = omega_q - omega_r, |delta| >> g.  
Dispersive shift: chi ≈ g^2 / delta.  
Code: `core/cqed.py`; demos in `experiments/vacuum_rabi.py`, `experiments/dispersive_shift.py`.

---

## 5. Quantum Control (RWA)
In the rotating frame with drive frequency omega_d and detuning Delta = omega_q - omega_d:  
H = (Delta / 2) sigma_z + (Omega(t) / 2)(cos phi sigma_x + sin phi sigma_y).  
Envelopes supply Omega(t); phases set rotation axis.  
Code: `control/drive_hamiltonian.py`, `control/propagator.py`; demos `experiments/rabi.py`, `ramsey.py`, `echo.py`.

---

## 6. Open Quantum Systems
Lindblad equation: rho_dot = -i[H, rho] + sum_i (L_i rho L_i† - 0.5 {L_i† L_i, rho}).  
Operators:  
- Relaxation: L_T1 = sqrt(1/T1) sigma_-  
- Pure dephasing: L_Tphi = sqrt(1/(2 Tphi)) sigma_z, with 1/T2 = 1/(2T1) + 1/Tphi.  
Code: `core/open_systems.py`; demos `experiments/t1_decay.py`, `t2_ramsey_decay.py`.

---

## 7. Dispersive Readout
Effective Hamiltonian: H = (omega_r + chi sigma_z) a† a + (omega_q/2) sigma_z.  
Driven cavity steady state: a = -i eps / (i(omega_r - omega_d) + kappa/2).  
State dependence: omega_r -> omega_r ± chi. Distinguishability D = |alpha_e - alpha_g|.  
Code: `core/readout.py`; demo `experiments/dispersive_readout.py` (amp/phase plots).

---

## 8. Randomized Benchmarking (1Q)
Survival model: P(m) = A p^m + B.  
Error per Clifford: r = (1 - p)/2.  
Code: `experiments/randomized_benchmarking.py`; Clifford set in `core/clifford_1q.py`.

---

## 9. Modeling Assumptions and Limits
- RWA and rotating frames; drive frequencies near qubit frequency.  
- Transmon treated as 2-level in control/benchmarking; spectra computed from truncated charge basis.  
- Dispersive readout assumes |delta| >> g and single-mode cavity, semiclassical drive.  
- Lindblad noise is Markovian; Euler integration with adaptive substeps; trace is renormalized.  
- Hilbert space truncation (n_cut) in transmon and cavity models; choose cutoffs to avoid leakage artifacts.  
- Randomized benchmarking uses depolarizing channel as a simple noise stand-in; not a full physical noise map.  
- Units: Hz (not rad/s) across cQED/control/readout modules; check comments in code when mixing rates.


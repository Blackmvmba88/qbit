# Circuit QED Notes

These notes summarize the cQED pieces implemented in the repo and the approximations behind them.

---

## 1. Jaynes–Cummings Model

H = hbar omega_r a† a + (hbar omega_q / 2) sigma_z + g (a sigma+ + a† sigma-)  
- omega_r: resonator frequency  
- omega_q: qubit transition  
- g: vacuum coupling

Implemented in `core/cqed.py` with spectrum/vacuum Rabi demos.

---

## 2. Vacuum Rabi Splitting

On resonance (omega_r ≈ omega_q): splitting ≈ 2g.  
Computed via eigenvalues of Jaynes–Cummings. Demo: `experiments/vacuum_rabi.py`.

---

## 3. Dispersive Regime

Detuning: delta = omega_q - omega_r, with |delta| >> g.  
Effective dispersive Hamiltonian (Schrieffer–Wolff to second order):  
H_eff ≈ (omega_r + chi sigma_z) a† a + (omega_q/2) sigma_z,  chi ≈ g^2 / delta.  
Consequences: state-dependent resonator pull, qubit-state-dependent phase shift on cavity probe.

Implemented helpers in `core/cqed.py` (chi) and `core/readout.py` (response).

---

## 4. Readout Response

Driven damped cavity equation (steady state):  
a = -i eps / (i(omega_r - omega_d) + kappa/2).  
With qubit: omega_r -> omega_r ± chi.  
Amplitude/phase separation between |0> and |1> is basis of dispersive readout.  
Demo plots: `experiments/dispersive_readout.py` -> `plots/readout_amp.png`, `plots/readout_phase.png`.

---

## 5. Validity and Limits

- Dispersive approximation: |delta| >> g, photon number << n_crit ~ delta^2 / (4 g^2).  
- Single cavity mode, semiclassical drive (no measurement backaction modeled).  
- Two-level qubit approximation; higher transmon levels ignored in cQED interactions.  
- Kappa treated as phenomenological linewidth; no Purcell filtering modeled.  
- No gain chain/added noise; outputs are ideal field amplitudes.

---

## 6. Next Extensions (out of current scope)

- Multilevel transmon in dispersive frame (anharmonic corrections to chi).  
- Time-domain readout including ring-up/ring-down dynamics.  
- Inclusion of Purcell decay and measurement-induced dephasing.  
- Two-qubit cross-Kerr (ZZ) and resonator-mediated entangling gates.


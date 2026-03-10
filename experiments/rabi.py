"""Rabi oscillation using rotating-frame drive Hamiltonian."""

import numpy as np

from control.pulses import square_pulse
from control.drive_hamiltonian import rotating_frame_h0, build_piecewise_hamiltonians
from control.propagator import propagate_piecewise, apply_unitary, excited_population


def main() -> None:
    omega_q = 5e9        # Hz
    omega_d = 5e9        # Hz (on resonance)
    delta = omega_q - omega_d
    duration = 200e-9
    sample_rate = 2e9
    rabi_rate = 50e6     # Hz

    t, _ = square_pulse(amplitude=rabi_rate, duration=duration, sample_rate=sample_rate)
    envelopes = [rabi_rate] * len(t)
    phases = [0.0] * len(t)

    H0 = rotating_frame_h0(omega_q=0.0)  # in rotating frame about drive -> only delta term
    Hs = build_piecewise_hamiltonians(H0, envelopes, phases, delta=delta)
    dt = 1.0 / sample_rate

    # start in |0>
    state0 = np.array([1.0, 0.0], dtype=complex)
    U = propagate_piecewise(Hs, dt)
    state_f = apply_unitary(U, state0)
    p_exc = excited_population(state_f)

    print("Rabi demo (resonant)")
    print(f"Duration {duration*1e9:.1f} ns, Omega={rabi_rate*1e-6:.1f} MHz")
    print(f"P_exc ≈ {p_exc:.3f} (expected ~sin^2(Omega*t/2))")


if __name__ == "__main__":
    main()


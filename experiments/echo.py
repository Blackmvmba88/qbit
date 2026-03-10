"""Hahn echo simulation: pi/2 - tau - pi - tau - measure."""

import numpy as np

from control.pulses import square_pulse
from control.drive_hamiltonian import rotating_frame_h0, build_piecewise_hamiltonians
from control.propagator import propagate_piecewise, apply_unitary, excited_population


def main() -> None:
    omega_q = 5e9
    omega_d = 5.0e9
    delta = omega_q - omega_d  # assume on resonance for pulses
    rabi_rate = 50e6
    sample_rate = 2e9
    tau = 300e-9
    dephasing_delta = 2e6  # Hz static detuning noise during free evolution

    # pulse lengths
    t_pi = (np.pi) / (2 * np.pi * rabi_rate)
    t_pi_over_2 = 0.5 * t_pi
    n_pi = max(1, int(np.ceil(t_pi * sample_rate)))
    n_pi_over_2 = max(1, int(np.ceil(t_pi_over_2 * sample_rate)))
    dur_pi = n_pi / sample_rate
    dur_pi_over_2 = n_pi_over_2 / sample_rate

    # pulses
    env_pi_over_2 = [rabi_rate] * n_pi_over_2
    env_pi = [rabi_rate] * n_pi
    env_delay = [0.0] * int(tau * sample_rate)

    envelopes = env_pi_over_2 + env_delay + env_pi + env_delay + env_pi_over_2
    # phases: set pi pulse phase 0; could alternate to cancel errors; keep simple.
    phases = [0.0] * len(envelopes)

    # During free evolution include static detuning (simulated via delta shift)
    H0 = rotating_frame_h0(omega_q=0.0)
    drift = 0.5 * (delta + dephasing_delta) * np.array([[1, 0], [0, -1]], dtype=complex)

    Hs = []
    for amp, ph in zip(envelopes, phases):
        h_drive = 0.5 * amp * (np.array([[0, np.exp(-1j * ph)], [np.exp(1j * ph), 0]], dtype=complex))
        Hs.append(H0 + drift + h_drive)

    dt = 1.0 / sample_rate
    state0 = np.array([1.0, 0.0], dtype=complex)
    U = propagate_piecewise(Hs, dt)
    state_f = apply_unitary(U, state0)
    p_exc = excited_population(state_f)

    print("Hahn echo demo")
    print(f"tau = {tau*1e9:.1f} ns, static detuning {dephasing_delta*1e-6:.2f} MHz")
    print(f"P_exc after echo ≈ {p_exc:.3f} (should recover near 0 or 1 depending on phase)")


if __name__ == "__main__":
    main()


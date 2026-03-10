"""Ramsey fringe simulation using two pi/2 pulses and free evolution."""

import numpy as np

from control.pulses import square_pulse
from control.drive_hamiltonian import rotating_frame_h0, build_piecewise_hamiltonians
from control.propagator import propagate_piecewise, apply_unitary, excited_population


def main() -> None:
    omega_q = 5e9
    omega_d = 5.001e9  # slight detuning 1 MHz
    delta = omega_q - omega_d
    rabi_rate = 50e6
    sample_rate = 2e9

    # pi/2 duration
    t_pi_over_2 = (np.pi / 2) / (2 * np.pi * rabi_rate)
    n_pi_over_2 = max(1, int(np.ceil(t_pi_over_2 * sample_rate)))
    duration_pi_over_2 = n_pi_over_2 / sample_rate

    t_pulse, _ = square_pulse(amplitude=rabi_rate, duration=duration_pi_over_2, sample_rate=sample_rate)

    # Sequence: pi/2, free delay, pi/2
    delay = 200e-9
    n_delay = int(delay * sample_rate)

    envelopes = [rabi_rate] * len(t_pulse) + [0.0] * n_delay + [rabi_rate] * len(t_pulse)
    phases = [0.0] * len(envelopes)

    H0 = rotating_frame_h0(omega_q=0.0)
    Hs = build_piecewise_hamiltonians(H0, envelopes, phases, delta=delta)
    dt = 1.0 / sample_rate

    state0 = np.array([1.0, 0.0], dtype=complex)
    U = propagate_piecewise(Hs, dt)
    state_f = apply_unitary(U, state0)
    p_exc = excited_population(state_f)

    beat_freq_mhz = abs(delta) * 1e-6
    print("Ramsey demo")
    print(f"Detuning: {delta*1e-6:.3f} MHz -> fringe freq ≈ {beat_freq_mhz:.3f} MHz")
    print(f"Delay: {delay*1e9:.1f} ns, P_exc ≈ {p_exc:.3f}")


if __name__ == "__main__":
    main()


"""Simulate Rabi oscillations for a resonant square pulse."""

import numpy as np

from control.time_evolution import rabi_population
from control.pulses import square_pulse


def main() -> None:
    # Define a 50 ns square pulse with Rabi frequency 2*pi*50 MHz
    duration = 50e-9
    sample_rate = 1e9  # 1 GS/s sampling grid
    omega_rabi = 2 * np.pi * 50e6  # rad/s

    t, _ = square_pulse(amplitude=1.0, duration=duration, sample_rate=sample_rate)
    p_exc = rabi_population(omega_rabi=omega_rabi, times=t, detuning=0.0)

    print("Rabi oscillation demo (resonant)")
    print(f"Pulse duration: {duration*1e9:.1f} ns")
    print(f"Rabi freq: {omega_rabi/(2*np.pi)*1e-6:.1f} MHz")
    print(f"Excited-state P_e max: {p_exc.max():.3f}")
    print(f"P_e at end of pulse: {p_exc[-1]:.3f}")


if __name__ == "__main__":
    main()


"""Vacuum Rabi splitting as a function of detuning."""

import numpy as np

from core.cqed import vacuum_rabi_splitting


def main() -> None:
    omega_r = 7.0  # GHz
    g = 0.1        # GHz
    detunings = np.linspace(-1.0, 1.0, 5)

    print("Vacuum Rabi splitting vs detuning")
    for delta in detunings:
        omega_q = omega_r + delta
        split = vacuum_rabi_splitting(omega_r, omega_q, g)
        print(f"Delta={delta:+.2f} GHz -> splitting {split:.4f} GHz (on-resonance ~ {2*g:.4f})")


if __name__ == "__main__":
    main()


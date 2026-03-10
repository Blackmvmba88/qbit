"""Simulate Ramsey fringes with T2 dephasing."""

import numpy as np

from core.open_systems import (
    SIGMA_X,
    SIGMA_Z,
    solve_lindblad_two_level,
    t1_t2_operators,
    excited_population,
)


def main() -> None:
    T1 = 50e-6
    T2 = 30e-6
    detuning = 2 * np.pi * 1e6  # 1 MHz detuning between drive and qubit
    # Work in rotating frame; only detuning term drives fringes
    H = 0.5 * detuning * SIGMA_Z

    times = np.linspace(0, 60e-6, 300)
    # Start in |+x> after a pi/2 pulse around Y; density matrix:
    psi_plus = (1 / np.sqrt(2)) * np.array([1, 1], dtype=complex)
    rho0 = np.outer(psi_plus, psi_plus.conj())

    Ls = t1_t2_operators(T1=T1, T2=T2)
    rhos = solve_lindblad_two_level(H, Ls, rho0, times)
    pops = [excited_population(r) for r in rhos]

    print("Ramsey with T2 decay")
    for t, p in zip(times[::60], pops[::60]):
        print(f"t = {t*1e6:5.1f} us -> Pe = {p:.4f}")
    print(f"Visibility decays toward 0.5; final Pe = {pops[-1]:.4f}")


if __name__ == "__main__":
    main()

"""Simulate T1 relaxation of a qubit."""

import numpy as np

from core.open_systems import (
    SIGMA_Z,
    solve_lindblad_two_level,
    t1_t2_operators,
    excited_population,
)


def main() -> None:
    T1 = 30e-6  # 30 microseconds
    T2 = None
    H = np.zeros((2, 2), dtype=complex)  # work in rotating frame; decay only

    times = np.linspace(0, 60e-6, 200)
    rho0 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)  # excited state
    Ls = t1_t2_operators(T1=T1, T2=T2)
    rhos = solve_lindblad_two_level(H, Ls, rho0, times)
    pops = [excited_population(r) for r in rhos]

    print("T1 decay demo")
    for t, p in zip(times[::40], pops[::40]):
        print(f"t = {t*1e6:5.1f} us -> Pe = {p:.4f}")
    print(f"Final Pe ≈ {pops[-1]:.4f} (should approach 0)")


if __name__ == "__main__":
    main()

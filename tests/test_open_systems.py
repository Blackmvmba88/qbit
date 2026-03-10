import unittest
import numpy as np

from core.open_systems import (
    SIGMA_Z,
    SIGMA_X,
    SIGMA_MINUS,
    solve_lindblad_two_level,
    t1_t2_operators,
    excited_population,
)


class TestOpenSystems(unittest.TestCase):
    def test_t1_relaxation_monotone(self):
        T1 = 20e-6
        H = 0.0 * SIGMA_Z
        times = np.linspace(0, 20e-6, 100)
        rho0 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
        Ls = t1_t2_operators(T1=T1, T2=None)
        rhos = solve_lindblad_two_level(H, Ls, rho0, times)
        pops = np.array([excited_population(r) for r in rhos])
        self.assertTrue(np.all(np.diff(pops) <= 1e-6))  # non-increasing (allow small num noise)
        self.assertAlmostEqual(pops[-1], np.exp(-1), delta=0.05)

    def test_t2_dephasing_reduces_visibility(self):
        T1 = 1e9  # effectively no relaxation
        T2 = 5e-6
        detuning = 2 * np.pi * 1e6
        H = 0.5 * detuning * SIGMA_X
        times = np.linspace(0, 20e-6, 120)
        psi_plus = (1 / np.sqrt(2)) * np.array([1, 1], dtype=complex)
        rho0 = np.outer(psi_plus, psi_plus.conj())
        Ls = t1_t2_operators(T1=T1, T2=T2)
        rhos = solve_lindblad_two_level(H, Ls, rho0, times)
        pops = np.array([excited_population(r) for r in rhos])
        self.assertLess(np.ptp(pops), 0.5)  # visibility decays below ideal 1.0


if __name__ == "__main__":
    unittest.main()

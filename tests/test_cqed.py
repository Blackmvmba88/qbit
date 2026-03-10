import unittest

import numpy as np

from core.cqed import (
    jaynes_cummings_spectrum,
    vacuum_rabi_splitting,
    dispersive_shift,
    resonator_frequencies_with_qubit,
)
from core.readout import resonator_response, state_distinguishability


class TestCQED(unittest.TestCase):
    def test_vacuum_rabi_on_resonance(self):
        omega = 7.0
        g = 0.05
        split = vacuum_rabi_splitting(omega, omega, g)
        # On resonance the splitting should be close to 2g.
        self.assertAlmostEqual(split, 2 * g, delta=0.002)

    def test_spectrum_monotonic(self):
        eigs = jaynes_cummings_spectrum(omega_r=6.0, omega_q=7.0, g=0.1, n_cut=3, levels=8)
        self.assertTrue(np.all(np.diff(eigs) >= -1e-12))

    def test_dispersive_shift_sign(self):
        chi = dispersive_shift(g=0.05, delta=0.5)
        omega_g, omega_e = resonator_frequencies_with_qubit(omega_r=6.0, chi=chi)
        self.assertGreater(omega_e, omega_g)
        self.assertAlmostEqual(omega_e - omega_g, 2 * chi, places=6)

    def test_readout_response_separates_states(self):
        omega_r = 6.5e9
        chi = 7.7e6
        omega_d = omega_r
        kappa = 1e6
        eps = 1e6
        a0 = resonator_response(omega_r - chi, omega_d, kappa, eps)
        a1 = resonator_response(omega_r + chi, omega_d, kappa, eps)
        d = state_distinguishability(a0, a1)
        self.assertGreater(d, 0.0)


if __name__ == "__main__":
    unittest.main()

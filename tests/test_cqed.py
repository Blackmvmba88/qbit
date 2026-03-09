import unittest

import numpy as np

from core.cqed import jaynes_cummings_spectrum, vacuum_rabi_splitting


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


if __name__ == "__main__":
    unittest.main()


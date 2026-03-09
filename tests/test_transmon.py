import unittest

import math

import numpy as np

from core.transmon import PLANCK, transmon_properties, transmon_spectrum


class TestTransmonSpectrum(unittest.TestCase):
    def test_baseline_properties(self):
        # Match the demo parameters: EJ/EC = 50, EC/h = 0.25 GHz
        EJ_over_EC = 50.0
        ec_over_h_ghz = 0.25
        EC = PLANCK * ec_over_h_ghz * 1e9
        EJ = EJ_over_EC * EC

        props = transmon_properties(EJ, EC, n_cut=25)
        self.assertAlmostEqual(props["E01_GHz"], 4.735, delta=0.05)
        self.assertAlmostEqual(props["alpha_GHz"] * 1e3, -287.0, delta=10.0)
        self.assertLess(props["charge_dispersion_kHz"], 15.0)

    def test_invalid_parameters_raise(self):
        EC = PLANCK * 0.25e9
        with self.assertRaises(ValueError):
            transmon_spectrum(-1.0, EC)
        with self.assertRaises(ValueError):
            transmon_spectrum(1.0, -EC)
        with self.assertRaises(ValueError):
            transmon_spectrum(1.0, EC, n_cut=0)
        with self.assertRaises(ValueError):
            transmon_spectrum(1.0, EC, levels=0)

    def test_monotonic_spectrum(self):
        EC = PLANCK * 0.25e9
        EJ = 50 * EC
        eigs = transmon_spectrum(EJ, EC, n_cut=20, levels=5)
        self.assertTrue(np.all(np.diff(eigs) >= -1e-12))



if __name__ == "__main__":
    unittest.main()

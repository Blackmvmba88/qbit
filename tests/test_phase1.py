import math
import unittest

from core.josephson import josephson_energy, PHI0
from core.lc_resonator import resonance_frequency


class TestPhase1Basics(unittest.TestCase):
    def test_lc_resonance_matches_formula(self):
        L = 8e-9
        C = 120e-15
        f = resonance_frequency(L, C)
        expected = 1.0 / (2.0 * math.pi * math.sqrt(L * C))
        self.assertTrue(math.isclose(f, expected, rel_tol=1e-12))

    def test_josephson_energy_linear_in_current(self):
        ic1 = 20e-9
        ic2 = 40e-9
        ratio = josephson_energy(ic2) / josephson_energy(ic1)
        self.assertTrue(math.isclose(ratio, ic2 / ic1, rel_tol=1e-12))

    def test_josephson_energy_known_value(self):
        ic = 25e-9
        ej = josephson_energy(ic)
        expected = PHI0 * ic / (2.0 * math.pi)
        self.assertTrue(math.isclose(ej, expected, rel_tol=1e-12))


if __name__ == "__main__":
    unittest.main()

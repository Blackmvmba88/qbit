import unittest
import numpy as np

from control.pulses import square_pulse, gaussian_pulse
from control.time_evolution import rabi_population


class TestPulses(unittest.TestCase):
    def test_square_pulse_shape(self):
        t, a = square_pulse(amplitude=0.5, duration=10e-9, sample_rate=1e9)
        self.assertTrue((a == 0.5).all())
        self.assertGreater(len(t), 1)
        self.assertAlmostEqual(t[-1], t[0] + (len(t) - 1) * (t[1] - t[0]))

    def test_gaussian_peak(self):
        t, a = gaussian_pulse(amplitude=1.0, duration=20e-9, sigma=5e-9, sample_rate=1e9)
        self.assertAlmostEqual(a.max(), 1.0, places=3)


class TestRabi(unittest.TestCase):
    def test_resonant_pi_pulse(self):
        omega_rabi = 2 * np.pi * 50e6  # rad/s
        t = np.array([np.pi / omega_rabi])  # one pi pulse duration
        p = rabi_population(omega_rabi, t, detuning=0.0)
        self.assertAlmostEqual(p[-1], 1.0, places=3)

    def test_detuned_has_lower_contrast(self):
        omega_rabi = 2 * np.pi * 50e6
        times = np.linspace(0, 100e-9, 50)
        p_res = rabi_population(omega_rabi, times, detuning=0.0)
        p_det = rabi_population(omega_rabi, times, detuning=2 * omega_rabi)
        self.assertLess(p_det.max(), p_res.max())


if __name__ == "__main__":
    unittest.main()


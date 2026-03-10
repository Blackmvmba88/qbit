import numpy as np
import unittest

from experiments.randomized_benchmarking import estimate_decay, fit_exponential


class TestRB(unittest.TestCase):
    def test_survival_decreases_with_noise(self):
        lengths = np.array([2, 4, 8, 16])
        trials = 10
        rng = np.random.default_rng(0)
        means_clean, _ = estimate_decay(lengths, trials, p_depol=0.0, rng=rng)
        rng = np.random.default_rng(0)
        means_noisy, _ = estimate_decay(lengths, trials, p_depol=0.01, rng=rng)
        self.assertLess(means_noisy[-1], means_clean[-1])

    def test_fit_returns_small_error_for_clean(self):
        lengths = np.array([2, 4, 8, 16, 32])
        rng = np.random.default_rng(1)
        means, _ = estimate_decay(lengths, trials=20, p_depol=0.0, rng=rng)
        r = fit_exponential(lengths, means)
        self.assertLess(r, 1e-3)


if __name__ == "__main__":
    unittest.main()


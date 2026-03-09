"""Simple pulse envelopes."""

import numpy as np


def square_pulse(amplitude: float, duration: float, sample_rate: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate a square pulse.
    Returns (t, amp) where t is seconds and amp is amplitude.
    """
    if duration <= 0 or sample_rate <= 0:
        raise ValueError("duration and sample_rate must be positive.")
    n = max(2, int(np.ceil(duration * sample_rate)))
    t = np.linspace(0.0, duration, n, endpoint=False)
    a = np.full_like(t, amplitude, dtype=float)
    return t, a


def gaussian_pulse(amplitude: float, duration: float, sigma: float, sample_rate: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate a Gaussian pulse truncated at duration.
    Centered at duration/2 with std = sigma.
    """
    if duration <= 0 or sigma <= 0 or sample_rate <= 0:
        raise ValueError("duration, sigma, sample_rate must be positive.")
    n = max(2, int(np.ceil(duration * sample_rate)))
    t = np.linspace(0.0, duration, n, endpoint=False)
    center = duration / 2.0
    a = amplitude * np.exp(-0.5 * ((t - center) / sigma) ** 2)
    return t, a


__all__ = ["square_pulse", "gaussian_pulse"]


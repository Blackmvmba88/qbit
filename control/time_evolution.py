"""Simple driven two-level system evolution (Rabi model)."""

import numpy as np


def rabi_population(omega_rabi: float, times: np.ndarray, detuning: float = 0.0) -> np.ndarray:
    """
    Compute excited-state population vs time for a two-level system
    driven with Rabi frequency omega_rabi (rad/s) and detuning delta (rad/s).

    Using P_e(t) = (Omega_R^2 / Omega_eff^2) * sin^2(Omega_eff * t / 2)
    where Omega_eff = sqrt(Omega_R^2 + delta^2).
    """
    if omega_rabi <= 0:
        raise ValueError("omega_rabi must be positive.")
    times = np.asarray(times, dtype=float)
    if times.ndim != 1:
        raise ValueError("times must be 1D.")

    omega_eff = np.sqrt(omega_rabi ** 2 + detuning ** 2)
    prefac = (omega_rabi / omega_eff) ** 2
    return prefac * np.sin(0.5 * omega_eff * times) ** 2


__all__ = ["rabi_population"]


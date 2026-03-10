"""Dispersive readout utilities for cQED."""

from __future__ import annotations

import numpy as np


def dispersive_shift(g: float, delta: float) -> float:
    """chi = g^2 / delta (Hz)."""
    if delta == 0:
        raise ValueError("delta must be nonzero for dispersive shift.")
    return g * g / delta


def resonator_response(omega_r: float, omega_d: float, kappa: float, drive_eps: float) -> complex:
    """
    Steady-state cavity field for driven damped mode:
    a = -i * eps / (i(omega_r - omega_d) + kappa/2)
    """
    return -1j * drive_eps / (1j * (omega_r - omega_d) + 0.5 * kappa)


def readout_response(omega_r: float, chi: float, omega_d: float, kappa: float, drive_eps: float, qubit_state: int) -> complex:
    """
    Resonator response conditioned on qubit state.
    qubit_state: 0 -> omega_r - chi; 1 -> omega_r + chi
    """
    omega_eff = omega_r + (chi if qubit_state == 1 else -chi)
    return resonator_response(omega_eff, omega_d, kappa, drive_eps)


def state_distinguishability(alpha_g: complex, alpha_e: complex) -> float:
    """D = |alpha_e - alpha_g|."""
    return abs(alpha_e - alpha_g)


__all__ = [
    "dispersive_shift",
    "resonator_response",
    "readout_response",
    "state_distinguishability",
]


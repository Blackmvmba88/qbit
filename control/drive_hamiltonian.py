"""Drive Hamiltonians in rotating frame (RWA)."""

from __future__ import annotations

import numpy as np

# Pauli matrices for general use (2-level); users can swap with larger dims if needed.
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def rotating_frame_h0(omega_q: float) -> np.ndarray:
    """Static qubit term (Hz) in rotating frame: (omega_q/2) * sigma_z."""
    return 0.5 * omega_q * SIGMA_Z


def rwa_drive_term(omega_envelope: float, phase: float = 0.0) -> np.ndarray:
    """
    Drive term under RWA: (Omega/2)(cos phi * sigma_x + sin phi * sigma_y).
    omega_envelope is instantaneous Rabi rate (Hz), phase in radians.
    """
    return 0.5 * omega_envelope * (np.cos(phase) * SIGMA_X + np.sin(phase) * SIGMA_Y)


def build_piecewise_hamiltonians(
    h0: np.ndarray,
    envelopes: list[float],
    phases: list[float],
    delta: float,
) -> list[np.ndarray]:
    """
    Create a list of constant Hamiltonians for each time step (Hz).
    H = (delta/2) sigma_z + rwa_drive_term
    """
    hams = []
    drift = 0.5 * delta * SIGMA_Z + h0
    for amp, ph in zip(envelopes, phases):
        hams.append(drift + rwa_drive_term(amp, ph))
    return hams


__all__ = ["SIGMA_X", "SIGMA_Y", "SIGMA_Z", "rotating_frame_h0", "rwa_drive_term", "build_piecewise_hamiltonians"]


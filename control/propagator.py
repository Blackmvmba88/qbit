"""Time-dependent propagator using piecewise-constant Hamiltonians."""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm


def propagate_piecewise(H_list: list[np.ndarray], dt: float, U0: np.ndarray | None = None) -> np.ndarray:
    """
    Compute unitary evolution for a list of constant Hamiltonians.
    H_list: list of Hamiltonians (Hz); dt in seconds; returns final U.
    """
    if not H_list:
        raise ValueError("H_list must not be empty.")
    dim = H_list[0].shape[0]
    U = np.eye(dim, dtype=complex) if U0 is None else np.array(U0, dtype=complex)
    for H in H_list:
        if H.shape != (dim, dim):
            raise ValueError("All Hamiltonians must have same shape.")
        U = expm(-1j * 2 * np.pi * H * dt) @ U
    return U


def apply_unitary(U: np.ndarray, state: np.ndarray) -> np.ndarray:
    """Apply unitary to state vector."""
    return U @ state


def excited_population(state: np.ndarray) -> float:
    """Population of |1> for a two-level state vector."""
    return float(np.abs(state[1]) ** 2)


__all__ = ["propagate_piecewise", "apply_unitary", "excited_population"]


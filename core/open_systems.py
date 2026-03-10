"""Lindblad evolution for a two-level system with T1/T2."""

from __future__ import annotations

import numpy as np
from numpy import linalg as LA

# Pauli / ladder operators
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
SIGMA_MINUS = np.array([[0, 1], [0, 0]], dtype=complex)  # |g><e|
SIGMA_PLUS = SIGMA_MINUS.conj().T                          # |e><g|


def lindblad_rhs(rho: np.ndarray, H: np.ndarray, Ls: list[np.ndarray]) -> np.ndarray:
    """Compute drho/dt = -i[H, rho] + sum_i (L rho L† - 0.5 {L† L, rho})."""
    comm = H @ rho - rho @ H
    diss = np.zeros_like(rho, dtype=complex)
    for L in Ls:
        Ld = L.conj().T
        diss += L @ rho @ Ld - 0.5 * (Ld @ L @ rho + rho @ Ld @ L)
    return -1j * comm + diss


def _max_rate(H: np.ndarray, Ls: list[np.ndarray]) -> float:
    rates = []
    if H.size:
        eig = LA.eigvals(H)
        rates.append(float(np.max(np.abs(eig))).real)
    for L in Ls:
        ld_l = L.conj().T @ L
        rates.append(float(np.real(np.trace(ld_l))))
    return max(rates) if rates else 0.0


def solve_lindblad_two_level(
    H: np.ndarray,
    Ls: list[np.ndarray],
    rho0: np.ndarray,
    times: np.ndarray,
) -> np.ndarray:
    """
    Integrate Lindblad equation using Euler with adaptive substeps for stability.
    Returns array with shape (len(times), 2, 2).
    """
    times = np.asarray(times, dtype=float)
    if times.ndim != 1:
        raise ValueError("times must be 1D array.")
    rho = np.array(rho0, dtype=complex)
    out = np.zeros((len(times), 2, 2), dtype=complex)
    out[0] = rho

    max_rate = _max_rate(H, Ls)
    # choose conservative dt_max relative to fastest rate
    dt_max = np.inf if max_rate == 0 else 0.005 / max_rate

    for k in range(1, len(times)):
        dt = times[k] - times[k - 1]
        n_sub = 1 if dt_max == np.inf else max(1, int(np.ceil(dt / dt_max)))
        sub_dt = dt / n_sub
        for _ in range(n_sub):
            drho = lindblad_rhs(rho, H, Ls)
            rho = rho + sub_dt * drho
            rho = 0.5 * (rho + rho.conj().T)  # enforce hermiticity
            rho = rho / np.trace(rho)         # keep trace ~ 1
        out[k] = rho
    return out


def t1_t2_operators(T1: float | None, T2: float | None) -> list[np.ndarray]:
    """
    Construct Lindblad operators for relaxation (T1) and pure dephasing (Tphi derived from T1, T2).
    """
    Ls: list[np.ndarray] = []
    if T1 is not None and T1 > 0:
        gamma1 = 1.0 / T1
        Ls.append(np.sqrt(gamma1) * SIGMA_MINUS)
    if T2 is not None and T2 > 0:
        # 1/T2 = 1/(2 T1) + 1/Tphi  =>  1/Tphi = 1/T2 - 1/(2 T1)
        gamma1 = 0.0 if T1 is None or T1 <= 0 else 1.0 / T1
        gamma2 = 1.0 / T2
        gamma_phi = max(gamma2 - 0.5 * gamma1, 0.0)
        if gamma_phi > 0:
            Ls.append(np.sqrt(gamma_phi) * SIGMA_Z)
    return Ls


def excited_population(rho: np.ndarray) -> float:
    """Return excited-state population."""
    return float(np.real(rho[1, 1]))


__all__ = [
    "SIGMA_X",
    "SIGMA_Z",
    "SIGMA_MINUS",
    "SIGMA_PLUS",
    "lindblad_rhs",
    "solve_lindblad_two_level",
    "t1_t2_operators",
    "excited_population",
]

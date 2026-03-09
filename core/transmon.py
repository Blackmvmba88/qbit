"""Transmon Hamiltonian and spectral utilities."""

from __future__ import annotations

import math
import numpy as np

try:  # Prefer SciPy's tridiagonal solver for speed and stability.
    from scipy.linalg import eigh_tridiagonal  # type: ignore
except Exception:  # pragma: no cover - fallback handled below
    eigh_tridiagonal = None

# Physical constants (SI)
ELEM_CHARGE = 1.602176634e-19  # Coulomb
PLANCK = 6.62607015e-34  # J*s


def charging_energy(capacitance_farad: float) -> float:
    """
    Compute charging energy EC (joules) for capacitance C.
    EC = e^2 / (2C)
    """
    if capacitance_farad <= 0:
        raise ValueError("Capacitance must be positive.")
    return (ELEM_CHARGE ** 2) / (2.0 * capacitance_farad)


def _validate_params(EJ: float, EC: float, n_cut: int, levels: int) -> None:
    if EJ <= 0 or EC <= 0:
        raise ValueError("EJ and EC must be positive.")
    if n_cut < 1:
        raise ValueError("n_cut must be at least 1.")
    if levels < 1:
        raise ValueError("levels must be at least 1.")


def _transmon_tridiagonal(EJ: float, EC: float, n_cut: int, ng: float) -> tuple[np.ndarray, np.ndarray]:
    """Return (diag, offdiag) arrays for the charge-basis transmon Hamiltonian."""
    n = np.arange(-n_cut, n_cut + 1, dtype=np.float64)
    diag = 4.0 * EC * (n - ng) ** 2
    offdiag = -0.5 * EJ * np.ones(n.size - 1, dtype=np.float64)
    return diag, offdiag


def transmon_hamiltonian(EJ: float, EC: float, n_cut: int = 25, ng: float = 0.0) -> np.ndarray:
    """
    Build the dense transmon Hamiltonian in the charge basis truncated to |n| <= n_cut.
    Primarily for inspection; spectrum routines use a tridiagonal solve.
    """
    _validate_params(EJ, EC, n_cut, levels=1)
    diag, off = _transmon_tridiagonal(EJ, EC, n_cut, ng)
    H = np.diag(diag)
    H += np.diag(off, k=1) + np.diag(off, k=-1)
    return H


def transmon_spectrum(EJ: float, EC: float, n_cut: int = 25, levels: int = 6, ng: float = 0.0) -> np.ndarray:
    """Return the lowest `levels` eigenenergies (joules)."""
    _validate_params(EJ, EC, n_cut, levels)
    diag, off = _transmon_tridiagonal(EJ, EC, n_cut, ng)

    # Tridiagonal solver is O(N) and numerically stable for Hermitian tridiagonal matrices.
    if eigh_tridiagonal:
        eigvals = eigh_tridiagonal(diag, off, select="i", select_range=(0, min(levels - 1, diag.size - 1)))[0]
    else:  # Fallback: dense solver
        H = np.diag(diag)
        H += np.diag(off, k=1) + np.diag(off, k=-1)
        eigvals = np.linalg.eigvalsh(H)[:levels]

    return np.asarray(eigvals, dtype=np.float64)


def _freq_from_energy_diff(delta_energy_joule: float) -> float:
    """Convert energy difference to frequency in Hz."""
    return delta_energy_joule / PLANCK


def transmon_properties(
    EJ: float,
    EC: float,
    n_cut: int = 25,
    ng: float = 0.0,
    ng_charge_disp: float = 0.5,
) -> dict:
    """
    Compute key transmon figures:
    - E01 (GHz)
    - anharmonicity alpha = (w12 - w01) in GHz
    - charge dispersion for E01 in kHz (delta between ng and ng_charge_disp)
    """
    energies = transmon_spectrum(EJ, EC, n_cut=n_cut, levels=3, ng=ng)
    w01 = _freq_from_energy_diff(energies[1] - energies[0]) / 1e9
    w12 = _freq_from_energy_diff(energies[2] - energies[1]) / 1e9
    alpha = w12 - w01

    # Charge dispersion: compare E01 at ng and ng + 0.5
    energies_offset = transmon_spectrum(EJ, EC, n_cut=n_cut, levels=2, ng=ng_charge_disp)
    w01_offset = _freq_from_energy_diff(energies_offset[1] - energies_offset[0])
    charge_disp_khz = abs(w01_offset - w01 * 1e9) / 1e3  # Hz -> kHz

    return {
        "E01_GHz": w01,
        "alpha_GHz": alpha,
        "charge_dispersion_kHz": charge_disp_khz,
    }


__all__ = [
    "ELEM_CHARGE",
    "PLANCK",
    "charging_energy",
    "transmon_hamiltonian",
    "transmon_spectrum",
    "transmon_properties",
]

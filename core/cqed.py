"""Minimal Jaynes-Cummings (cQED) model utilities."""

from __future__ import annotations

import numpy as np


def jaynes_cummings_hamiltonian(omega_r: float, omega_q: float, g: float, n_cut: int = 5) -> np.ndarray:
    """
    Build the Jaynes-Cummings Hamiltonian in the basis |g,n> and |e,n>.

    Parameters are in GHz (not angular). The Hamiltonian is returned in GHz.
    H = omega_r * a† a + (omega_q / 2) * sigma_z + g (a† sigma_- + a sigma_+)
    """
    if n_cut < 0:
        raise ValueError("n_cut must be non-negative.")
    if g < 0:
        raise ValueError("Coupling g must be non-negative.")

    dim = 2 * (n_cut + 1)
    H = np.zeros((dim, dim), dtype=float)

    def idx(excited: bool, n: int) -> int:
        return 2 * n + (1 if excited else 0)

    # Oscillator term and qubit sigma_z term
    for n in range(n_cut + 1):
        H[idx(False, n), idx(False, n)] += omega_r * n - 0.5 * omega_q
        H[idx(True, n), idx(True, n)] += omega_r * n + 0.5 * omega_q

    # Coupling term g(a† sigma_- + a sigma_+)
    for n in range(n_cut):
        coupling = g * np.sqrt(n + 1)
        # |e,n> <-> |g,n+1>
        i = idx(True, n)
        j = idx(False, n + 1)
        H[i, j] = coupling
        H[j, i] = coupling

    return H


def jaynes_cummings_spectrum(omega_r: float, omega_q: float, g: float, n_cut: int = 5, levels: int = 6) -> np.ndarray:
    """Return the lowest `levels` eigenvalues (GHz) of the Jaynes-Cummings Hamiltonian."""
    H = jaynes_cummings_hamiltonian(omega_r, omega_q, g, n_cut=n_cut)
    eigvals = np.linalg.eigvalsh(H)
    eigvals.sort()
    return eigvals[:levels]


def vacuum_rabi_splitting(omega_r: float, omega_q: float, g: float) -> float:
    """
    Compute the vacuum Rabi splitting for the first doublet (GHz).
    On resonance (omega_r ≈ omega_q) the splitting approaches 2g.
    """
    eigvals = jaynes_cummings_spectrum(omega_r, omega_q, g, n_cut=1, levels=4)
    # One-excitation manifold energies are eigvals[1] and eigvals[2]
    return abs(eigvals[2] - eigvals[1])


__all__ = [
    "jaynes_cummings_hamiltonian",
    "jaynes_cummings_spectrum",
    "vacuum_rabi_splitting",
]


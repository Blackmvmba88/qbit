"""Single-qubit Clifford utilities."""

from __future__ import annotations

import numpy as np


def _rz(theta: float) -> np.ndarray:
    return np.array(
        [
            [np.exp(-1j * theta / 2), 0],
            [0, np.exp(1j * theta / 2)],
        ],
        dtype=complex,
    )


def _rx(theta: float) -> np.ndarray:
    return np.array(
        [
            [np.cos(theta / 2), -1j * np.sin(theta / 2)],
            [-1j * np.sin(theta / 2), np.cos(theta / 2)],
        ],
        dtype=complex,
    )


def _ry(theta: float) -> np.ndarray:
    return np.array(
        [
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [np.sin(theta / 2), np.cos(theta / 2)],
        ],
        dtype=complex,
    )


def clifford_set() -> list[np.ndarray]:
    """
    Return the 24 single-qubit Clifford unitaries as 2x2 matrices.
    Constructed from rotation generators.
    """
    cliffords = []
    # Identity
    I = np.eye(2, dtype=complex)
    cliffords.append(I)
    # +/- pi rotations about axes
    for axis in ("x", "y", "z"):
        cliffords.append(_rot(axis, np.pi))
        cliffords.append(_rot(axis, -np.pi))
    # +/- pi/2 rotations about axes
    for axis in ("x", "y", "z"):
        cliffords.append(_rot(axis, np.pi / 2))
        cliffords.append(_rot(axis, -np.pi / 2))
    # Combinations: ±π/2 about x then ±π about y, etc., to reach full 24
    # Explicitly enumerate common generating set used in RB (as in Magesan et al.)
    extra = [
        _rot("x", np.pi / 2) @ _rot("y", np.pi),
        _rot("x", -np.pi / 2) @ _rot("y", np.pi),
        _rot("y", np.pi / 2) @ _rot("x", np.pi),
        _rot("y", -np.pi / 2) @ _rot("x", np.pi),
        _rot("x", np.pi / 2) @ _rot("y", np.pi / 2),
        _rot("x", np.pi / 2) @ _rot("y", -np.pi / 2),
        _rot("x", -np.pi / 2) @ _rot("y", np.pi / 2),
        _rot("x", -np.pi / 2) @ _rot("y", -np.pi / 2),
        _rot("y", np.pi / 2) @ _rot("x", np.pi / 2),
        _rot("y", np.pi / 2) @ _rot("x", -np.pi / 2),
        _rot("y", -np.pi / 2) @ _rot("x", np.pi / 2),
        _rot("y", -np.pi / 2) @ _rot("x", -np.pi / 2),
    ]
    cliffords.extend(extra)
    # Deduplicate numerically
    uniq = []
    for U in cliffords:
        if not any(np.allclose(U, V) for V in uniq):
            uniq.append(U)
    return uniq


def _rot(axis: str, theta: float) -> np.ndarray:
    if axis == "x":
        return _rx(theta)
    if axis == "y":
        return _ry(theta)
    if axis == "z":
        return _rz(theta)
    raise ValueError("axis must be x, y, or z")


def random_clifford(rng: np.random.Generator | None = None) -> np.ndarray:
    rng = rng or np.random.default_rng()
    C = rng.choice(clifford_set())
    return C


def clifford_inverse(U: np.ndarray) -> np.ndarray:
    """Unitary inverse is the dagger."""
    return U.conj().T


__all__ = ["clifford_set", "random_clifford", "clifford_inverse"]


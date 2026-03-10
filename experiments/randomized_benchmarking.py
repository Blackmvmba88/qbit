"""Single-qubit randomized benchmarking (Clifford) with optional depolarizing noise."""

import argparse
import numpy as np
from numpy.linalg import norm

from core.clifford_1q import random_clifford, clifford_inverse


def depolarize(rho: np.ndarray, p: float) -> np.ndarray:
    """Apply single-qubit depolarizing channel with probability p."""
    if p <= 0:
        return rho
    I = np.eye(2, dtype=complex) / 2
    return (1 - p) * rho + p * I


def apply_unitary(rho: np.ndarray, U: np.ndarray) -> np.ndarray:
    return U @ rho @ U.conj().T


def survival_probability(rho: np.ndarray) -> float:
    """Return probability of measuring |0>."""
    return float(np.real(rho[0, 0]))


def run_sequence(m: int, p_depol: float, rng: np.random.Generator) -> float:
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    ops = [random_clifford(rng) for _ in range(m)]
    U_total = np.eye(2, dtype=complex)
    for U in ops:
        rho = apply_unitary(rho, U)
        rho = depolarize(rho, p_depol)
        U_total = U @ U_total
    U_inv = clifford_inverse(U_total)
    rho = apply_unitary(rho, U_inv)
    return survival_probability(rho)


def estimate_decay(lengths, trials, p_depol, rng):
    means = []
    stds = []
    for m in lengths:
        vals = [run_sequence(m, p_depol, rng) for _ in range(trials)]
        means.append(np.mean(vals))
        stds.append(np.std(vals))
    return np.array(means), np.array(stds)


def fit_exponential(lengths, means):
    """
    Fit P(m) ~ 0.5 + 0.5 p^m  (standard 1Q RB with SPAM folded into A,B omitted).
    Use log on y = 2P-1 > 0.
    """
    y = 2 * means - 1
    mask = y > 0
    if np.count_nonzero(mask) < 2:
        return np.nan
    logy = np.log(y[mask])
    slope, _ = np.polyfit(lengths[mask], logy, 1)
    p = np.exp(slope)
    r = (1 - p) / 2
    return r


def main():
    parser = argparse.ArgumentParser(description="Single-qubit randomized benchmarking.")
    parser.add_argument("--lengths", nargs="+", type=int, default=[2, 4, 8, 16, 32])
    parser.add_argument("--trials", type=int, default=30)
    parser.add_argument("--p-depol", type=float, default=0.0, help="Depolarizing probability per Clifford.")
    parser.add_argument("--seed", type=int, default=1234)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    lengths = np.array(args.lengths, dtype=int)
    means, stds = estimate_decay(lengths, args.trials, args.p_depol, rng)
    r = fit_exponential(lengths, means)

    print("Randomized Benchmarking (1Q Clifford)")
    print(f"Depolarizing p per Clifford: {args.p_depol}")
    print("Length   Survival   Std")
    for m, mu, sd in zip(lengths, means, stds):
        print(f"{m:6d}   {mu:8.4f}  {sd:6.4f}")
    print(f"Estimated error per Clifford r ≈ {r:.4e}" if np.isfinite(r) else "Not enough data to fit.")


if __name__ == "__main__":
    main()


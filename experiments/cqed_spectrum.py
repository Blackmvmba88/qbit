"""Demonstrate vacuum Rabi splitting for a resonant cQED system."""

from core.cqed import jaynes_cummings_spectrum, vacuum_rabi_splitting


def main() -> None:
    omega_r = 7.0  # GHz cavity
    omega_q = 7.0  # GHz qubit (resonant)
    g = 0.1        # GHz coupling
    n_cut = 4

    eigs = jaynes_cummings_spectrum(omega_r, omega_q, g, n_cut=n_cut, levels=6)
    split = vacuum_rabi_splitting(omega_r, omega_q, g)

    print("cQED spectrum (lowest 6 levels) [GHz]:")
    for i, e in enumerate(eigs):
        print(f"  {i}: {e:.4f}")
    print(f"Vacuum Rabi splitting ≈ {split:.4f} GHz (expected ≈ {2*g:.4f} GHz)")


if __name__ == "__main__":
    main()

